import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import scipy as stats

def read_data(data_file: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(data_file, encoding='utf-8', sep=',')
        print(f"File {data_file} was read: {len(df)}")  
        return df
    except Exception as e:
        print(f'Failed to read file "{data_file}": {e}')
        return

def get_selected_regions_df(df: pd.DataFrame, selected_regions: list[str]):
    return df[df['region'].isin(selected_regions)]

def get_limited_df(df: pd.DataFrame, limit: int):
    return df[df['ranking_position'] <= limit]

def get_total_count_matrix(df: pd.DataFrame):
    
    matrix_df = df.pivot_table(
        index='year',         
        columns='region',      
        values='player',    
        aggfunc='count',       
        fill_value=0           
    )

    matrix_df = matrix_df.sort_index()
    matrix_df['Total'] = matrix_df.sum(axis=1)
    
    # group = df.groupby(['region'])['nickname']
    # agg_df = group.agg(total_players = 'count')

    return matrix_df

def get_percentage_matrix(df: pd.DataFrame):
    
    yearly_totals = df['Total']
    percentage_matrix = round(df.div(yearly_totals, axis=0)*100,2)
    
    return percentage_matrix

def get_linear_graph(df: pd.DataFrame, limit: str):
    df = df.drop(columns='Total')
    
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(14, 7))

    # Построение графика
    df.plot(ax=ax, marker='o', markersize=4, linewidth=2)

    # Оформление осей и заголовка
    ax.set_title(f'Доля игроков по регионам в рейтинге HLTV (Top-{limit}) c 2016 по 2026 год', fontsize=16, fontweight='bold')
    ax.set_xlabel('Год', fontsize=12)
    ax.set_ylabel('Доля игроков (%)', fontsize=12)

    # Форматирование оси Y: добавляем знак % к значениям
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=1))
    ax.set_ylim(0, df.max().max() * 1.15)  # Запас сверху для легенды

    # Легенда справа от графика, чтобы не перекрывать линии
    ax.legend(title='Регион', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10)

    # Подписи всех годов на оси X (чтобы не пропускались)
    ax.set_xticks(df.index)
    ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(f'data/player_share_top_{limit}.png', dpi=150, bbox_inches='tight')
    plt.show()

def get_average_matrix(df: pd.DataFrame):
    matrix_df = df.pivot_table(
        index='year',         
        columns='region',      
        values='ranking_position',    
        aggfunc='mean',       
        fill_value=0           
    ).round(2)
    
    matrix_df = matrix_df.sort_index()
    return matrix_df

def get_median_matrix(df: pd.DataFrame):
    matrix_df = df.pivot_table(
        index='year',         
        columns='region',      
        values='ranking_position',    
        aggfunc='median',       
        fill_value=0           
    )
    
    matrix_df = matrix_df.sort_index()
    return matrix_df

def get_weighted_matrix(df: pd.DataFrame, limit: int):
    df['weighted_ranking'] = limit + 1 - df['ranking_position']

    matrix_df = df.pivot_table(
        index='year',         
        columns='region',      
        values='weighted_ranking',    
        aggfunc='mean',       
        fill_value=0           
    )   
    
    matrix_df = matrix_df.sort_index()
    return matrix_df

def get_pearson(df_total: pd.DataFrame, df_weighted: pd.DataFrame):
    return df_total.corrwith(df_weighted, axis=1, method='pearson')

def get_divided_matrix(df_10: pd.DataFrame, df_200: pd.DataFrame):
    return df_10.div(df_200)    

def get_average_by_years(df: pd.DataFrame):
    new_df = df.mean(axis=0)
    return new_df

def get_pie_chart(df: pd.DataFrame, limit: int):
    plt.figure(figsize=(8, 8))
    plt.pie(df, labels=df.index, autopct='%1.1f%%', startangle=140)
    plt.title(f'Средняя доля игроков по регионам в топ-{limit}')
    plt.legend(title="Регионы", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.tight_layout()
    plt.savefig(f'data/avg_share_pie_chart_top_{limit}.png')
    plt.show()

def get_scatter_plot(df: pd.DataFrame, limit: int):
    pass

def get_bar_chart(df: pd.DataFrame, limit: int):
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(df.index, df.values)

    ax.set_title(f'Средний взвешенный рейтинг регионов за 2016-2026 год (Top-{limit})')
    ax.set_xlabel('Регион')
    ax.set_ylabel('Взвешенный рейтинг')
    plt.xticks(rotation=45, ha='right')
    plt.bar_label(bars, padding=3)
    plt.tight_layout()
    plt.savefig(f'data/avg_weighted_ranking_top_{limit}.png')
    plt.show()
    

data_file = 'data/parsed-data.csv'
df = read_data(data_file)

if df is not None:
    for i in [10,50,100,200]:
        print(f'TOP-{i}')
        df_selected = get_selected_regions_df(df, selected_regions=['Asia', 'CIS', 'Europe', 'South America', 'North America'])
        df_limited = get_limited_df(df_selected, i)
        total_count = get_total_count_matrix(df_limited)
        weighted_matrix = get_weighted_matrix(df_limited, i)
        pearson = get_pearson(total_count, weighted_matrix)
        average_by_years_weighted = get_average_by_years(weighted_matrix)
        # get_pie_chart(average_by_years, i)
        # print(average_by_years_weighted)
        # print(weighted_matrix)
        print(pearson)
        # get_bar_chart(average_by_years_weighted, i)
        # percentage = get_percentage_matrix(total_count)
        # get_linear_graph(percentage, i)
        # mean_ranking = get_average_matrix(df_limited)
        # median_ranking = get_median_matrix(df_limited)
        
        # print(mean_ranking)
        # print(median_ranking)
        # print('----------------------')

divided_matrix = get_divided_matrix(get_total_count_matrix(get_limited_df(df_selected, 10)), get_total_count_matrix(get_limited_df(df_selected, 200)))
# print(divided_matrix)