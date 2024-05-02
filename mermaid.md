# Testing mermaid

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

## Explanation:

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