# PR Review Application - README

This application aims to automate various aspects of the code review process using Google Cloud Platform (GCP) services and Vertex AI's generative models. It provides functionalities for code review, performance review, diff review, security review, and credentials review.

## Components:
The application consists of several key components:

- Cloud Build Trigger: This trigger initiates the review process upon a pull request (PR) creation or update. It retrieves the PR diff and interacts with Cloud Run services for different review types.
  - Cloud Run Services: These services host the APIs for different review functionalities:
    - Code Review API: Analyzes code for inefficiencies and poor coding practices using the gemini-1.0-pro-001 model.
    - Performance Review API: Identifies potential performance bottlenecks and resource contention using the gemini-1.0-pro-001 model.
    - Diff Review API: Summarizes the main changes and identifies broken SOLID principles in the PR diff using the gemini-1.0-pro-001 model.
    - Security Review API: Detects potential security vulnerabilities like insecure cookies, session management, SQL injection, and XSS using the gemini-1.0-pro-001 model.
    - Credentials Review API: Identifies potential credential leaks, hardcoded passwords, and exposed environment variables using the gemini-1.0-pro-001 model.
- Vertex AI Generative Models: The application leverages the power of Vertex AI's generative models, specifically gemini-1.0-pro-001, to analyze code and provide insightful feedback.
- Cloud Functions: A Cloud Function is used to analyze Cloud Build failures and provide explanations using the gemini-pro model.
- Cloud Storage: Stores the generated review reports and other relevant data.
- 
### Usage
**Setup:**

- Ensure you have a GCP project with necessary APIs enabled (Cloud Build, Cloud Run, Artifact Registry, Vertex AI, etc.).
- Follow the specific deployment instructions provided in each API's README file to deploy the Cloud Run services.

Configure the Cloud Build trigger with appropriate environment variables and secrets.
Triggering Reviews:
1. Create or update a pull request in your repository.
2. The Cloud Build trigger will automatically initiate the review process.
  - Review Reports:
The generated review reports will be posted as comments on the pull request.
You can also access the reports directly in Cloud Storage.
Additional Notes:
The application is currently a work in progress (WIP) and may require further customization and development based on your specific needs.
The provided codebase includes sample configurations and deployment instructions. You may need to adjust them based on your environment and preferences.
Consider exploring the capabilities of Vertex AI's generative models to further enhance the review process and tailor it to your specific requirements.
Disclaimer:
While the application leverages advanced AI models, it's important to remember that the generated reviews are suggestions and should not be considered as definitive or exhaustive. Human judgment and expertise are still crucial in the code review process.