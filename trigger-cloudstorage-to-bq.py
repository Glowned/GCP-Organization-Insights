from google.cloud import bigquery

DATASET_ID = 'my_dataset_id'
TARGET_TABLE = 'my_table_id'
def transfer(event, context):
	"""Triggered by a change to a Cloud Storage bucket.
	Args:
		 event (dict): Event payload.
		 context (google.cloud.functions.Context): Metadata for the event.
	"""
	client = bigquery.Client()
	dataset_ref = client.dataset(DATASET_ID)
	file = event
	print(f"Processing file: {file['name']}.")
	
	job_config = bigquery.LoadJobConfig()
	job_config.autodetect = True
	job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
	uri = 'gs://assets-inventory-staging/'+file['name']
	load_job = client.load_table_from_uri(
		uri,
		dataset_ref.table(TARGET_TABLE),
		job_config=job_config)  # API request
	print('Starting job {}'.format(load_job.job_id))

	load_job.result()  # Waits for table load to complete.
	print('Job finished.')

	destination_table = client.get_table(dataset_ref.table(TARGET_TABLE))
	print('Loaded {} rows.'.format(destination_table.num_rows))