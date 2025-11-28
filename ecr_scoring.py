import pandas as pd

df = pd.read_csv("ecr_raw.csv")

# 2) 문항/역채점 정보 정의
question_cols = [f"Q{i}" for i in range(1, 37)]

anxiety_items = [f"Q{i}" for i in range(1, 19)]      # Q1~Q18
avoidance_items = [f"Q{i}" for i in range(19, 37)]   # Q19~Q36

# 공식 ECR-R 역채점 문항
reverse_anxiety = ["Q9", "Q11"]
reverse_avoidance = ["Q20", "Q22", "Q26", "Q27", "Q28",
                     "Q29", "Q30", "Q31", "Q33", "Q34", "Q35", "Q36"]

# 3) 역채점 처리
LIKERT_MAX = 7  # 만약 척도가 1~5면 5로 바꿔줘

df_rev = df.copy()

df_rev[reverse_anxiety]  = (LIKERT_MAX + 1) - df_rev[reverse_anxiety]
df_rev[reverse_avoidance] = (LIKERT_MAX + 1) - df_rev[reverse_avoidance]

# 4) anxiety / avoidance 평균 점수 계산
df_rev["anxiety"]  = df_rev[anxiety_items].mean(axis=1)
df_rev["avoidance"] = df_rev[avoidance_items].mean(axis=1)

# 5) 중앙값 기준으로 4유형 라벨 만들기
anx_med = df_rev["anxiety"].median()
avo_med = df_rev["avoidance"].median()

def categorize_attachment(row):
    high_anx = row["anxiety"]  > anx_med
    high_avo = row["avoidance"] > avo_med

    if not high_anx and not high_avo:
        return "secure"      # 안정 애착
    elif high_anx and not high_avo:
        return "anxious"     # 불안 애착
    elif not high_anx and high_avo:
        return "avoidant"    # 회피 애착
    else:
        return "fearful"     # 두 개 다 높은 경우

df_rev["attachment_style"] = df_rev.apply(categorize_attachment, axis=1)

# 6) 분류용 X, y 뽑기 예시
feature_cols = question_cols + ["age", "gender"]  # country는 빼고 싶으면 빼도 됨
X = df_rev[feature_cols]
y = df_rev["attachment_style"]

# 필요하면 CSV로 저장해서 과제용 train/test로 쓰기
df_rev.to_csv("ecr_with_labels.csv", index=False)
