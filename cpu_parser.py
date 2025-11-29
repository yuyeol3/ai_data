import pandas as pd
import re

df_raw = pd.read_excel("CPU_BENCHMARKS.xlsx")  # 한 열짜리
col = df_raw.columns[0]                        # 첫 번째 열 이름

def parse_row(s: str):
    # 1) 이름 + 퍼센트 분리
    name_part, rest = s.rsplit('(', 1)
    name = name_part.strip()

    # 2) 괄호 안의 퍼센트
    perc_str, rest2 = rest.split('%)', 1)
    rel_perf = float(perc_str)  # 예: '59.4' -> 59.4

    after = rest2  # 뒤에 value + score + price 전부 붙어있는 부분

    # 3) price(끝부분) 찾기: 'NA' 또는 '$...'
    m_price = re.search(r'(NA|\$.*)$', after)
    price_str = m_price.group(1)
    before_price = after[:m_price.start()]

    if price_str == "NA":
        price = None
    else:
        price = float(
            price_str.replace('$', '').replace('*', '').replace(',', '')
        )

    # 4) value / score 나누기
    #    - value: 소수점 1자리까지 (예: '53.9')
    #    - score: 나머지 (예: '24,644')
    if before_price.startswith('NA'):
        value = None
        score_str = before_price[2:]  # 'NA' 뒤부터
    else:
        dot = before_price.find('.')
        # 소수점 한 자리까지만 value로 사용
        value_str = before_price[:dot+2]      # '53.9'
        value = float(value_str)
        score_str = before_price[dot+2:]      # '24,644'

    score = int(score_str.replace(',', ''))

    return name, rel_perf, value, score, price

parsed_rows = [parse_row(s) for s in df_raw[col]]

df = pd.DataFrame(
    parsed_rows,
    columns=["name", "rel_perf", "value", "score", "price"]
)

print(df.head())
df.to_csv("cpu_benchmarks.csv")