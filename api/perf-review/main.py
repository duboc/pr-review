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
def perf_review(request):
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
    Task: Conduct an application performance review, focusing on language-specific issues that can lead to bottlenecks or resource contention and provide all the answers in markdown format.

    Input:
        {user_code}

    Output:
        If issues found:
            Location: Class and method name(s) where the issue occurs.
            Issue Type: Categorize the issue (e.g., string concatenation overhead, memory leak, race condition potential, deadlock possibility).
            Explanation: Detailed description of why this code pattern is problematic for performance.
            Impact: Explain how this issue could affect the application's speed, responsiveness, or scalability.
            Recommendation: Provide concrete suggestions for optimizing the code, potentially including alternative implementations.
        If no significant issues found: Output "No major performance concerns identified."
"""
    
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