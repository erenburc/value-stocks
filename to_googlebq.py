from google.cloud import bigquery

# Set the path to your service account key file
service_account_key_file = 'sodium-daylight-375513-120c92fff4f7.json'

# Create a BigQuery client object
client = bigquery.Client.from_service_account_json(service_account_key_file)

# Set the ID of your dataset
dataset_id = 'python_to_bq'

# Create the dataset object
dataset = bigquery.Dataset(client.dataset(dataset_id))

# Create the dataset in BigQuery
dataset = client.create_dataset(dataset)

# Set the ID of your table
table_id = 'python_close_price'

# Define the schema of the table
schema = [
    bigquery.SchemaField('Date', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('Open', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('High', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('Low', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('Close', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('Volume', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('Dividends', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('Stock Splits', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('Ticker', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('Adj Close', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('Capital Gains', 'STRING', mode='NULLABLE')

    
    	
]

# Create the table object
table = bigquery.Table(dataset.table(table_id), schema=schema)

# Create the table in BigQuery
table = client.create_table(table)

# Set the path to your text file
file_path = 'close_price.txt'

# Set the format of your file (e.g. CSV, JSON, etc.)
file_format = bigquery.SourceFormat.CSV

# Set any other options as needed (e.g. delimiter, encoding, etc.)
options = {
    'field_delimiter': '\t'}

# Load the data into the table
with open(file_path, 'rb') as file:
    job = client.load_table_from_file(file, table, job_config=bigquery.LoadJobConfig(source_format=file_format, **options))

job.result()  # Wait for the job to complete
