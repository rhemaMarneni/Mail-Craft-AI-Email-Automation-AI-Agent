import os
import requests
import certifi

from agents import Agent, function_tool
from consts import MAILGUN_BASE_URL
from output_structures import EmailSenderOutput

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

MAILGUN_API_URL = f"{MAILGUN_BASE_URL}/v3/{os.environ['MAILGUN_DOMAIN']}/messages"
FROM_CREDENTIALS = f"{os.environ['SENDER_NAME']} <{os.environ['SENDER_EMAIL_ADDRESS']}>"  # Ex: "Jane Doe <jane.doe@gmail.com>"

@function_tool
async def send_html_email(to_addresses: list[str], html_email: str, should_attach_pdf: bool, pdf_file_path: str, subject_line: str) -> dict:
    """Send an HTML email using the Mailgun API."""
    try:
        files = None
        print(FROM_CREDENTIALS)
        if should_attach_pdf and pdf_file_path:
            files = [("attachment", (os.path.basename(pdf_file_path), open(pdf_file_path, "rb"), "application/pdf"))]
            print(files)
        response = requests.post(
            MAILGUN_API_URL,
            auth=("api", os.getenv('MAILGUN_API_KEY')),
            data={
                "from": FROM_CREDENTIALS,
                "to": to_addresses,
                "subject": subject_line,
                "html": html_email,
            },
            files=files
        )
        if response.status_code == 200:
            return {
                "status": "success",
                "message": f"Email sent to {len(to_addresses)} recipients"
            }
        return {
            "status": "error",
            "message": response.text
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


INSTRUCTIONS = """You receive a JSON message with: to_addresses (list of email strings), html_email (HTML string), should_attach_pdf (boolean), pdf_file_path (string, may be empty).
Call your send_html_email tool once with exactly those four arguments. Do not modify or summarize the HTML or the list of addresses."""

email_sender_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_html_email],
    model="gpt-4o-mini",
    output_type=EmailSenderOutput
)
