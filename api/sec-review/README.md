# Cloud Function Vertex API

This application demonstrates a simple GenAI Security Review using Cloud Function.


## Environment variables required

Insert your Project_ID and execute the following lines.

```bash
export GCP_PROJECT='conventodapenha'  # Change this
export GCP_REGION='us-central1'  
```

Execute the following command to deploy the function

   ```bash
   gcloud functions deploy sec_review \
   --gen2 \
   --runtime=python311 \
   --region=$GCP_REGION \
   --source=. \
   --entry-point=sec_review \
   --trigger-http \
   --set-env-vars=GCP_PROJECT=$GCP_PROJECT,GCP_REGION=$GCP_REGION \
   --memory=512MB
   ```