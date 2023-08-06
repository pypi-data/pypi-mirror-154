import os

from yafal import YAFALDataset, YAFALRegression
from yafal.corruption import DatasetCorruptor
import pandas as pd
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score

current_dir = os.path.dirname(os.path.abspath(__file__))
train_csv_path = os.path.join(current_dir, 'data', 'train.csv')
test_csv_path = os.path.join(current_dir, 'data', 'test.csv')

train_data = pd.read_csv(train_csv_path)
test_data = pd.read_csv(test_csv_path)

topic_mapping = {1: 'world',
                 2: 'sports',
                 3: 'business',
                 4: 'science'}

train_yafal_dataset = YAFALDataset()
total_samples = 10000  # To make everything faster
for i, sample in train_data.iterrows():
    index_label = sample['Class Index']
    string_label = topic_mapping[index_label]
    news_article = f"{sample['Title']}. {sample['Description']}"
    train_yafal_dataset.add_sample(
        text=news_article,
        sample_labels=[string_label]
    )
    # For speedup
    if i == total_samples:
        break

# Train our model
print("Let's train our YAFAL Regressor")
yafal_regression = YAFALRegression(label_encoder_method="semantic", verbose=True, max_epochs=10)
yafal_regression.fit(train_yafal_dataset,
                     descriptors={"world": ["politics", "international", "global", "world"],
                                  "sports": ["soccer", "basketball", "sport", "workout", "gym"],
                                  "business": ["economics", "trade", "money", "business"],
                                  "science": ["science", "technology", "innovation", "research"]})

# Save the model

yafal_regression.save("YAFAL_ag_semantic_model.pck")

# Test the model - Load a new YAFAL dataset for the test
test_yafal_dataset = YAFALDataset()
total_test_samples = 2000
for i, sample in train_data.iterrows():
    index_label = sample['Class Index']
    string_label = topic_mapping[index_label]
    news_article = f"{sample['Title']}. {sample['Description']}"
    test_yafal_dataset.add_sample(
        text=news_article,
        sample_labels=[string_label]
    )
    if i == total_test_samples:
        break

# Corrupt the dataset
corruptor = DatasetCorruptor()
corrupted_test_dataset = corruptor.transform(test_yafal_dataset)

# Predict with our model
y_true, y_predicted = [], []
for sample, labels, is_corrupted in corrupted_test_dataset:
    result = yafal_regression.predict([sample], labels=labels)
    y_true.append(is_corrupted)
    y_predicted.append(result.item())

y_predicted_class = [0 if predict < 0.5 else 1 for predict in y_predicted]

print('Accuracy score: {}'.format(accuracy_score(y_true, y_predicted_class)))
print('Precision score: {}'.format(precision_score(y_true, y_predicted_class)))
print('Recall score: {}'.format(recall_score(y_true, y_predicted_class)))
print('ROC AUC score: {}'.format(roc_auc_score(y_true, y_predicted)))
