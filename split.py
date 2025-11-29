from sklearn.model_selection import train_test_split
import pandas as pd


df = pd.read_csv("trees.csv")

train_df, test_df = train_test_split(
    df, 
    test_size=0.2,
    random_state=42,
    shuffle=True
)

train_df.to_csv("classification_train.csv", index=False)
test_df.to_csv("classification_test.csv", index=False)