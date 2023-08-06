import pickle
import pprint
from typing import Callable, Dict, Union, List, Optional, Tuple

import numpy as np
from torch.utils.data import Dataset, DataLoader, RandomSampler
import torch
from torch import nn

from yafal.corruption import DatasetCorruptor
from yafal.label import YAFALLabelEncoder
from yafal.models import YAFALDataset
from .binary import BinaryYAFAL
from .semantic import SemanticYAFAL
from ..exceptions import InvalidMethodException, DescriptorsRequiredException


class YAFALTorchDataset(Dataset):
    def __init__(self, dataset: YAFALDataset,
                 label_encoder: Callable,
                 label_transform: str = "binary",
                 ):
        """
        Torch handler for the YAFAL dataset class to be used by a Torch data handler

        Parameters
        ----------

        :param dataset:
        :param label_transform: Callable
            method to transform
        """

        self.dataset = dataset
        self.label_transform = label_transform
        self.label_encoder = label_encoder

    def __len__(self):
        return len(self.dataset.samples)

    def add_sample(self, *args, **kwargs):
        return self.dataset.add_sample(*args, **kwargs)

    def __getitem__(self, index):
        sample = self.dataset.samples[index]
        if self.label_transform == "binary":
            original_label_transform = torch.FloatTensor(
                self.label_encoder(self.dataset.labels[index])[0]
            )
        else:
            original_label_transform = self.label_encoder(self.dataset.labels[index])[0]
        label_to_predict = torch.FloatTensor([self.dataset.is_corrupted[index]])
        return sample, original_label_transform, label_to_predict


class YAFALRegression:
    def __init__(self, label_encoder_method: str,
                 corrupt_percentage: float = 0.3,
                 keep_original: bool = True,
                 n_rounds: int = 1,
                 max_labels_to_corrupt: int = -1,
                 validation_corpus_ratio: float = 0.2,
                 max_epochs: int = 4,
                 verbose: bool = False,
                 device: str = "cpu",
                 batch_size: int = 64,
                 freeze_label_encoder: bool = True,
                 freeze_sequence_encoder: bool = True,
                 early_stopping: bool = True,
                 patience: int = 5,
                 **yafal_kwargs
                 ):
        """

        Parameters
        ----------

        label_encoder_method: str
            String in "binary" or "semantic"

        corrupt_percentage: float, default=0.3
            The amount of noise to add to the original dataset

        keep_original: bool, default=True
            If we want to keep the original sample once it is corrupted

        n_rounds: int, default=1
            Number of rounds to corrupt the dataset

        max_labels_to_corrupt: int, default=-1
            Maximum amount of labels to corrupt from the sample (for multi-label). If -1, all labels will be flipped.

        validation_corpus_ratio: float, default=0.2
            Percentage of the corpus to use for validation

        max_epochs: int, default=4
            Number of maximum epochs to train the network

        verbose: bool, default=False
            Print debugging info during training or not

        device: str, default="cpu"
            The device to use for training

        batch_size: int, default=64
            Batch size for training

        freeze_label_encoder: bool, default=True
            If we want to freeze the LLM that encodes the model for training

        freeze_sequence_encoder: bool, default=True
            If we want to freeze the LLM that encodes the sequence for training

        early_stopping: bool, default=True
            If we want to stop the training early if the metrics are not being improved in the validation set

        patience: int, default=5
            Number of rounds to wait where the validation set scores do not improved before stopping

        **yafal_kwargs: kwargs
            Keywords arguments that are passed to the YAFALRegressors' underlying model

        """

        self._verbose = verbose
        self._yafal_kwargs = yafal_kwargs
        self._label_encoder = YAFALLabelEncoder()
        self._dataset_corruptor = DatasetCorruptor(probability=corrupt_percentage, keep_original=keep_original,
                                                   n_rounds=n_rounds, max_labels_to_corrupt=max_labels_to_corrupt)
        self.encoding_method = label_encoder_method
        if label_encoder_method == "binary":
            self.__model_loader = BinaryYAFAL
        elif label_encoder_method == "semantic":
            self.__model_loader = SemanticYAFAL
        else:
            raise InvalidMethodException("Label encoding method should be either 'binary' or 'semantic'")

        # Training parameters
        self._val_ratio = validation_corpus_ratio
        self._max_epochs = max_epochs
        self.device = device
        self._batch_size = batch_size
        self._freeze_encoder = freeze_label_encoder
        self._freeze_sequence_encoder = freeze_sequence_encoder
        self.model = None
        self._do_early_stopping = early_stopping
        self._patience = patience
        self._best_model_state_dict = None

    def _vprint(self, text: str):
        if self._verbose:
            pprint.pprint(text)

    def fit(self, x: YAFALDataset,
            descriptors: Optional[Dict[Union[str, int], List[str]]] = None):
        """
        Parameters
        ----------

        x: YAFALDataset
            Dataset to train the Regressor

        descriptors: Dict
            Dict of the form {"label": ["describing keywords"]}

            >>> {"sports": ["football", "gym", "exercise"]}

        """

        train_losses, valid_losses = [], []
        avg_train_losses, avg_valid_losses = [], []

        # Fit the label encoder
        if self.encoding_method == "semantic":
            if not descriptors:
                raise DescriptorsRequiredException("Semantic label encoding was "
                                                   "selected but no encoding method was provided")

            self._label_encoder.fit(
                x.label_list, descriptors
            )
            if not self._label_encoder.validate_descriptions():
                raise DescriptorsRequiredException("Some of the labels do not have any descriptor")
            self.model = self.__model_loader(**self._yafal_kwargs)
            self.__freeze_label_encoder()
        else:
            self._label_encoder.fit(x.label_list, None)
            self.model = self.__model_loader(label_encoding_size=len(self._label_encoder.label_indexes),
                                             **self._yafal_kwargs)

        self.__freeze_encoder()

        # Split in train and validation sets
        x_train, x_validation = self._split_train_val(x)

        # Corrupt the datasets
        x_train_corrupt = self._dataset_corruptor.transform(
            dataset=x_train
        )
        x_val_corrupt = self._dataset_corruptor.transform(
            dataset=x_validation,
        )

        # Start the training
        torch_data_handler = YAFALTorchDataset(dataset=x_train_corrupt,
                                               label_encoder=self._label_encoder.transform if
                                               self.encoding_method == "binary" else self._label_encoder.describe,
                                               label_transform=self.encoding_method)

        torch_validation_data_handler = YAFALTorchDataset(dataset=x_val_corrupt,
                                                          label_encoder=self._label_encoder.transform if
                                                          self.encoding_method == "binary"
                                                          else self._label_encoder.describe,
                                                          label_transform=self.encoding_method)

        train_data_loader = DataLoader(
            torch_data_handler,  # The training samples.
            sampler=RandomSampler(torch_data_handler),  # Select batches randomly
            batch_size=self._batch_size  # Trains with this batch size.
        )

        val_data_loader = DataLoader(
            torch_validation_data_handler,  # The training samples.
            batch_size=self._batch_size  # Trains with this batch size.
        )

        # Use it for training
        self.model.to(torch.device(self.device))

        criterion = nn.BCELoss()  # Binary Cross Entropy Loss for 0/1 regression
        optimizer = torch.optim.AdamW(filter(lambda p: p.requires_grad, self.model.parameters()), lr=0.004)

        self.model.train()
        remaining_patience = self._patience
        best_loss = 1e6
        for epoch in range(self._max_epochs):
            self._vprint('======== Epoch {:} / {:} ========'.format(epoch + 1, self._max_epochs))

            for index, (texts, label_encodings, targets) in enumerate(train_data_loader):
                optimizer.zero_grad()
                if self.encoding_method == "semantic":
                    label_encodings = list(label_encodings)
                outputs = self.model(list(texts), label_encodings)
                loss = criterion(outputs, targets)
                train_losses.append(loss.item())
                loss.backward()
                optimizer.step()

            # Perform the validation
            self.model.eval()
            with torch.no_grad():
                for index, (texts, label_encodings, targets) in enumerate(val_data_loader):
                    if self.encoding_method == "semantic":
                        label_encodings = list(label_encodings)
                    outputs = self.model(list(texts), label_encodings)
                    val_loss = criterion(outputs, targets)
                    valid_losses.append(val_loss.item())

            avg_train_losses.append(
                np.average(train_losses)
            )
            avg_valid_losses.append(
                np.average(valid_losses)
            )
            self._vprint("Training set loss: {} / Val loss: {}".format(avg_train_losses[-1], avg_valid_losses[-1]))
            # Early Stopping
            if self._do_early_stopping:
                if avg_valid_losses[-1] > best_loss:
                    remaining_patience -= 1
                else:
                    best_loss = avg_valid_losses[-1]
                    remaining_patience = self._patience
                    self._best_model_state_dict = self.model.state_dict()
                if remaining_patience <= 0:
                    self._vprint("There were no improvements after {} rounds. Stopping.".format(self._patience))
                    self.model.load_state_dict(self._best_model_state_dict)
                    break

    def _split_train_val(self, x: YAFALDataset) -> Tuple[YAFALDataset, YAFALDataset]:
        x_train = YAFALDataset()
        x_validation = YAFALDataset()
        train_indexes, validation_indexes = x.split_indexes(ratio=self._val_ratio)
        for sample_index in train_indexes:
            sample, labels, is_corrupted = x[sample_index]
            x_train.add_sample(text=sample, sample_labels=labels, is_corrupted=is_corrupted)
        for sample_index in validation_indexes:
            sample, labels, is_corrupted = x[sample_index]
            x_validation.add_sample(text=sample, sample_labels=labels, is_corrupted=is_corrupted)
        return x_train, x_validation

    def __freeze_label_encoder(self):
        if self._freeze_encoder:
            for param in self.model.label_bert.parameters():
                param.requires_grad = False

    def __freeze_encoder(self):
        if self._freeze_sequence_encoder:
            for param in self.model.bert.parameters():
                param.requires_grad = False

    def predict(self, x: List[str], labels: List[Union[int, str, List[Union[str, int]]]]) -> np.ndarray:
        """
        Predicts score of the sample being corrupted given the list of strings and the labels of those strings

        Parameters
        ----------
        x: List[str]
            List of texts to predict

        labels:  List[Union[int, str, List[Union[str, int]]]]
            Labels associated with the input samples of x

        Returns
        -------
        np.ndarray
            Array with the predictions of shape (len(x), 1)
        """
        if self.encoding_method == "binary":
            codified_labels = self._label_encoder.transform(labels)
            label_encoding = torch.FloatTensor(codified_labels)
        else:
            label_encoding = self._label_encoder.describe(labels)
        with torch.no_grad():
            return self.model(x, label_encoding)

    def save(self, file_path: str):
        """
        Saves the model with the given filename

        Parameters
        ----------
        file_path: str
            Path to save the model
        """
        self.model.load_state_dict(self._best_model_state_dict)
        # Remove intermediate model to lighten the saved item
        self._best_model_state_dict = None
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)
