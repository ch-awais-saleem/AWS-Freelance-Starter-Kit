# AWS Freelance Starter Kit

This repository is a starter kit designed for freelance cloud data engineers and developers. It includes sample AWS Glue jobs, Lambda functions, reporting templates, and deployment-ready scripts that you can reuse and customize for client projects.

---

## 🧰 Features

- 🔄 Convert JSON files in S3 to CSV using AWS Glue
- 🚀 Trigger Glue jobs automatically on S3 upload via Lambda
- 🔔 Send notifications with SNS when new files are uploaded
- 📊 Query ETL logs via Athena and generate daily summaries
- 📁 Clean and well-structured folder hierarchy for quick deployment

---

## 📂 Folder Structure

```
aws-freelance-starter-kit/
│
├── glue_jobs/
│   └── json_to_csv.py                 # Glue script to convert JSON to CSV
│
├── lambda_templates/
│   ├── s3_trigger_to_glue.py          # Trigger Glue job when file is uploaded
│   └── send_sns_on_upload.py          # Notify via SNS when new file is added
│
├── reports/
│   ├── daily_file_count.sql           # Athena query: files processed per day
│   └── daily_summary_lambda.py        # Lambda: summarize today's ETL activity
│
├── cloudformation/
│   └── deploy_stack.yaml              # Full stack template to provision S3, Lambda, Glue, SNS
│
└── README.md                          # Project overview and setup guide
```

---

## 🚀 Getting Started

1. **Clone this repo**
```bash
git clone https://github.com/your-username/aws-freelance-starter-kit.git
cd aws-freelance-starter-kit
```

2. **Deploy Full Stack with CloudFormation**
```bash
aws cloudformation deploy \
  --template-file cloudformation/deploy_stack.yaml \
  --stack-name freelance-etl-pipeline \
  --capabilities CAPABILITY_NAMED_IAM
```
- This provisions:
  - S3 buckets
  - Glue Job
  - Lambda functions
  - SNS Topic
  - IAM roles

3. **Manual Edits** (optional)
- Add your own Glue script paths
- Update Lambda handler references in the template

4. **Athena Setup**
- Run queries in `reports/` folder
- Use with QuickSight or Power BI for visuals

---

## 🧠 Use Cases

✅ Freelancers automating file processing pipelines  
✅ Clients needing instant insights into uploaded data  
✅ Building proof-of-concepts or client demos quickly  
✅ Lightweight ETL automation without big data overhead

---

## 📌 Coming Soon

- S3 ZIP to CSV loader (public bucket support)
- Surrogate key generator tool
- Client onboarding Notion template
- Resume builder using S3 + CloudFront
- Glue job health dashboard using CloudWatch

---

## 🤝 Contributing
Want to contribute templates, use cases, or ideas? Feel free to open a PR or drop a suggestion!

---

## 📬 Contact
Made by a data engineer helping others build smarter with AWS ☁️  
Feel free to reach out if you're mentoring, hiring, or collaborating.

---

> "Helping others do good with their lives starts with building tools that remove friction, spark insight, and invite growth."

---
