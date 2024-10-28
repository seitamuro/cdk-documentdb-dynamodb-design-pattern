import boto3
import pprint as pp
import time
from envs import TABLE_NAME

ddb_client = boto3.client("dynamodb")

def get_gsi_status(gsi_name):
    response = ddb_client.describe_table(TableName=TABLE_NAME)
    if "GlobalSecondaryIndexes" not in response["Table"]: return None
    gsi_status = None
    for gsi in response['Table']['GlobalSecondaryIndexes']:
        if gsi['IndexName'] == gsi_name:
            gsi_status = gsi['IndexStatus']
            break
    return gsi_status

def wait_gsi_creating(gsi_name):
    print(f"{gsi_name} is still in progress.", end="")
    while True:
        if get_gsi_status(gsi_name) == "ACTIVE":
            print(f"\n{gsi_name} is now active")
            break
        else:
            print(f".", end="", flush=True)
            time.sleep(5)

def wait_gsi_deleting(gsi_name):
    print(f"{gsi_name} is still in progress.", end="")
    while True:
        if get_gsi_status(gsi_name) is None:
            print(f"\n{gsi_name} is now deleted")
            break
        else:
            print(f".", end="", flush=True)

            time.sleep(5)