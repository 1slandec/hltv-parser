import pandas as pd

def read_data(data_file: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(data_file, encoding='utf-8', sep=',')
        print(f"File {data_file} was read: {len(df)}")  
        return df
    except Exception as e:
        print(f'Failed to read file "{data_file}": {e}')
        return


def analyse(df: pd.DataFrame):
    matrix_df = df.pivot_table(
        index='year',         
        columns='region',      
        values='nickname',    
        aggfunc='count',       
        fill_value=0           
    )

    matrix_df = matrix_df.sort_index()
    matrix_df['Total'] = matrix_df.sum(axis=1)
    
    # group = df.groupby(['region'])['nickname']
    # agg_df = group.agg(total_players = 'count')

    print(matrix_df)


data_file = 'data/parsed-data.csv'
df = read_data(data_file)
if df is not None:
    analyse(df)
