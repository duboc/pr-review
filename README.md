# PR Review Application - README

This application aims to automate various aspects of the code review process using Google Cloud Platform (GCP) services and Vertex AI's generative models. It provides functionalities for code review, performance review, diff review, security review, and credentials review.

## Components:
The application consists of several key components:

- **Cloud Build Trigger**: This trigger initiates the review process upon a pull request (PR) creation or update. It retrieves the PR diff and interacts with Cloud Run services for different review types.
  - **Cloud Run Services**: These services host the APIs for different review functionalities:
    - **Code Review API**: Analyzes code for inefficiencies and poor coding practices using the **gemini-1.0-pro-001 model**.
    - Performance Review API: Identifies potential performance bottlenecks and resource contention using the **gemini-1.0-pro-001 model**.
    - Diff Review API: Summarizes the main changes and identifies broken SOLID principles in the PR diff using the **gemini-1.0-pro-001 model**.
    - Security Review API: Detects potential security vulnerabilities like insecure cookies, session management, SQL injection, and XSS using the g**emini-1.0-pro-001 model**.
    - Credentials Review API: Identifies potential credential leaks, hardcoded passwords, and exposed environment variables using the **gemini-1.0-pro-001 model**.
- **Vertex AI Generative Models**: The application leverages the power of Vertex AI's generative models, specifically **gemini-1.0-pro-001**, to analyze code and provide insightful feedback.
- **Cloud Functions**: A Cloud Function is used to analyze Cloud Build failures and provide explanations using the gemini-pro model.
- **Cloud Storage**: Stores the generated review reports and other relevant data.
  
### Usage
**Setup:**

- Ensure you have a GCP project with necessary APIs enabled (Cloud Build, Cloud Run, Artifact Registry, Vertex AI, etc.).
- Follow the specific deployment instructions provided in each API's README file to deploy the Cloud Run services.

Configure the Cloud Build trigger with appropriate environment variables and secrets.
Triggering Reviews:
1. Create or update a pull request in your repository.
2. The Cloud Build trigger will automatically initiate the review process.
3. Review Reports:
4. The generated review reports will be posted as comments on the pull request.

### Additional Notes:
The application is currently a work in progress (WIP) and may require further customization and development based on your specific needs.

The provided codebase includes sample configurations and deployment instructions. You may need to adjust them based on your environment and preferences.

Consider exploring the capabilities of Vertex AI's generative models to further enhance the review process and tailor it to your specific requirements.

### Architecture and components

```mermaid
graph LR
  subgraph GitHub
    PR[Pull Request] --> CloudBuild[Cloud Build Trigger]
  end

  subgraph Cloud Build
    CloudBuild --> SecretManager(Secret Manager)
    SecretManager --> CloudBuild
    CloudBuild --> GitHub(GitHub API)
    GitHub --> CloudBuild
    CloudBuild --> DiffReview(Diff Review API)
    DiffReview --> CloudBuild
    CloudBuild --> SecReview(Security Review API)
    SecReview --> CloudBuild
    CloudBuild --> PerfReview(Performance Review API)
    PerfReview --> CloudBuild
    CloudBuild --> CredsReview(Credentials Review API)
    CredsReview --> CloudBuild
    CloudBuild --> GitHub
  end

  subgraph Vertex AI
    DiffReview --> Gemini[Gemini Model]
    SecReview --> Gemini
    PerfReview --> Gemini
    CredsReview --> Gemini
  end

  subgraph Cloud Functions
    CloudBuild --> CICD_TS[CICD Troubleshooting]
    CICD_TS --> Gemini
    CICD_TS --> Storage(Cloud Storage)
    Storage --> Render(Markdown Render)
  end
  ```

#### Explanation:

1. **GitHub:** A Pull Request triggers the Cloud Build pipeline.
2. **Cloud Build:**
- Retrieves secrets from Secret Manager for GitHub authentication.
- Uses the GitHub API to fetch the PR diff and post comments.
- Calls each review API (Diff, Security, Performance, Credentials) with the PR diff.
- Each review API uses the Gemini model in Vertex AI for analysis and returns results.
- Cloud Build posts the review results as comments on the PR.
- If the build fails, it triggers the CICD Troubleshooting Cloud Function.
3. **Vertex AI:** The Gemini model processes the code and provides insights for each review type.
4. **Cloud Functions:**
- The CICD Troubleshooting function uses the Gemini model to analyze build logs and generate a markdown report explaining the failure.
- The report is stored in Cloud Storage and rendered by the Markdown Render function.

**Note:** This flowchart provides a high-level overview of the interactions. Additional details and error handling might be present in the actual implementation.

#### Disclaimer:
While the application leverages advanced AI models, it's important to remember that the generated reviews are suggestions and should not be considered as definitive or exhaustive. Human judgment and expertise are still crucial in the code review process.
