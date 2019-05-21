from google.oauth2 import service_account
from google.cloud import storage
import time
import json
import logging
import datetime
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


import pprint

STAGING_BUCKET = "gs://staging-bucket"
BUCKET_NAME = "staging-bucket"
KEY = "randomkey"

def gcs_upload_blob(content):
	storage_client = storage.Client() # From default credentials
	"""storage_client = storage.Client.from_service_account_json(
			'/var/go/gcp-admin-tools-k68h-211ae287b91b.json')"""
	bucket = storage_client.get_bucket(BUCKET_NAME)
	blob = bucket.blob("export.json")

	blob.upload_from_string(content,'application/json')

	print("File has been generated and uploaded to "+BUCKET_NAME+ " bucket")
	return True


def listProjects():
	credentials = GoogleCredentials.get_application_default()

	"""credentials = service_account.Credentials.from_service_account_file(
		filename="/var/go/gcp-admin-tools-k68h-211ae287b91b.json",
		scopes=['https://www.googleapis.com/auth/cloud-platform'])"""


	#Build the service cloudresourcemanager from the SDK.
	service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials,cache_discovery=False)
	#Our project list
	projectlist = []
	try:
		request = service.projects().list()
	except Exception as e:
		logging.critical("Project list API Call failed "+e.message)
	while True:
		response = request.execute()
	   
		for project in response.get('projects', []):
			projectRow = {"CreateTime":project["createTime"],"Active":project["lifecycleState"],"Name":project["name"],"ID": project["projectId"],"Number":project["projectNumber"],"Parent":project["parent"]["id"]}
			projectlist.append(projectRow)

		#If this page is the last, then finish the execution
		if response.get('nextPageToken') is None:
			break
		else:
			request = service.projects().list_next(previous_request=request, previous_response=response)

	if gcs_upload_blob('\n'.join(json.dumps(obj) for obj in projectlist)):
		return True


def main(request):
	if 'key' not in request.args or request.args.get('key') != KEY:
		return "Unauthorized export"
	else:
		#Only write Critical errors to logs. Otherwise, a lot of useless info are written.
		logging.getLogger('googleapiclient.discovery').setLevel(logging.CRITICAL)
		if listProjects():
			return "Export request success"
	