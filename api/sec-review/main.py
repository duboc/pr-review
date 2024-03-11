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
def sec_review(request):
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

    Prompt:

        Task: Conduct a security-focused code review to identify potential vulnerabilities and provide all the answers in markdown format.

        Inputs:

            Code: {user_code}
		Focus Areas:
			Insecure Cookies: Check cookie handling for issues like missing HttpOnly and Secure flags, inadequate expiration, or sensitive data stored in plaintext.
            Insecure Session Management: Examine session generation, storage, transmission, timeout mechanisms, and protection against session hijacking or fixation.
		    SQL Injection: Look for any unsanitized user input used directly in SQL queries.
		    Cross-Site Scripting (XSS): Inspect how user input is handled and whether it's properly sanitized/encoded before being rendered on web pages.
		    Other Vulnerabilities: Remain alert for:
		    Authorization flaws (e.g., missing access checks)
		    Buffer overflows (especially in languages like C/C++)
		    Insecure file uploads
		    Sensitive data exposure
		Output:
		    If issues found:
		        Class name.Method name: Where the vulnerability exists.
		        Issue: Specific type of vulnerability (e.g., SQL injection, reflected XSS).
		        Explanation: Brief description of why the code is problematic.
		        Recommendation: Concrete steps to fix the vulnerability, including code examples if possible.
		    If no issues found: Output "No major security issues found."
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