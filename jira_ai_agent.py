import os
from jira import JIRA
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Jira Configuration
JIRA_SERVER = os.getenv('JIRA_SERVER')
JIRA_USER = os.getenv('JIRA_USER')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY')
JIRA_ISSUE_TYPE = os.getenv('JIRA_ISSUE_TYPE')

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def extract_email_text(email_content):
    """Extract plain text from an email content."""
    try:
        soup = BeautifulSoup(email_content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text
    except Exception:
       return email_content

def summarize_issue_with_gpt(email_text):
    """Summarize email content with OpenAI."""
    try:
        prompt = f"""
            You are a helpful AI assistant tasked with summarizing customer complaint emails and extracting key information to create a Jira ticket. Please be concise and focus on the core issue the customer is reporting.

            Email Content:
            {email_text}

            Summary of the issue:
        """

        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        summary = chat_completion.choices[0].message.content
        return summary.strip()
    except Exception as e:
         print(f"Error during OpenAI processing: {e}")
         return "Unable to summarize email. Check logs."


def create_jira_ticket(email_summary, email_text, customer_name="Unknown"):
    """Create a new Jira ticket."""
    try:
        jira_options = {"server": JIRA_SERVER}
        jira = JIRA(options=jira_options, basic_auth=(JIRA_USER, JIRA_API_TOKEN))

        issue_dict = {
            'project': {'key': JIRA_PROJECT_KEY},
            'summary': f'Customer Complaint: {email_summary[:150]}...', # Trim summary if too long
            'description': f"Customer Name: {customer_name}\n\nSummary: {email_summary}\n\nOriginal Email:\n{email_text}",
            'issuetype': {'name': JIRA_ISSUE_TYPE}
        }
        new_issue = jira.create_issue(fields=issue_dict)
        print(f"Jira ticket created: {new_issue.key} - {new_issue.fields.summary}")
        return new_issue.key
    except Exception as e:
        print(f"Error creating Jira ticket: {e}")
        return None

def process_email(email_content, customer_name="Unknown"):
    """Main function to process email and create Jira ticket."""
    email_text = extract_email_text(email_content)
    issue_summary = summarize_issue_with_gpt(email_text)

    if issue_summary:
       jira_key = create_jira_ticket(issue_summary, email_text, customer_name)
       if jira_key:
        print(f"Ticket {jira_key} has been created")
       else:
        print("Failed to create Jira Ticket")
    else:
      print("Failed to analyze email")
    return

if __name__ == '__main__':
    # Example usage - you would fetch this from an email service
    email_example = """
       <div dir="ltr">
            <p>Hi Support Team,</p>
             <p>I am writing to report a problem with your website. When I try to log in, I receive an "Invalid Credentials" error, even though I am sure my password is correct. I tried resetting my password, but I'm still facing the same problem.</p>
             <p>Please assist.</p>
            <p>Thanks,<br>
              John L
            </p>
        </div>
     """
    process_email(email_example, "John L")
