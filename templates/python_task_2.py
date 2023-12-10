import pandas as pd
from datetime import time


def calculate_distance_matrix(df):
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    # Example logic: (Replace this with your own logic)
    df_distance = df.copy()  # Assuming df contains columns: 'id_start', 'id_end', 'distance'
    distance_matrix = pd.pivot_table(df_distance, values='distance', index='id_start', columns='id_end', fill_value=0)
    distance_matrix += distance_matrix.T  # Make the matrix symmetric
    distance_matrix.values[[range(len(distance_matrix))] * 2] = 0  # Set diagonal values to 0
    return distance_matrix


def unroll_distance_matrix(df):
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    # Example logic: (Replace this with your own logic)
    unrolled_df = df.melt(id_vars='id_start', var_name='id_end', value_name='distance')
    return unrolled_df


def find_ids_within_ten_percentage_threshold(df, reference_id):
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    # Example logic: (Replace this with your own logic)
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()
    threshold = 0.1 * reference_avg_distance
    result_df = df.groupby('id_start')['distance'].mean().reset_index()
    result_df = result_df[(result_df['distance'] >= (reference_avg_distance - threshold)) &
                          (result_df['distance'] <= (reference_avg_distance + threshold))]
    return result_df


def calculate_toll_rate(df):
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    # Example logic: (Replace this with your own logic)
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    for vehicle_type, rate in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate
    return df


def calculate_time_based_toll_rates(df):
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """

    # Write your logic here
    # Example logic: (Replace this with your own logic)
    def apply_discount(row):
        if row['start_day'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            if time(0, 0, 0) <= row['start_time'] <= time(10, 0, 0):
                return 0.8
            elif time(10, 0, 0) <= row['start_time'] <= time(18, 0, 0):
                return 1.2
            else:
                return 0.8
        else:  # Weekends
            return 0.7

    df['start_day'] = df['start_time'].dt.day_name()
    df['end_day'] = df['end_time'].dt.day_name()
    df['discount_factor'] = df.apply(apply_discount, axis=1)

    for vehicle_type in ['moto', 'car', 'rv', 'bus', 'truck']:
        df[vehicle_type] = df[vehicle_type] * df['discount_factor']

    return df

