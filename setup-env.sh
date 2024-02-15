#!/bin/bash

PROJECT_ID=$(gcloud config list --format='value(core.project)')                                                                                                      py cli-code-api 11:26:18
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')

gcloud config set project ${PROJECT_ID}

gcloud services enable \
    orgpolicy.googleapis.com \
    aiplatform.googleapis.com \
    cloudfunctions.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    secretmanager.googleapis.com

gcloud secrets create pr-secret-id \
    --replication-policy="automatic"


gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor