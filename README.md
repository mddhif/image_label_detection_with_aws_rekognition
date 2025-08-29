# 📸 Image Label Detection with AWS Rekognition + DynamoDB

This project provides an AWS Lambda function that automatically analyzes images uploaded to an S3 bucket using **Amazon Rekognition**, and stores the detected labels into a **DynamoDB table**.

It is built with the **AWS Serverless Application Model (SAM)**.

---

## 🚀 Features
- Triggered when a new image is uploaded to an S3 bucket
- Uses **Amazon Rekognition** to detect labels (objects, scenes, concepts)
- Stores results in **Amazon DynamoDB**
- Each image is assigned a **unique UUID** to avoid filename collisions
- Captures additional metadata: confidence score, parent labels, categories, and aliases

---

## 📂 Project Structure
```
.
├── src/
│   └── app.py            # Lambda function (Python 3.13)
├── template.yaml         # SAM template
├── README.md             # This file
├── env.json              # (Optional) Local environment variables for testing
└── events/
    └── s3-event.json     # Sample S3 event for local testing
```

---

## ⚙️ Prerequisites
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) configured with credentials
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- Python **3.12+** (recommended: **3.13**)
- An existing DynamoDB table (or create one via CloudFormation/SAM)

---

## 🔧 Environment Variables
The Lambda expects one environment variable:

- `RESULTS_TABLE` → Name of the DynamoDB table where results will be stored.

When deployed via SAM, this is set automatically in **template.yaml** (via a parameter).  
When testing locally, you can provide it via `env.json`:

```json
{
  "Function": {
    "RESULTS_TABLE": "ResultsTable"
  }
}
```

> Note: `"Function"` should match the Logical ID of your Lambda in `template.yaml`.

---

## 📦 Deployment

### 1) Build
```bash
sam build
```

### 2) Deploy (guided)
```bash
sam deploy --guided
```

You will be asked for:
- **Stack name**
- **S3 bucket** for deployment artifacts
- **Parameter**: `ResultsTable` (the name of your existing DynamoDB table)

> Non-guided example:
```bash
sam deploy \
  --stack-name rekognition-app \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides ResultsTable=YourDynamoDBTableName
```

---

## 🧪 Local Testing

### Invoke locally with a sample S3 event
```bash
sam local invoke Function --event events/s3-event.json --env-vars env.json
```

### Example event (`events/s3-event.json`)
```json
{
  "Records": [
    {
      "s3": {
        "bucket": { "name": "my-upload-bucket" },
        "object": { "key": "test-image.jpg" }
      }
    }
  ]
}
```

---

## 📊 DynamoDB Schema

The Lambda stores one item per detected label with the following attributes:

- **ImageID** (string, UUID) → Partition key  
- **LabelName** (string) → Detected label (e.g., "Car", "Tree")  
- **OriginalFilename** (string) → Original image filename  
- **Confidence** (string) → Rekognition confidence score  
- **Parents** (list) → Parent label names  
- **Categories** (list) → Category names  
- **Aliases** (list) → Label aliases  

---

## ✅ Example Output

For an uploaded image `dog.jpg`, DynamoDB might contain:

```json
{
  "ImageID": "550e8400-e29b-41d4-a716-446655440000",
  "LabelName": "Dog",
  "OriginalFilename": "dog.jpg",
  "Confidence": "99.12",
  "Parents": ["Animal", "Pet"],
  "Categories": ["Mammal"],
  "Aliases": ["Canine"]
}
```

---

## 📜 License
MIT License
