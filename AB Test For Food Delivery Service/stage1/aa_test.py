import pandas as pd
from scipy.stats import levene
from scipy.stats import ttest_ind

# Upload data
df_aa = pd.read_csv('test/aa_test.csv')

# Run Levene's test for the equality of variances
W, p_levene = levene(df_aa['Sample 1'], df_aa['Sample 2'])

# Make conclusion about variances and choose t-test type (for equal variances or not)
if p_levene <= 0.05:
    p_levene_answ = "<="
    reject_null_levene = "yes"
    vars_equal = "no"
    t, p_t = ttest_ind(df_aa['Sample 1'], df_aa['Sample 2'], equal_var=False)
else:
    p_levene_answ = ">"
    reject_null_levene = "no"
    vars_equal = "yes"
    t, p_t = ttest_ind(df_aa['Sample 1'], df_aa['Sample 2'])

# Draw conclusion about equality of means
if p_t <= 0.05:
    p_t_answ = "<="
    reject_null_t = "yes"
    means_equal = "no"
else:
    p_t_answ = ">"
    reject_null_t = "no"
    means_equal = "yes"

answer = f"""Levene's test
W = {round(float(W), 3)}, p-value {p_levene_answ} 0.05
Reject null hypothesis: {reject_null_levene}
Variances are equal: {vars_equal}

T-test
t = {round(float(t), 3)}, p-value {p_t_answ} 0.05
Reject null hypothesis: {reject_null_t}
Means are equal: {means_equal}"""

print(answer)

# answer str

#print('''Levene's test
#W = 0.0, p-value > 0.05
#Reject null hypothesis: no
#Variances are equal: yes
#
#T-test
#t = -3.432, p-value <= 0.05
#Reject null hypothesis: yes
#Means are equal: no''')
