import os

from yafal import YAFALDataset, YAFALRegression
import pandas as pd

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
for i, sample in train_data.iterrows():
    index_label = sample['Class Index']
    string_label = topic_mapping[index_label]
    news_article = f"{sample['Title']}. {sample['Description']}"
    train_yafal_dataset.add_sample(
        text=news_article,
        sample_labels=[index_label]
    )

# Train our model
print("Let's train our YAFAL Regressor")
yafal_regression = YAFALRegression(label_encoder_method="binary", verbose=True, max_epochs=10)
yafal_regression.fit(train_yafal_dataset)

# Predict our model
for sample in test_data.iterrows():
    result = yafal_regression.predict(["Cristiano ronaldo scores 4 goals against Manchester City"], labels=[4])
    print(result)