import boto3
import pprint  as pp
from envs import TABLE_NAME

ddb = boto3.client("dynamodb")

def get_events_by_tag(tag):
    response = ddb.query(
        TableName=TABLE_NAME,
        IndexName="GSI-1",
        KeyConditionExpression="#pk = :pk_val",
        ExpressionAttributeNames={
            "#pk": "DataValue",
        },
        ExpressionAttributeValues={
            ":pk_val": {"S": tag},
        }
    )

    return response

print("タグでイベントを検索")
pp.pprint(get_events_by_tag("Tag_#Serverless")["Items"])

def get_event_ids():
    response = ddb.query(
        TableName=TABLE_NAME,
        IndexName="GSI-2",
        KeyConditionExpression="#pk = :pk_val",
        ExpressionAttributeNames={
            "#pk": "DataType",
        },
        ExpressionAttributeValues={
            ":pk_val": {"S": "EventID"},
        }
    )

    return response

print("イベントID一覧")
pp.pprint(get_event_ids()["Items"])

def get_event_by_timestamp(query_timestamp):
    response = ddb.query(
        TableName=TABLE_NAME,
        IndexName="GSI-3",
        KeyConditionExpression="#pk = :pk_val",
        FilterExpression="#starttime <= :querytime AND :querytime <= #endtime",
        ExpressionAttributeNames={
            "#pk": "DataType",
            "#starttime": "StartTime",
            "#endtime": "EndTime"
        },
        ExpressionAttributeValues={
            ":pk_val": {"S": f"TimeRange"},
            ":querytime": {"S": query_timestamp},
        }
    )
    return response

print("タイムスタンプでイベントIDを取得")
pp.pprint(get_event_by_timestamp("2024-03-14 08:00:00")["Items"])
pp.pprint(get_event_by_timestamp("2024-03-14 10:00:00")["Items"])
pp.pprint(get_event_by_timestamp("2024-03-14 13:00:00")["Items"])
