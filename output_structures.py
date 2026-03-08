# to set syntactical guardrails for the output of the agents
from pydantic import BaseModel, Field

"""
Output structure for the email generator agent.
"""
class EmailOutput(BaseModel):
    email_subject_line: str = Field(description="A relevant subject line for the email.")
    email_body: str = Field(description="Email body in plain text.")

"""
Output structure for the email Sender agent.
"""
class EmailSenderOutput(BaseModel):
    status: str = Field(description="The status of the email sending process either 'success' or 'error'.")
    message: str = Field(description="The message of the email sending process.")

"""
Output structure for the input validator agent.
"""
class InputValidationOutput(BaseModel):
    is_invalid: bool = Field(description="Whether the input is invalid or not.")
    reason: str | None = Field(description="The reason for the input validation.")