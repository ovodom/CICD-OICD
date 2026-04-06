import json
import boto3
import uuid
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):

    method = event.get("httpMethod")

    # CREATE NOTE
    if method == "POST":
        body = json.loads(event.get("body", "{}"))

        note_id = str(uuid.uuid4())

        table.put_item(Item={
            "id": note_id,
            "title": body.get("title"),
            "content": body.get("content")
        })

        return {
            "statusCode": 201,
            "body": json.dumps({"id": note_id})
        }

    # GET ALL NOTES
    if method == "GET":
        response = table.scan()
        return {
            "statusCode": 200,
            "body": json.dumps(response.get("Items", []))
        }

    # DELETE NOTE (optional path param)
    if method == "DELETE":
        note_id = event.get("pathParameters", {}).get("id")

        if not note_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "missing id"})
            }

        table.delete_item(Key={"id": note_id})

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "deleted"})
        }

    return {
        "statusCode": 400,
        "body": json.dumps({"error": "unsupported method"})
    }