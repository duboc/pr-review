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
    
    model = GenerativeModel("gemini-1.0-pro-001")

    prompt = f"""
    Task: Perform automated code review to identify potential inefficiencies and poor coding practices and provide all the answers in markdown format.

    Input:
        {user_code}
    Output:
        If issues found:
            Location: Class and method name(s) where the issue occurs.
            Issue: Description of the inefficiency or poor practice.
            Suggestion: Specific guidance on how to improve the code (consider providing alternative code examples).
            Severity: If possible, indicate the potential impact of the issue (e.g., performance bottleneck, maintainability risk, security vulnerability).
        If no issues found: Output "No Issues".
        
    Output Example: 
        Location: class DataProcessor, method load_data
        Issue: Loading entire file into memory at once could be inefficient for large files.
        Suggestion: Consider using a generator or line-by-line processing to reduce memory usage.
        Severity: Medium (depends on your application's expected file sizes)"""
    
    prompt_response = model.generate_content(prompt,
        generation_config={
            "max_output_tokens": 4096,
            "temperature": 0.4,
            "top_p": 1
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