import os
import json
import functions_framework

import google.cloud.logging

import vertexai
from vertexai.language_models import TextGenerationModel
from flask_cors import cross_origin

PROJECT_ID = os.environ.get('GCP_PROJECT', '-')
LOCATION = os.environ.get('GCP_REGION', '-')
client = google.cloud.logging.Client(project=PROJECT_ID)
client.setup_logging()
log_name = "code-cloudfunction-log"
logger = client.logger(log_name)

@cross_origin()
@functions_framework.http
def pr_review(request):
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
    model = TextGenerationModel.from_pretrained("text-bison")
    prompt = f"You're a senior developer tasked with reviewing code. review the following code and report out any findings: {user_code}"
    parameters = {
        "temperature": 1.0,
        "max_output_tokens": 256,
        "top_p": 1.0,
        "top_k": 40
    }
    prompt_response = model.predict(prompt, **parameters)
    logger.log(f"PaLM Text Bison Model response: {prompt_response.text}")

    # Format the response
    data = {}
    data['response'] = []
    data['response'].append({"details": prompt_response.text})
    return json.dumps(data), 200, {'Content-Type': 'application/json'}