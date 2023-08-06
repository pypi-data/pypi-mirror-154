"""
Implements the Semantic Label Encoder
"""
import typing
from typing import List, Union

import numpy as np


class YAFALLabelEncoder:
    """Performs the semantic encoding of the labels for the YAFAL regressors
    """

    def __init__(self, ):
        """
        Initializes the YAFAL Label Encoder Class
        """

        self.label_indexes = []
        self.label_map = {}

    @staticmethod
    def __check_label_type(label_list: List[Union[int, str]]) -> None:
        label_types = set([type(label) for label in label_list])
        if len(label_types) != 1:
            raise Exception("Only one data type is expected for labels, received: {}".format(set(label_types)))
        label_type = label_types.pop()
        if label_type not in [int, str]:
            raise Exception("Label type needs to be int or str, received: {}".format(label_type))

    def fit(self, labels: List[Union[int, str]],
            label_descriptors=None) -> None:
        """
        Builds the YAFAL Label Encoder with the required labels and optionally with the label descriptors

        Parameters
        ----------

        labels: list, list of integers of strings
            List of labels to train the YAFAL Label Encoder

        label_descriptors: optional, dictionary with the label descriptors
            Dictionary of type ``{label: [descriptor_text, descriptor_text2, ...]}``

        """
        self.__check_label_type(labels)
        for label in labels:
            if not self.label_map.get(label):
                # The label does not exists
                label_index = len(self.label_indexes)
                self.label_indexes.append(label_index)
                self.label_map[label] = {
                    "index": label_index,
                    "descriptors": []
                }
        if label_descriptors:
            for label_identifier in label_descriptors:
                if label_identifier in self.label_map:
                    self.label_map[label_identifier]["descriptors"] = label_descriptors[label_identifier]
                else:
                    raise Exception('Label "{}" not found when updating descriptors.'.format(label_identifier))

    def transform(self, labels: List[Union[int, str, List[Union[str, int]]]]) -> np.ndarray:
        """
        Given a list of labels, composed either of integers, strings or lists (for multilabel)
        and returns the numpy array representation.

        Parameters
        ----------

        labels: list
            List of labels, they can be of type int, str or nested for multi-label classifiers
            ``labels = [1, 0 , 0, 1, 1]``

        Returns
        -------

        label_array : ndarray of shape (n_samples, n_labels)
            Label array
        """
        label_transform = np.zeros((len(labels), len(self.label_indexes)))
        for i in range(len(labels)):
            if isinstance(labels[i], list):
                for sub_label in labels[i]:
                    label_index = self.label_map[sub_label]["index"]
                    label_transform[i, label_index] = 1
            else:
                label_index = self.label_map[labels[i]]["index"]
                label_transform[i, label_index] = 1
        return label_transform

    def describe(self, labels: List[Union[int, str]], separator_token: str = " [SEP] ",
                 max_descriptors: int = 5) -> typing.List[str]:
        """Creates the description of the given labels for semantic encoding in LLM.

        .. warning::
            Currently it does not support multi-label description. I still have my doubts if in a multi-label
            setup if a micro or macro corruption method should be taken into account.

        Parameters
        ----------

        labels : list
            List of labels to encode:

                ``labels = [1, 0 , 0, 1, 1]``

                ``labels = ["hi", "bye" , "hi", "bye", "hi"]``

        separator_token : str, default=" [SEP] "
            Separator token to join the different descriptions given for each label. Currently, the separator used for
            BERT is used.

        max_descriptors : int, default=5
            Amount of descriptors to use to describe a label

        Returns
        -------
        list
            List of strings describing each one of the labels

        """
        if max_descriptors < 1:
            raise Exception("At least one descriptor needs to be employed (max_descriptions=1)")
        texts_to_return = []
        for label in labels:
            texts_to_return.append(
                separator_token.join(self.label_map[label]["descriptors"][:max_descriptors])
            )
        return texts_to_return

    def update_descriptors(self, label_identifier: Union[int, str], descriptors: List[str]) -> None:
        """
        Updates the descriptors of a label identifier

        Parameters
        ----------

        :param label_identifier: str
            Identifier of the label to update, it must be available in the label map

        :param descriptors: list, List of strings used to describe the label


        """
        if label_identifier not in self.label_map:
            raise Exception('Label id "{}" not found in the label map.'.format(label_identifier))
        self.label_map[label_identifier]["descriptors"] = descriptors

    def validate_descriptions(self) -> bool:
        """
        Checks that all the labels have the required semantic description

        Returns
        -------

        :return: bool,
            If the descriptions are valid or not

        """
        if not self.label_map:
            return False
        for label in self.label_map:
            if not self.label_map[label]["descriptors"]:
                return False
        return True
