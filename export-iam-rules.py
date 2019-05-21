from google.cloud import asset_v1beta1
from google.cloud.asset_v1beta1.proto import asset_service_pb2
import logging

KEY = "randomkey"
ORGANIZATION_ID = "myorganizationkey"
DESTINATION_PATH = "gs://My-GCS-Bucket/My-Export.json"


def main(request):
	request_json = request.get_json()
	if 'key' not in request.args or request.args.get('key') != KEY:
		return "Unauthorized export"

	client = asset_v1beta1.AssetServiceClient()
	parent = "organizations/"+ORGANIZATION_ID
	output_config = asset_service_pb2.OutputConfig()
	output_config.gcs_destination.uri = DESTINATION_PATH
	response = client.export_assets(parent, output_config,None,None,"IAM_POLICY")
	logging.info(response.result())
	logging.info("isdone:")
	logging.info(response.done())
	logging.info("errors:")
	try:
		logging.info(response.error())
	except:
		logging.info("no errors")
	return "Export request success"
