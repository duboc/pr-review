#!/bin/bash

PROJECT_ID="your-project-id"

gcloud config set project ${PROJECT_ID}

gcloud services enable \
    orgpolicy.googleapis.com \
    aiplatform.googleapis.com \
    cloudfunctions.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com
