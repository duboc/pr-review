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
log_name = "perfreview-cloudrun-log"
logger = client.logger(log_name)

# Default Route to service heath easy validation
@app.route('/')
def main():
    name = PROJECT_ID
    return f"perf-review app - {name}!"

# perf Review Post 
@app.route('/perf_review', methods=['POST'])
def perf_review():
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

if __name__ == "__perf-review-main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

