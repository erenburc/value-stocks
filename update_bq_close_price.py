def update_close_price():
    from google.cloud import bigquery

    # Set the path to your service account key file
    service_account_key_file = 'sodium-daylight-375513-120c92fff4f7.json'

    # Create a BigQuery client object
    client = bigquery.Client.from_service_account_json(service_account_key_file)

    # Set the ID of your dataset and table
    dataset_id = 'python_to_bq'
    table_id = 'python_close_price'

    # Set the path to your text file
    file_path = 'close_price.txt'

    # Set the format of your file (e.g. CSV, JSON, etc.)
    file_format = bigquery.SourceFormat.CSV

    # Set any other options as needed (e.g. delimiter, encoding, etc.)
    options = {
        'field_delimiter': '\t'}

    # Load the data into the table
    with open(file_path, 'rb') as file:
        table_ref = client.dataset(dataset_id).table(table_id)
        job_config = bigquery.LoadJobConfig(
            schema=[
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
            ],
            source_format=file_format,
            skip_leading_rows=1,
            field_delimiter="\t",
            write_disposition='WRITE_TRUNCATE',
        )
        job = client.load_table_from_file(file, table_ref, job_config=job_config)
        job.result()  # Wait for the job to complete
