import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# ==========================================
# ИСХОДНЫЕ ФУНКЦИИ АНАЛИЗА
# ==========================================

def read_data(data_file: str) -> pd.DataFrame:
    """Загружает CSV-файл в DataFrame pandas."""
    try:
        df = pd.read_csv(data_file, encoding='utf-8', sep=',')
        print(f"Файл {data_file} успешно загружен. Записей: {len(df)}")
        return df
    except Exception as e:
        print(f'Ошибка чтения файла "{data_file}": {e}')
        return None

def get_selected_regions_df(df: pd.DataFrame, selected_regions: list[str]):
    """Фильтрует данные, оставляя только указанные регионы."""
    return df[df['region'].isin(selected_regions)]

def get_limited_df(df: pd.DataFrame, limit: int):
    """Фильтрует данные, оставляя игроков только в пределах указанного рейтинга (Top-N)."""
    return df[df['ranking_position'] <= limit]

def get_total_count_matrix(df: pd.DataFrame):
    """Создает таблицу количества игроков по годам и регионам + общий итог."""
    matrix_df = df.pivot_table(
        index='year',
        columns='region',
        values='player',
        aggfunc='count',
        fill_value=0
    )
    matrix_df = matrix_df.sort_index()
    matrix_df['Total'] = matrix_df.sum(axis=1)
    return matrix_df

def get_percentage_matrix(df: pd.DataFrame):
    """Преобразует абсолютные числа в проценты от общего количества за год."""
    yearly_totals = df['Total']
    percentage_matrix = round(df.div(yearly_totals, axis=0)*100, 2)
    return percentage_matrix

def get_linear_graph(df: pd.DataFrame, limit: str):
    """Строит линейный график изменения доли игроков по регионам во времени."""
    df_plot = df.drop(columns='Total')

    plt.style.use('seaborn-v0_8-whitegrid')

    _, ax = plt.subplots(figsize=(14, 7))
    df_plot.plot(ax=ax, marker='o', markersize=4, linewidth=2)

    ax.set_title(f'Доля игроков по регионам в рейтинге HLTV (Top-{limit}) c 2016 по 2026 год', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Год', fontsize=14, fontweight='bold')
    ax.set_ylabel('Доля игроков (%)', fontsize=14, fontweight='bold')

    ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=1))

    ax.set_ylim(0, df_plot.max().max() * 1.15)
    ax.legend(title='Регион', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=14)
    ax.set_xticks(df_plot.index)
    ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(f'data/player_share_top_{limit}.png', dpi=150, bbox_inches='tight')
    plt.show()

def get_linear_graph_weighted(df_weigted: pd.DataFrame, limit: str):
    """Строит линейный график изменения доли игроков по регионам во времени."""
    plt.style.use('seaborn-v0_8-whitegrid')

    _, ax = plt.subplots(figsize=(14, 7))
    df_weigted.plot(ax=ax, marker='o', markersize=4, linewidth=2)

    ax.set_title(f'Динамика взвешенного рейтинга регионов в рейтинге HLTV (Top-{limit}) c 2016 по 2026 год', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Год', fontsize=14, fontweight='bold')
    ax.set_ylabel('Средний взвешенный рейтинг', fontsize=14, fontweight='bold')

    ax.set_ylim(0, df_weigted.max().max() * 1.15)
    ax.legend(title='Регион', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=14)
    ax.set_xticks(df_weigted.index)
    ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(f'data/linear_weighted_top_{limit}.png', dpi=150, bbox_inches='tight')
    plt.show()

def get_average_matrix(df: pd.DataFrame):
    """Считает среднюю позицию в рейтинге для каждого региона по годам."""
    matrix_df = df.pivot_table(
        index='year', columns='region', values='ranking_position', aggfunc='mean', fill_value=pd.NA
    ).round(2)
    return matrix_df.sort_index()

def get_median_matrix(df: pd.DataFrame):
    """Считает медианную позицию в рейтинге для каждого региона по годам."""
    matrix_df = df.pivot_table(
        index='year', columns='region', values='ranking_position', aggfunc='median', fill_value=pd.NA
    )
    return matrix_df.sort_index()

def get_weighted_matrix(df: pd.DataFrame, limit: int):
    """Рассчитывает взвешенный рейтинг (чем выше место, тем больше вес)."""
    df = df.copy()
    df['weighted_ranking'] = limit + 1 - df['ranking_position']
    matrix_df = df.pivot_table(
        index='year', columns='region', values='weighted_ranking', aggfunc='mean', fill_value=0
    ).round(2)
    return matrix_df.sort_index()

def get_pearson(df_total: pd.DataFrame, df_weighted: pd.DataFrame):
    """Вычисляет корреляцию Пирсона между количеством игроков и их взвешенным рейтингом."""
    return df_total.corrwith(df_weighted, axis=1, method='pearson')

def get_spearman(df_total: pd.DataFrame, df_weighted: pd.DataFrame):
    """Вычисляет корреляцию Спирмена между количеством игроков и их взвешенным рейтингом."""
    return df_total.corrwith(df_weighted, axis=1, method='spearman')

def get_divided_matrix(df_10: pd.DataFrame, df_200: pd.DataFrame):
    """Сравнивает долю игроков в Top-10 относительно Top-200."""
    return round(df_10.div(df_200), 4)

def get_average_by_years(df: pd.DataFrame):
    """Усредняет значения матрицы по всем годам для получения общей статистики по регионам."""
    return df.mean(axis=0).round(2)

def get_pie_chart(df: pd.DataFrame, limit: int):
    """Строит круговую диаграмму средней доли регионов за все годы."""
    plt.figure(figsize=(8, 8))
    plt.pie(df, labels=df.index, autopct='%1.1f%%', startangle=140)
    plt.title(f'Средняя доля игроков по регионам в топ-{limit} (за все годы)', fontweight='bold')
    plt.legend(title="Регионы", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.tight_layout()
    plt.savefig(f'data/avg_share_pie_chart_top_{limit}.png', dpi=150, bbox_inches='tight')
    plt.show()

def get_bar_chart(df: pd.DataFrame, limit: int):
    """Строит столбчатую диаграмму среднего взвешенного рейтинга регионов."""
    _, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(df.index, df.values)

    ax.set_title(f'Средний взвешенный рейтинг регионов за 2016-2026 год (Top-{limit})', fontweight='bold', pad=20)
    ax.set_xlabel('Регион', fontweight='bold')
    ax.set_ylabel('Взвешенный рейтинг', fontweight='bold')

    plt.xticks(rotation=45, ha='right')
    plt.bar_label(bars, padding=3, fmt='%.2f')
    plt.tight_layout()
    plt.savefig(f'data/avg_weighted_ranking_top_{limit}.png', dpi=150, bbox_inches='tight')
    plt.show()

def get_plot_elite_heatmap(coefficient_matrix):
    """Строит тепловую карту коэффициента концентрации элиты (Top-10/Top-200)."""
    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(coefficient_matrix, annot=True, fmt='.4f', cmap='RdBu_r',
                     center=0.05, linewidths=0.5,
                     cbar_kws={'label': 'Коэффициент (Top-10/Top-200)'})
    
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    
    ax.set_title('Концентрация игроков в элите по регионам (Top-10 / Top-200)', 
                 fontweight='bold', fontsize=14)
    ax.set_ylabel('Год', fontweight='bold')
    ax.set_xlabel('Регион', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('data/elite_concentration_heatmap.png', dpi=150, bbox_inches='tight')
    plt.show()


def get_valid_limit():
    """Запрашивает у пользователя корректное значение лимита рейтинга (10, 50, 100 или 200)."""
    while True:
        limit = input("Введите лимит рейтинга (10, 50, 100 или 200): ").strip()
        if limit in ['10', '50', '100', '200']:
            return int(limit)
        print("Неверный ввод. Пожалуйста, введите 10, 50, 100 или 200.")

def run_full_analysis(df: pd.DataFrame, regions: list):
    """Запускает полный текстовый анализ (корреляции и средние веса)."""
    limit = get_valid_limit()
    
    print(f"\n--- Анализ для TOP-{limit} ---")
    df_selected = get_selected_regions_df(df, regions)
    df_limited = get_limited_df(df_selected, limit)

    total_count = get_total_count_matrix(df_limited)
    weighted_matrix = get_weighted_matrix(df_limited, limit)
    pearson = get_pearson(total_count.drop(columns='Total'), weighted_matrix)
    spearman = get_spearman(total_count.drop(columns='Total'), weighted_matrix)
    avg_weighted = get_average_by_years(weighted_matrix)

    print("\nКорреляция Пирсона (Количество игроков vs Взвешенный рейтинг):")
    print(pearson.to_string())

    print("\nКорреляция Спирмена (Количество игроков vs Взвешенный рейтинг):")
    print(spearman.to_string())

    print("\nСредний взвешенный рейтинг по регионам (за все годы):")
    print(avg_weighted.to_string())

def visualize_and_save(df: pd.DataFrame, regions: list, limit: int):
    print(f"\n--- Построение графиков для TOP-{limit} ---")
    df_selected = get_selected_regions_df(df, regions)
    df_limited = get_limited_df(df_selected, limit)

    print("Строится линейный график долей...")
    percentage = get_percentage_matrix(get_total_count_matrix(df_limited))
    get_linear_graph(percentage, limit)

    print("Строится круговая диаграмма...")
    avg_share = get_average_by_years(percentage.drop(columns='Total'))
    get_pie_chart(avg_share, limit)

    print("Строится столбчатая диаграмма взвешенного рейтинга...")
    weighted_matrix = get_weighted_matrix(df_limited, limit)
    avg_weighted = get_average_by_years(weighted_matrix)
    get_bar_chart(avg_weighted, limit)    

def run_visualizations(df: pd.DataFrame, regions: list):
    """Генерирует и сохраняет все графики."""
    limit = get_valid_limit()
    visualize_and_save(df, regions, limit)
    print("Все графики сохранены в папку 'data/' и отображены.")

def run_visualizations_all_limits(df: pd.DataFrame, regions: list):
    """Генерирует и сохраняет все графики для всех лимитов."""
    for limit in [10, 50, 100, 200]:
        visualize_and_save(df, regions, limit)
    print("Все графики сохранены в папку 'data/' и отображены.")

def run_divided_analysis(df: pd.DataFrame, regions: list):
    """Запускает сравнение концентрации лидеров (Top-10 vs Top-200)."""
    print("\n--- Сравнение доли игроков: Top-10 vs Top-200 ---")
    df_selected = get_selected_regions_df(df, regions)
    df_10 = get_total_count_matrix(get_limited_df(df_selected, 10)).drop(columns='Total')
    df_200 = get_total_count_matrix(get_limited_df(df_selected, 200)).drop(columns='Total')

    divided_matrix = get_divided_matrix(df_10, df_200)
    print("\nКоэффициент (Количество в Top-10 / Количество в Top-200) по годам:")
    print("Значение > 0.05 означает, что регион хорошо представлен в самой элите.")
    print(divided_matrix.to_string())

    get_plot_elite_heatmap(divided_matrix)

def view_matrices(df: pd.DataFrame, regions: list):
    """Позволяет пользователю выбрать и просмотреть конкретную матрицу данных в консоли."""
    limit = get_valid_limit()
    print("\nВыберите тип матрицы для просмотра:")
    print("1. Общее количество игроков")
    print("2. Средняя позиция в рейтинге")
    print("3. Медианная позиция в рейтинге")
    print("4. Взвешенный рейтинг")
    choice = input("Ваш выбор (1-4): ").strip()

    df_selected = get_selected_regions_df(df, regions)
    df_limited = get_limited_df(df_selected, limit)

    print(f"\n--- Матрица для TOP-{limit} ---")
    if choice == '1':
        print(get_total_count_matrix(df_limited).to_string())
    elif choice == '2':
        print(get_average_matrix(df_limited).to_string())
    elif choice == '3':
        print(get_median_matrix(df_limited).to_string())
    elif choice == '4':
        weighted_matrix = get_weighted_matrix(df_limited, limit) 
        print(weighted_matrix.to_string())
        get_linear_graph_weighted(weighted_matrix, limit) # строит диагрмму динамики средневзвешенного рейтинга
    else:
        print("Неверный выбор.")

def main():
    """Главная функция, содержащая меню программы и цикл выполнения."""
    # Создаем папку для сохранения графиков, если её нет
    os.makedirs('data', exist_ok=True)
    data_file = 'data/parsed-data.csv'
    df = read_data(data_file)

    if df is None:
        print("Программа завершена из-за ошибки загрузки данных.")
        return

    # Настройки отображения pandas для красивого вывода в консоль
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)

    # Настройка диаграмм
    plt.rc('font', size=14)

    selected_regions = ['Asia', 'CIS', 'Europe', 'South America', 'North America']

    while True:
        print("\n" + "= "*60)
        print("АНАЛИЗ РЕЙТИНГА ИГРОКОВ HLTV (2016–2026)")
        print("= "*60)
        print("1. Полный текстовый анализ (для конкретного лимита рейтинга)")
        print("2. Построение и сохранение всех графиков (для конкретного лимита рейтинга)")
        print("3. Построение и сохранение всех графиков")
        print("4. Сравнение концентрации лидеров: Top-10 vs Top-200")
        print("5. Вычисление метрик, просмотр матриц")
        print("0. Выход из программы")
        print("= "*60)
        
        choice = input("Выберите действие (0-5): ").strip()
        
        if choice == '0':
            print("Завершение работы программы.")
            break
        elif choice == '1':
            run_full_analysis(df, selected_regions)
        elif choice == '2':
            run_visualizations(df, selected_regions)
        elif choice == '3':
            run_visualizations_all_limits(df, selected_regions)
        elif choice == '4':
            run_divided_analysis(df, selected_regions)
        elif choice == '5':
            view_matrices(df, selected_regions)
        else:
            print("Неверный ввод. Пожалуйста, выберите число от 0 до 5.")
            
        input("\nНажмите Enter, чтобы продолжить...")

if __name__ == "__main__":
    main()