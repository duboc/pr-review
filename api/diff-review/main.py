import os
import json
#import functions_framework
from flask import Flask, request
import google.cloud.logging

import vertexai
from vertexai.language_models import TextGenerationModel
#from flask_cors import cross_origin
from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_

PROJECT_ID = os.environ.get('GCP_PROJECT', '-')
LOCATION = os.environ.get('GCP_REGION', '-')
client = google.cloud.logging.Client(project=PROJECT_ID)
client.setup_logging()
log_name = "code-cloudfunction-log"
logger = client.logger(log_name)


app = Flask(__name__)

@app.route('/')
def main():
    name = PROJECT_ID
    return f"diff-review app - {name}!"


@app.route('/diff_review', methods=['POST'])
def diff_review():
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
    As a Senior Developer, ignore small changes and summarize the following code in bullet points, using the following format:

    Main changes:
    - Bullet-points with main changes

    Performance and security recommendations:
    - Bullet-points with performance and security recommendations that could be added

    Broken SOLID Concepts:
    - Bullet-points with broken solid concepts

    If no changes are found: Output "No changes are found.

    Consider the following code:
    {user_code}
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

    # Format the response
    # data = {}
    # data['response'] = []
    # data['response'].append({"details": final_response.text})
    # return json.dumps(data), 200, {'Content-Type': 'application/json'}

    return final_response.text, 200, {'Content-Type': 'text/plain'}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))