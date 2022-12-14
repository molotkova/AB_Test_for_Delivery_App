import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu

# Upload and prepare data
df_ab = pd.read_csv('test/ab_test.csv')
p_ov = np.percentile(df_ab['order_value'], 99)
p_sd = np.percentile(df_ab['session_duration'], 99)
df_clean = df_ab.loc[(df_ab['order_value'] <= p_ov) & (df_ab['session_duration'] <= p_sd)]

# Run Mann-Whitney U test
x = df_clean[df_clean['group'] == 'Control']['order_value']
y = df_clean[df_clean['group'] == 'Experimental']['order_value']

U1, p_u = mannwhitneyu(x, y, method="auto")

if p_u <= 0.05:
    p_ans = "<="
    null = "yes"
    same_dist = "no"
else:
    p_ans = ">"
    null = "no"
    same_dist = "yes"

answer = f"""Mann-Whitney U test
U1 = {round(float(U1), 3)}, p-value {p_ans} 0.05
Reject null hypothesis: {null}
Distributions are same: {same_dist}
"""

print(answer)

# answer str

#print("""
#Mann-Whitney U test
#U1 = 60612.0, p-value <= 0.05
#Reject null hypothesis: yes
#Distributions are same: no""")