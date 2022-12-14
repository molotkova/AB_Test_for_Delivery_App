from statsmodels.stats.power import TTestIndPower
import math
import pandas as pd

# Sample size per group
effect = 0.2
alpha = 0.05
power = 0.8

analysis = TTestIndPower()
n = analysis.solve_power(effect,
                         power=power,
                         nobs1=None,
                         alpha=alpha,
                         ratio=1)

print(f'Sample size: {int(math.ceil(n / 100.0)) * 100}')

# Number of sessions in control and experimental groups
df_ab = pd.read_csv('test/ab_test.csv')
print(f"""\n{df_ab['group'].value_counts().index[0]} group: {df_ab['group'].value_counts().iloc[0]}
{df_ab['group'].value_counts().index[1]} group: {df_ab['group'].value_counts().iloc[1]}""")


# answer str

#print("""Sample size: 400
#
#Control group: 400
#Experimental group: 400""")