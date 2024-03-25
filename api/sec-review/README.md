# Cloud Run Vertex API
This application demonstrates a simple GenAI Diff Sec Review using Cloud Run.

## Steps to deploy
Export your project definitions:
```bash
export MY_PROJECT_ID="your-project-id"
export MY_PROJECT_NO="1234567890"
export MY_LOCATION="us-central1"
``` 

Enable the following APIs: 
```bash
gcloud services enable cloudbuild.googleapis.com \
                       run.googleapis.com \
                       container.googleapis.com \
                       compute.googleapis.com \
                       artifactregistry.googleapis.com \
                       aiplatform.googleapis.com \
                       --project=$MY_PROJECT_ID
```

Create a Docker Repo on Artifact Registry: 
```bash
gcloud artifacts repositories create sec-review-repo \
       --repository-format=docker \
       --location=$MY_LOCATION \
       --description="SecReview Docker Repository"
``` 

Grant IAM permissions:
```bash
gcloud projects add-iam-policy-binding $MY_PROJECT_ID \
       --member="serviceAccount:$MY_PROJECT_NO@cloudbuild.gserviceaccount.com" \
       --role="roles/container.developer" \
       --condition=None

gcloud projects add-iam-policy-binding $MY_PROJECT_ID \
       --member="serviceAccount:$MY_PROJECT_NO@cloudbuild.gserviceaccount.com" \
       --role="roles/iam.serviceAccountUser" \
       --condition=None

gcloud projects add-iam-policy-binding $MY_PROJECT_ID \
       --member="serviceAccount:$MY_PROJECT_NO@cloudbuild.gserviceaccount.com" \
       --role="roles/run.admin" \
       --condition=None	

gcloud projects add-iam-policy-binding $MY_PROJECT_ID \
       --member="serviceAccount:$MY_PROJECT_NO@cloudbuild.gserviceaccount.com" \
       --role="roles/artifactregistry.admin" \
       --condition=None

gcloud projects add-iam-policy-binding $MY_PROJECT_ID \
       --member="serviceAccount:$MY_PROJECT_NO-compute@developer.gserviceaccount.com" \
       --role="roles/aiplatform.user" \
       --condition=None
```

Run cloud build to deploy on Cloud Run:
```bash
gcloud builds submit . --config=./cloudbuild.yaml --substitutions SHORT_SHA=1.0
```