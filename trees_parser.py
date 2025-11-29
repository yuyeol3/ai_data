import pandas as pd

df = pd.read_csv("baeume.csv")  

num_cols = ["hoehe", "stammdurchmesser", "stammumfang", "kronendurchmesser"]

df = df.dropna()

# label: 속 이름(독일어)
label_col = "gattung_deutsch"

# 각 속별 개수
counts = df[label_col].value_counts()

# 예: 샘플 500개 이상 있는 속만 사용
valid_species = counts[counts >= 500].index
df = df[df[label_col].isin(valid_species)]


print(df.head())
df.to_csv("trees.csv")