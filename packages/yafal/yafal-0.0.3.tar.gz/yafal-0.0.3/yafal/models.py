from typing import List, Tuple, Union
from pydantic import BaseModel
from sklearn.model_selection import train_test_split


class YAFALDataset(BaseModel):
    """Dataset model to handle the required transformations in YAFAL!
    """
    samples: List[str] = []
    labels: List[List[int]] = []
    is_corrupted: List[int] = []

    def add_sample(self, text: str, sample_labels: List[Union[int, str]], is_corrupted: int = 0) -> None:
        """ Adds a sample to the dataset

        Parameters
        ----------
        text : str
            Sample to add

        sample_labels : List[Union[int, str]]
            List of the labels associated to this sample. The list should contain only one item for single-label
            settings, else, more.

        is_corrupted: int, default = 0
            If the sample is corrupted (wrong label) or not. 0 if OK, 1 if corrupted.

        """
        self.samples.append(text)
        self.labels.append(sample_labels)
        self.is_corrupted.append(is_corrupted)

    @property
    def label_list(self):
        label_list = []
        for labels in self.labels:
            label_list += labels
        return sorted(list(set(label_list)))

    def __iter__(self) -> Tuple[str, List[int], int]:
        for sample, label, is_corrupted in zip(self.samples, self.labels, self.is_corrupted):
            yield sample, label, is_corrupted

    def __len__(self):
        return len(self.samples)

    def split_indexes(self, ratio: float) -> Tuple[List[int], List[int]]:
        """ Split the dataset according to a given ratio and returns the split indexes

        """
        train_indexes, validation_indexes, labels_train, label_validations = \
            train_test_split(range(len(self.samples)), self.labels, test_size=ratio)
        return train_indexes, validation_indexes

    def __getitem__(self, index: int):
        return self.samples[index], self.labels[index], self.is_corrupted[index]

