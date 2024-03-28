import os
import base64
from flask import Flask, request
import google.cloud.logging

import vertexai
from vertexai.language_models import TextGenerationModel
from vertexai.preview.generative_models import GenerativeModel

PROJECT_ID = os.environ.get('GCP_PROJECT', '-')
LOCATION = os.environ.get('GCP_REGION', '-')

app = Flask(__name__)

#Instanciate Cloud Logging client
client = google.cloud.logging.Client(project=PROJECT_ID)
client.setup_logging()
log_name = "secreview-cloudrun-log"
logger = client.logger(log_name)

# Default Route to service heath easy validation
@app.route('/')
def main():
    name = PROJECT_ID
    return f"sec-review app - {name}!"

# Sec Review Post 
@app.route('/sec_review', methods=['POST'])
def sec_review():
    logger.log(f"Received a request for code review")

    # Parse the request body
    request_json = request.get_json(silent=True)

    # Extract the word from the request body and decode
    if request_json and 'code' in request_json:
        user_code = base64.b64decode(request_json['code']) 
        logger.log(f"Received code from user: {user_code}")
    else:
        user_code = "NO SOURCE PROVIDED"
        logger.log(user_code)

 
    #Vertex AI integration
    vertexai.init(project=PROJECT_ID, location=LOCATION) 
    model = GenerativeModel("gemini-1.0-pro-001")


    prompt = f"""
    Consider the following code snippet:
        {user_code}
    Conduct a security-focused code review to identify potential vulnerabilities.
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
    logger.log(f"Gemini Model response: {prompt_response.text}")

    # Format the response using Markdown
    format_prompt = f"""
     Execute this list of tasks:
     - Format the code as Markdown, where the topic's header must be bold
     For the following text:
     {prompt_response.text}
    """
    final_response = model.generate_content(format_prompt,
        generation_config={
            "max_output_tokens": 4096,
            "temperature": 0.4,
            "top_p": 1
        },
    )
    logger.log(f"Formated Gemini Model response: {final_response.text}")

    #Return the final response as plain text
    return final_response.text, 200, {'Content-Type': 'text/plain'}

if __name__ == "__sec-review-main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))