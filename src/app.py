import json
import boto3
import os
import uuid

rek_client = boto3.client("rekognition")
s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")


table_name = os.environ["RESULTS_TABLE"]
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    print("Detecting labels on uploaded images ...")
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        unique_id = str(uuid.uuid4())
        
        print(f"A new image has been uploaded: s3://{bucket}/{key}")
        
        # Detect labels using Rekognition
        response = rek_client.detect_labels(
            Image={"S3Object": {"Bucket": bucket, "Name": key}},
            MaxLabels=10,
            MinConfidence=80
        )
        
        labels = response.get("Labels", [])
        
       
        for label in labels:
            item = {
                "ImageID": unique_id,
                "LabelName": label["Name"], 
                "OriginalFilename": key,                          
                "Confidence": str(label["Confidence"]),  
                "Parents": [p["Name"] for p in label.get("Parents", [])],
                "Categories": [c["Name"] for c in label.get("Categories", [])],
                "Aliases": [a["Name"] for a in label.get("Aliases", [])],
            }
            
            
            table.put_item(Item=item)
        
        print(f"Saved {len(labels)} labels for {key} into DynamoDB table {table_name}")
    
    return {"statusCode": 200, "body": "Rekognition analysis completed."}
