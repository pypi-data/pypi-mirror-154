import random
import typing

from yafal.models import YAFALDataset


class DatasetCorruptor:
    def __init__(self, probability: float = 0.3, keep_original: bool = True,
                 n_rounds: int = 1, max_labels_to_corrupt: int = -1):
        """
        Class used to corrupt / flip the labels of an original YAFAL dataset.

        Parameters
        ----------

        probability: float, default=0.3
            Probability to select a sample to flip the labels from it.

        keep_original: bool, default=True
            If we want to keep the original sample after the corruption or not.

        n_rounds: int, default=1
            How many times do we want to iterate over this dataset to corrupt it.

        max_labels_to_corrupt: int, default=-1
            Mostly for multi-label tasks, how many labels do we want to corrupt if the sample is selected.
            For example, if the sample has 4 labels, and if 'max_labels_to_corrupt'=3, three will be flipped.
            If -1 is selected, all the labels will be flipped/corrupted randomly.

        """
        self._p = probability
        self._keep_original = keep_original
        self._n_rounds = n_rounds
        self._max_labels_to_corrupt = max_labels_to_corrupt

    def flip_labels(self, original_labels: typing.List[int], available_labels: typing.List[int]) -> typing.List[int]:
        """
        Flip the original labels using the set of available labels to that ent

        Parameters
        ----------

        original_labels: List[int]
            Original labels to flip

        available_labels: List[int]
            Labels that can be used to flip the original labels

        Returns
        -------
        List[int]
            List of new (flipped) labels
        """
        if self._max_labels_to_corrupt < 0:
            # Corrupt all the labels
            num_labels_to_corrupt = len(original_labels)
        else:
            num_labels_to_corrupt = min(len(original_labels), self._max_labels_to_corrupt)

        selected_labels = random.sample(original_labels, k=num_labels_to_corrupt)

        # Initialise the new labels with the ones that are not selected to be corrupted
        new_labels = [label for label in original_labels if label not in selected_labels]

        for label_to_corrupt in selected_labels:
            corrupted_label = random.choice([possible_label for possible_label in available_labels if
                                             possible_label != label_to_corrupt])
            new_labels.append(corrupted_label)

        return list(set(new_labels))

    def transform(self, dataset: YAFALDataset) -> YAFALDataset:
        """
        Transforms the input dataset into a corrupted one

        Parameters
        ----------

        dataset: YAFALDataset
            Original, non-corrupted, dataset

        Returns
        -------

        YAFALDataset:
            Corrupted dataset using the above one
        """
        corrupted_dataset = YAFALDataset()

        for epoch in range(self._n_rounds):

            for sample, label_list, _ in dataset:
                if self.__flip_sample():
                    new_labels = self.flip_labels(label_list, available_labels=dataset.label_list)
                    corrupted_dataset.add_sample(
                        text=sample,
                        sample_labels=new_labels,
                        is_corrupted=1
                    )
                    if self._keep_original:
                        corrupted_dataset.add_sample(
                            text=sample,
                            sample_labels=label_list,
                            is_corrupted=0
                        )
                else:
                    corrupted_dataset.add_sample(
                        text=sample,
                        sample_labels=label_list,
                        is_corrupted=0
                    )

        return corrupted_dataset

    def __flip_sample(self) -> bool:
        return random.random() < self._p
