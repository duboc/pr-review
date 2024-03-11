import os
import json
import functions_framework

import google.cloud.logging

import vertexai
from vertexai.language_models import TextGenerationModel
from flask_cors import cross_origin
from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_

PROJECT_ID = os.environ.get('GCP_PROJECT', '-')
LOCATION = os.environ.get('GCP_REGION', '-')
client = google.cloud.logging.Client(project=PROJECT_ID)
client.setup_logging()
log_name = "code-cloudfunction-log"
logger = client.logger(log_name)

@cross_origin()
@functions_framework.http
def diff_review(request):
    logger.log(f"Received a request for code review")

    # Parse the request body
    request_json = request.get_json(silent=True)

    # Extract the word from the request body
    if request_json and 'code' in request_json:
        user_code = request_json['code']
        logger.log(f"Received code from user: {user_code}")
    else:
        user_code = "NO SOURCE PROVIDED"
        logger.log(user_code)

    vertexai.init(project=PROJECT_ID, location=LOCATION)
    # model = TextGenerationModel.from_pretrained("text-bison")
    
    model = GenerativeModel("gemini-pro")

    prompt = f"""
    Task: Analyze code changes and provide a change management summary.

        Inputs:
            Code: {user_code}
        Output expected:
            If changes are found:
                Change Summary: A concise explanation, aimed at a change management audience, focusing on the following:
                High-Level Description: In a few sentences, describe the overall purpose of the code changes.
                Key Changes (Bullet Points):
                Briefly explain each significant new code addition indicated by the Git diffs.
                Relate these changes to the commit messages for context, if helpful.
            If no changes are found: Output "No changes are found."""
    
    prompt_response = model.generate_content(prompt,
        generation_config={
            "max_output_tokens": 4096,
            "temperature": 0,
            "top_p": 0.5
        },
    )

    # parameters = {
    #     "temperature": 1.0,
    #     "max_output_tokens": 256,
    #     "top_p": 1.0,
    #     "top_k": 40
    # }
    # prompt_response = model.predict(prompt, **parameters)
    
    logger.log(f"Gemini Model response: {prompt_response.text}")

    # Format the response
    data = {}
    data['response'] = []
    data['response'].append({"details": prompt_response.text})
    return json.dumps(data), 200, {'Content-Type': 'application/json'}