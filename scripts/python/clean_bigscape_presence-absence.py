import pandas as pd

# Read the TSV file into a DataFrame
file_path = './derivedData/multismash_out/bigscape/absence_presence.tsv'
df = pd.read_csv(file_path, sep='\t')

# Extract strain information from contig names
df['Strain'] = df['ACC'].str.split('_').str[0]

# Drop the original ACC column
df.drop(columns=['ACC'], inplace=True)

# Group by strain and sum the values for each gene cluster
grouped_df = df.groupby('Strain').sum().reset_index()

# Remove columns with sum equal to 0
grouped_df = grouped_df.loc[:, (grouped_df != 0).any(axis=0)]

# Remove the header for the 'Strain' column to leave A1 empty
grouped_df.columns = ['' if col == 'Strain' else col for col in grouped_df.columns]

# Save the result to a new TSV file
output_file_path = './derivedData/multismash_out/bigscape/absence_presence_clean.tsv'
grouped_df.to_csv(output_file_path, sep='\t', index=False)