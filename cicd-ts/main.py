import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
from google.cloud import storage
import base64
import functions_framework
from typing import List
from google.cloud import logging_v2
from datetime import datetime, timedelta
import json

PROJECT_ID = os.environ["PROJECT_ID"]
PROMPT = """You are a senior DevOps Engineer. You will find below a Cloud Build trigger that has failed, as well as the logs. Your job is to explain why it failed. You can also suggest how the issue can be fixed, but your main job is to explain why it failed.
Explain as if you have a Junior Developer in front of you. He can only edit the code he comitted and that caused the failure of the pipeline. Do not advise to modify the trigger or the pipeline. The error comes from the code not passing the pipeline.

Use markdown to format your response.


Cloud Build Trigger:
----
%s
----

Logs:
----
%s
----"""

# Triggered from a message on Cloud Build Pub/Sub 
@functions_framework.cloud_event
def on_message(cloud_event):
    pubsub_message_text = base64.b64decode(cloud_event.data["message"]["data"]).decode("utf-8")
    json_data = json.loads(pubsub_message_text)

    # If the build is not a failure, nothing to do for us
    if json_data["status"] != "FAILURE":
        return

    # Retrieve the build ID from metadata
    build_id = json_data["id"]

    #############
    # Get the logs
    #############

    # Calculate the timestamp an hour ago
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    timestamp_string = one_hour_ago.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Define the filter string
    filter_string = f"""
    log_name="projects/{PROJECT_ID}/logs/cloudbuild"
    timestamp >= "{timestamp_string}"
    resource.labels.build_id="{build_id}"
    -- -(textPayload =~ "\\w{{12}}: (Pulling fs layer|Pull complete|Waiting)")
    """

    # Retrieve the logs (max 1000), and concatenate
    client = logging_v2.services.logging_service_v2.LoggingServiceV2Client()
    request = logging_v2.types.ListLogEntriesRequest(
        resource_names=[f"projects/{PROJECT_ID}"],
        filter=filter_string,
        page_size=1000
    )

    log_entries = client.list_log_entries(request=request).entries
    logs_text = "\n".join([str(log.text_payload) for log in log_entries])

    #################
    # Ask Gemini for help
    #################

    # Initialize the model
    vertexai.init(project=PROJECT_ID, location="us-central1")
    model = GenerativeModel("gemini-pro")

    # Generate the content
    response = model.generate_content(
        PROMPT % (pubsub_message_text, logs_text),
        generation_config={
            "max_output_tokens": 4096,
            "temperature": 0,
            "top_p": 0.5
        },
    )

    #############
    # Save the response
    #############

    # Create the destination blob name and initialize
    destination_blob_name = f"{build_id}.md"
    storage_client = storage.Client()
    bucket = storage_client.bucket(os.environ["BUCKET_NAME"])

    # Update the latest failed build id (could be retrieved otherwise but easier to store along)
    # and upload the response to the bucket
    bucket.blob("latest_build_id.txt").upload_from_string(build_id)
    bucket.blob(destination_blob_name).upload_from_string(response.text)

    # To debug later, also useful to save the prompt
    bucket.blob(f"{build_id}_prompt.txt").upload_from_string(PROMPT % (pubsub_message_text, logs_text))

    
    print(
        f"Generated response uploaded to {destination_blob_name}."
    )

    # Everything good, return 200 OK
    return 