import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import levene
from scipy.stats import ttest_ind

# Upload and prepare the data
df_ab = pd.read_csv('test/ab_test.csv')
p_ov = np.percentile(df_ab['order_value'], 99)
p_sd = np.percentile(df_ab['session_duration'], 99)
df_clean = df_ab.loc[(df_ab['order_value'] <= p_ov) & (df_ab['session_duration'] <= p_sd)].copy()

# Apply log-transformation
df_clean.loc[:, 'log_order_value'] = [np.log(x) for x in df_clean.loc[:, 'order_value']]

# Plot new variable
df_clean.loc[:, 'log_order_value'].plot.hist(bins=30)
plt.show()

# Run Levene's test for the equality of variances
x = df_clean[df_clean['group'] == 'Control'].loc[:, 'log_order_value']
y = df_clean[df_clean['group'] == 'Experimental'].loc[:, 'log_order_value']

# Run Levene's test for the equality of variances
W, p_levene = levene(x, y)

# Make conclusion about variances and choose t-test type (for equal variances or not)
if p_levene <= 0.05:
    p_levene_answ = "<="
    reject_null_levene = "yes"
    vars_equal = "no"
    t, p_t = ttest_ind(x, y, equal_var=False)
else:
    p_levene_answ = ">"
    reject_null_levene = "no"
    vars_equal = "yes"
    t, p_t = ttest_ind(x, y)

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

#print("""
#Levene's test
#W = 30.174, p-value <= 0.05
#Reject null hypothesis: yes
#Variances are equal: no
#
#T-test
#t = -5.859, p-value <= 0.05
#Reject null hypothesis: yes
#Means are equal: no""")


