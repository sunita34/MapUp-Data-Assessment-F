import pandas as pd


def generate_car_matrix(df) -> pd.DataFrame:
    """
    Creates a DataFrame for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values,
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    pd.DataFrame(np.fill_diagonal(car_matrix.values, 0), index=car_matrix.index, columns=car_matrix.columns)
    return car_matrix


def get_type_count(df) -> dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'])
    type_count = df['car_type'].value_counts().to_dict()
    return dict(sorted(type_count.items()))


def get_bus_indexes(df) -> list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    mean_bus = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * mean_bus].index.tolist()
    return sorted(bus_indexes)


def filter_routes(df) -> list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    average_truck_by_route = df.groupby('route')['truck'].mean()
    filtered_routes = average_truck_by_route[average_truck_by_route > 7].index.tolist()
    return sorted(filtered_routes)


def multiply_matrix(matrix) -> pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    return modified_matrix.round(1)


def time_check(df) -> pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    df['start_time'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_time'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    df['timestamp'] = df.apply(lambda row: pd.date_range(start=row['start_time'], end=row['end_time'], freq='H'), axis=1)

    completeness_check = df.groupby(['id', 'id_2'])['timestamp'].apply(lambda x: len(x) == 24 * 7).reset_index()
    completeness_check.set_index(['id', 'id_2'], inplace=True)

    return completeness_check['timestamp']
