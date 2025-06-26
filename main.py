import functions_framework
from google.cloud import storage, pubsub_v1
import fitz  # PyMuPDF
import os

@functions_framework.cloud_event
def pdf_to_text(cloud_event):
    bucket_name = cloud_event.data["bucket"]
    file_name = cloud_event.data["name"]

    if not file_name.endswith(".pdf"):
        return

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    local_path = f"/tmp/{file_name}"
    blob.download_to_filename(local_path)

    doc = fitz.open(local_path)
    text = ""
    for page in doc:
        text += page.get_text()

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(os.environ["GCP_PROJECT"], "pdf-topic")
    publisher.publish(topic_path, text.encode("utf-8"))
