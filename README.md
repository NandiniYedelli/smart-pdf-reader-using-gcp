# 📄 Smart PDF Reader using Google Cloud Platform (GCP)

This project is a serverless Smart PDF Reader built using GCP's free tier services. 
It automatically extracts text from uploaded PDFs, detects the language, summarizes the content, and stores the output in a public Cloud Storage bucket.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🧠 Features

- 🚀 Auto-triggered via PDF upload to Cloud Storage
- 🧾 Text extraction using PyMuPDF
- 🌐 Detects language using langdetect
- 📝 Summarizes using Sumy
- ☁️ All components run in the cloud (serverless)
- 🔓 Public bucket for easy access to processed data
- ✅ Built using **only free-tier GCP services**

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🌐 Project Architecture
PDF Upload (GCS Bucket)
│
▼
Cloud Function (Trigger on PDF Upload)
│
▼
Text Extraction (PyMuPDF) ➜ Publish to Pub/Sub
│
▼
Dataflow Pipeline (Apache Beam)
├─ Language Detection (langdetect)
├─ Summarization (Sumy)
└─ Store Outputs (GCS as JSON)

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

📁 Folder Structure

smart-pdf-reader/
├── main_function/
│ ├── main.py # Cloud Function
│ ├── requirements.txt
├── dataflow/
│ ├── pipeline.py # Dataflow Pipeline
│ ├── requirements.txt
├── test_files/
│ └── GIT_AWS_GCP_Handout.pdf
├── README.md

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------


✅ Setup Instructions

🔹 1. Create & Make Cloud Storage Bucket Public
        gsutil mb -l us-central1 gs://smart-pdf-nandini
        gsutil iam ch allUsers:objectViewer gs://smart-pdf-nandini

🔹 2. Create Pub/Sub Topic and Subscription
        gcloud pubsub topics create pdf-topic
        gcloud pubsub subscriptions create pdf-topic-sub --topic=pdf-topic

🔹 3. Deploy Cloud Function
        cd main_function
        gcloud functions deploy pdf-to-text-function \
            --entry-point pdf_to_text \
            --runtime python310 \
            --trigger-resource smart-pdf-nandini \
            --trigger-event google.storage.object.finalize \
            --region us-central1 \
            --set-env-vars GCP_PROJECT=$(gcloud config get-value project) \
            --allow-unauthenticated
            
🔹 4. Upload a PDF File
        gsutil cp test_files/GIT_AWS_GCP_Handout.pdf gs://smart-pdf-nandini

🔹 5. Run Dataflow Locally (or on GCP)
        cd dataflow
        python3 pipeline.py

📦 Output Files
Check the output in your public bucket:
        gsutil ls gs://smart-pdf-nandini/output/

------------------xxxxxxxx------------------------------xxxxxx----------------------------------xxxxxx--------------------------xxxxx------------------------------------
