import pandas as pd

# Read a CSV file into a DataFrame
data = pd.read_csv('Pipeline_process1/rep20230915.csv')

# Define a specific date and time range by bellow two lines
# specific_date = pd.to_datetime('2023-10-01 01:00')
# data = data[pd.to_datetime(data['date_time_send']) >= specific_date]

# Convert the 'date_time_send' column to datetime format
data['date_time_send'] = pd.to_datetime(data['date_time_send'])

# Sort the DataFrame by 'task_id' and 'date_time_send' in ascending order
data.sort_values(by=['task_id', 'date_time_send'], ascending=[True, True], inplace=True)

# Calculate the time spent for each task by finding the time difference between consecutive 'date_time_send' values
data['time_spent'] = data.groupby(['task_id'])['date_time_send'].diff()

# Group data by 'code_of_stage' and calculate various statistics on 'time_spent'
stage_stats = data.groupby(['code_of_stage'])['time_spent'].agg(['sum', 'min', 'mean', 'max']).reset_index()

# Group data by 'code_of_stage' and 'next_stage', then count the occurrences of 'next_stage' for each 'code_of_stage'
result = data.groupby('code_of_stage')['next_stage'].value_counts().unstack().fillna(0)

# Reset the index of the 'result' DataFrame
result.reset_index(inplace=True)

# Count the number of occurrences of each 'code_of_stage'
stage_counts = data['code_of_stage'].value_counts().reset_index()
stage_counts.columns = ['code_of_stage', 'iteration_count']

# Merge the 'stage_stats', 'stage_counts', and 'result' DataFrames on 'code_of_stage'
merged_data = pd.merge(stage_stats, stage_counts, on='code_of_stage')
merged_data = pd.merge(merged_data, result, on='code_of_stage')

# Print the final merged DataFrame
print(merged_data)
