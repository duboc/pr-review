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
    # model = TextGenerationModel.from_pretrained("text-bison")
    
    model = GenerativeModel("gemini-pro")

    prompt = f"""
    Task: Analyze code changes and provide a change management summary.

        Inputs:
            Git Diffs: Showing lines added (+) and removed (-) within the context of the final code.
            Git Commits: Developer-written commit messages.
            Final Code: The complete source code after the changes have been applied.
            This is the provided code: {user_code}
        Output:
            Change Summary: A concise explanation, aimed at a change management audience, focusing on the following:
            High-Level Description: In a few sentences, describe the overall purpose of the code changes.
            Key Changes (Bullet Points):
            Briefly explain each significant new code addition indicated by the Git diffs.
            Relate these changes to the commit messages for context, if helpful.
            Potential Impact: If possible, note any expected impact on functionality, user experience, or system dependencies (this may be speculative based on the provided information).
    Style:
        Professional Tone: Write in a clear, business-oriented style suitable for internal change management documents.
        Focus on New Code: Concentrate on explaining the changes themselves, avoid analyzing the quality of existing code.
"""
    
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