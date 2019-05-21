from google.cloud import asset_v1beta1
from google.cloud.asset_v1beta1.proto import asset_service_pb2

KEY = "randomkey"
ORGANIZATION_ID = "myorganizationkey"
DESTINATION_PATH = "gs://My-GCS-Bucket/My-Export.json"

def main(request):
	request_json = request.get_json()
	if 'key' not in request.args or request.args.get('key') != KEY:
		return "Unauthorized export"
	if request.args and 'fileName' in request.args:
		project_id=request.args.get('fileName')
		dump_file_path=DESTINATION_PATH
		client = asset_v1beta1.AssetServiceClient()
		parent = "organizations/"+ORGANIZATION_ID
		output_config = asset_service_pb2.OutputConfig()
		output_config.gcs_destination.uri = dump_file_path
		response = client.export_assets(parent, output_config)
		return "Export requestsuccess"
	else:
		raise ValueError("Please specify a fileName")
