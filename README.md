# Jira Ticket Creation Agent

This Python-based agent automatically creates Jira tickets from customer complaint emails. It leverages OpenAI for text summarization and the Jira Python library for ticket creation.

## Prerequisites

Before running the agent, ensure you have the following:

1.  **Python 3.6+:** You must have Python installed on your system.
2.  **Jira Account:** You need access to your Jira instance with the necessary permissions to create tickets.
3.  **OpenAI API Key:** You need to have an API Key from OpenAI to use the GPT model for summarization.
4.  **Python Libraries:** Install required libraries using pip (see Installation section).

## Installation

1.  **Clone the Repository:** (If you've got this in a Git repo)

    ```bash
    git clone [your-repository-url]
    cd [your-repository-directory]
    ```

2.  **Install Dependencies:** Use `pip` to install the required packages:

    ```bash
    pip install jira beautifulsoup4 requests python-dotenv openai
    ```

## Configuration

1.  **Create `.env` File:** In the same directory as `jira_ticket_agent.py`, create a file named `.env` and add the following:

    ```env
    JIRA_SERVER="your_jira_url"  # e.g., "https://yourcompany.atlassian.net"
    JIRA_USER="your_jira_username"
    JIRA_API_TOKEN="your_jira_api_token"  # Generate in Jira user settings
    JIRA_PROJECT_KEY="your_jira_project_key" # e.g., PROJ
    JIRA_ISSUE_TYPE="Bug"  # or Task, Story, etc
    OPENAI_API_KEY="your_openai_api_key" # Your OpenAI API key
    ```

    *   **Replace placeholders:** Make sure to replace the placeholders with your actual Jira credentials, project key, desired issue type and the OpenAI API key.
    *   **Jira API Token:**  Generate an API token in your Jira account's security settings.
    *   **Project Key:** Locate the project key in your Jira project settings.
    *   **Issue Type:** Choose the type of issue you want to create when you raise a ticket.

## How to Run

1.  **Navigate to the Directory:** In your terminal, navigate to the directory where you have `jira_ticket_agent.py`.

2.  **Run the Script:** Execute the script:

    ```bash
    python jira_ticket_agent.py
    ```

    The example code has an email embedded for testing. This will process that email, summarize it and create a Jira ticket if all configurations are correct and it can access your Jira and OpenAI account.

## Notes and Enhancements

*   **Error Handling:** The current error handling is basic. You should enhance it with specific handling for network issues, API errors, etc.
*   **Email Integration:** This script currently uses a hardcoded example email string. In order to fully integrate, you must integrate with your chosen email provider (e.g., using IMAP, an email API, or a webhook) to fetch real complaint emails and pass the email to the `process_email()` function.
*   **Jira Customization:**  If your Jira uses custom fields, adjust the `issue_dict` dictionary in `create_jira_ticket` to handle these fields.
*   **Security:** Ensure you do not expose your API keys and use environment variables (as done in this case).
*   **Rate Limiting:** Be mindful of rate limits imposed by email services and APIs.
*   **Cost of OpenAI Usage:** Keep an eye on your OpenAI usage costs, as each request to the GPT model will incur charges.

## Example

After successful execution, you should see output on the console similar to the below:
Jira ticket created: PROJ-1234 - Customer Complaint: Summary of complaint ...
Ticket PROJ-1234 has been created

Where `PROJ-1234` is the created Jira Ticket key.

## Further Development

*   **Email parsing**: Enhance how the `extract_email_text` works to support various email types and formats, with embedded images, etc
*   **Email filtering**: Add functions that classifies the email as a complaint before processing to ensure only legitimate emails are processed.
*  **Logging**: Implement logging to track the activity of the script and ease debugging.
*   **Automation**: Consider integrating with a task scheduler (e.g., cron on Linux) for regular automated processing.
