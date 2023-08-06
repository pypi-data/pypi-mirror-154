import random

import numpy as np

from yafal.label import YAFALLabelEncoder


def test_label_encoder_binary_single_label():
    encoder = YAFALLabelEncoder()
    # Test 1: use integers as labels
    label_list = list(range(10))*2
    encoder.fit(label_list)
    assert set(encoder.label_indexes) == set(label_list)

    # Test1.1: Transform each label individually
    for i, label in enumerate(range(10)):
        result = encoder.transform([label])
        result_to_compare = np.zeros((1, len(label_list)))
        result_to_compare[0, i] = 1
        assert result.all() == result_to_compare.all()

    # Test 1.2: Transform several items at once
    batch_result = encoder.transform(list(range(10)))
    assert batch_result.all() == np.eye(10).all()

    # Test 1.3: test the empty result
    assert np.zeros((0, 10)).all() == encoder.transform([]).all()
    # Test 1.4: test some unseen label - this should crash
    for unseen in [-1, len(label_list)+2]:
        try:
            encoder.transform([unseen])
        except KeyError:
            # This should happen
            pass
        except Exception:
            raise Exception("The label encoder does not fail when unseen labels are given")

    # Test 2: use texts as labels
    encoder = YAFALLabelEncoder()
    labels = [f"label-{i}" for i in range(10)]*2
    encoder.fit(labels)
    # Test that there are 10 total labels
    assert set(encoder.label_indexes) == set(list(range(10)))
    # Test that every label is in the label map
    for label in labels:
        assert label in encoder.label_map

    for i, label in enumerate(labels):
        result = encoder.transform([label])
        result_to_compare = np.zeros((1, len(label_list)))
        result_to_compare[0, i] = 1
        assert result.all() == result_to_compare.all()
    batch_result = encoder.transform(labels)
    assert batch_result.all() == np.eye(10).all()


def test_label_encoder_binary_multi_label():
    encoder = YAFALLabelEncoder()
    # Test 1: use integers as labels
    label_list = list(range(10))
    encoder.fit(label_list)
    assert set(encoder.label_indexes) == set(label_list)

    # Test1.1: Transform each label individually
    samples, transformations = [], []
    for try_number in range(1000):
        items_to_sample = random.choice(list(range(1, 10)))
        selected_labels = random.sample(label_list, k=items_to_sample)
        expected_result = np.zeros((1, 10))
        expected_result[0, selected_labels] = 1
        assert encoder.transform([selected_labels]).all() == expected_result.all()
        samples.append(selected_labels)
        transformations.append(expected_result)

    assert encoder.transform(samples).all() == np.vstack(transformations).all()

    # Test 2: use texts as labels
    encoder = YAFALLabelEncoder()
    labels = [f"label-{i}" for i in range(10)] * 2
    encoder.fit(labels)
    # Test that there are 10 total labels
    assert set(encoder.label_indexes) == set(list(range(10)))
    # Test that every label is in the label map
    for label in labels:
        assert label in encoder.label_map

    samples, transformations = [], []
    for try_number in range(1000):
        items_to_sample = random.choice(list(range(1, 10)))
        selected_labels = random.sample(labels, k=items_to_sample)
        selected_label_indexes = [labels.index(selected_label) for selected_label in selected_labels]
        expected_result = np.zeros((1, 10))
        expected_result[0, selected_label_indexes] = 1
        assert encoder.transform([selected_labels]).all() == expected_result.all()
        samples.append(selected_labels)
        transformations.append(expected_result)

    assert encoder.transform(samples).all() == np.vstack(transformations).all()


def test_label_encoder_semantic_single_label():
    encoder = YAFALLabelEncoder()
    labels = [f"label-{i}" for i in range(10)]
    encoder.fit(labels,
                label_descriptors={label: [f"desc-{j}" for j in range(i)] for i, label in enumerate(labels)})
    assert set(encoder.label_indexes) == set(range(len(labels)))
    # The first label has no descriptors, so the check should not be ok
    assert not encoder.validate_descriptions()
    # Let's update the descriptor of the first label
    encoder.update_descriptors(
        label_identifier="label-0",
        descriptors=["desc-0"]
    )
    # Now everything should be OK
    assert encoder.validate_descriptions()
    for label_index in range(1, len(labels)):
        label = labels[label_index]
        supposed_descriptor = [' [SEP] '.join([f"desc-{j}" for j in range(label_index)])]
        encoder_result = encoder.describe([label], max_descriptors=10)
        assert encoder_result == supposed_descriptor

    # Check that the max_descriptors parameter works
    for i in range(1, len(labels)):
        descriptions = encoder.describe(labels, max_descriptors=i)
        for descr in descriptions:
            assert len(descr.split(' [SEP] ')) <= i
