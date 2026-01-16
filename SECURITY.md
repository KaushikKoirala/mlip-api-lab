# Security Best Practices

This document outlines the security measures implemented in this project for handling API credentials.

## Credential Management Best Practices

### 1. Never Hard-Code Credentials
- **Problem**: Hard-coding credentials in source code exposes them to anyone with access to the repository
- **Solution**: Store credentials in environment variables or configuration files that are excluded from version control
- **Implementation**: We use a `.env` file for local development and load credentials using `python-dotenv`

### 2. Never Commit Credentials to Git
- **Problem**: Once committed, credentials remain in Git history even if removed later
- **Solution**: Use `.gitignore` to exclude credential files before committing
- **Implementation**:
  - `.env` is listed in `.gitignore` (line 123)
  - We provide `.env.example` as a template
  - Verify with `git status` before committing

### 3. Rotate Secrets Regularly
- **Recommendation**: Periodically regenerate API keys and update them
- **Why**: Limits the window of exposure if a key is compromised
- **How**: Follow your API provider's documentation to generate new keys

### 4. Encrypt Secrets at Rest and in Transit
- **At Rest**: Store `.env` files with appropriate file permissions (e.g., `chmod 600 .env`)
- **In Transit**: Always use HTTPS/TLS when transmitting credentials
- **Implementation**: LiteLLM uses HTTPS for API calls by default

### 5. Practice Least-Access Privilege
- **Principle**: Grant minimum necessary permissions
- **Application**:
  - Restrict file permissions on credential files
  - Use API keys with minimal required scopes
  - Limit access to production environments

## Setup Instructions

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your actual API key:
   ```
   GROQ_API_KEY=your_actual_api_key_here
   ```

3. Set appropriate file permissions (Unix/Linux/Mac):
   ```bash
   chmod 600 .env
   ```

4. Verify `.env` is ignored by Git:
   ```bash
   git status
   # .env should NOT appear in the output
   ```

## What to Commit vs. What to Keep Local

### ✅ Safe to Commit
- `.env.example` (template with placeholder values)
- `.gitignore` (ensures credentials are excluded)
- Code that loads from environment variables
- Documentation about security practices

### ❌ Never Commit
- `.env` (actual credentials)
- Any file containing real API keys
- Configuration files with production secrets
- Backup files that might contain credentials

## Implementation in This Project

### Code Changes
The `analyze.py` file has been updated to:
1. Load API key from environment variable using `dotenv`
2. Validate that the key exists before making API calls
3. Provide clear error messages if credentials are missing
4. Use Pydantic for response validation and schema enforcement

### Schema Validation
The response from the LLM is validated against a predefined schema:
```python
class ItinerarySchema(BaseModel):
    destination: str
    price_range: str
    ideal_visit_times: List[str]
    top_attractions: List[str]
```

This ensures:
- Type safety
- Required fields are present
- Data structure consistency
- Early error detection

## Additional Resources
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [12-Factor App: Config](https://12factor.net/config)
- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
