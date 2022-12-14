import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_session_stats(df: pd.DataFrame) -> None:
    session_data = df.groupby('group', as_index=False)['date'].value_counts()
    session_data = session_data.pivot(index='date', columns='group', values='count')

    session_data.plot(kind='bar', xlabel='April', ylabel='Number of sessions')
    plt.legend(title='Group')


def plot_order_value_distribution(df: pd.DataFrame) -> None:
    pd.DataFrame.hist(df, column='order_value', by='group')


def plot_sessions_duration_distribution(df: pd.DataFrame) -> None:
    pd.DataFrame.hist(df, column='session_duration', by='group')


def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    order_value_threshold = np.percentile(df['order_value'], 99)
    session_duration_threshold = np.percentile(df['session_duration'], 99)
    return df[(df['order_value'] <= order_value_threshold) & (df['session_duration'] <= session_duration_threshold)]


def main():
    df = pd.read_csv('test/ab_test.csv')
    df['date'] = pd.to_datetime(df['date']).dt.day

    plot_session_stats(df)
    plot_order_value_distribution(df)
    plot_sessions_duration_distribution(df)
    plt.show()

    filtered_df = remove_outliers(df)
    print(f'Mean: {filtered_df["order_value"].mean():.2f}')
    print(f'Standard deviation: {filtered_df["order_value"].std(ddof=0):.2f}')
    print(f'Max: {filtered_df["order_value"].max():.2f}')


if __name__ == '__main__':
    main()