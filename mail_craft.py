# entry point to application
from dotenv import load_dotenv
load_dotenv(override=True)

import re
import gradio as gr
from email_manager import EmailManager

email_manager = EmailManager()
should_attach_pdf = False
final_email_list = []

async def generate_email(query: str, tone: str, pdf_upload: gr.File, subject_line: str, email_body: str):
    email_output = await email_manager.run_email_generator(query, tone, pdf_upload, subject_line, email_body)
    print(f"Email output: {email_output}")
    if email_output["success"]:
        gr.Success(email_output["message"], duration=10)
    else:
        gr.Error(email_output["message"], duration=10)
    yield email_output["email_subject_line"], email_output["email_body"]


async def display_html_output(subject_line: str, email_body: str):
    html_output = await email_manager.run_html_converter(subject_line, email_body)
    yield html_output

async def set_should_attach_pdf(should_attach_pdf_value: bool):
    global should_attach_pdf
    should_attach_pdf = should_attach_pdf_value
    print(f"User wants to attach PDF to generated email: {should_attach_pdf}")


async def add_emails_to_list(emails_list_input: str):
    if emails_list_input:
        emails = re.split(r"[,\s]+", emails_list_input.strip())
        domain_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        final_email_list.extend([email.lower() for email in emails if re.fullmatch(domain_regex, email)])
        return "\n".join(final_email_list), ""
    else:
        return "", ""


async def clear_emails_list():
    global final_email_list
    final_email_list = []
    yield ""

async def send_emails_to_recipients():
    email_send_status = await email_manager.run_email_sender(final_email_list, should_attach_pdf) #  if final_email_list else [] -- do i need type checking?
    print(f"Email Sent: {email_send_status}")

with gr.Blocks() as ui:
    # EmailManager.run()
    email_section_visible = gr.State(False)
    email_section_invisible = gr.State(True)
    gr.Markdown("# Mail Craft: Email Automation AI Agent")
    gr.Markdown("## Craft Your Email with AI") #Or paste existing email to send/edit/preview
    with gr.Row(equal_height=True):
        with gr.Column(scale=1):
            query_textbox = gr.Textbox(lines=5, label="What do you want your email to be about?", placeholder="Enter your email content here")
            tone_textbox = gr.Textbox(label="What tone do you want your email to be in?", placeholder="Enter your tone here")
            pdf_upload = gr.File(label="Upload a PDF containing text", file_types=[".pdf"], type="filepath")
            should_attach_pdf_checkbox = gr.Checkbox(label="Attach PDF when sending email", value=False)
            generate_button = gr.Button("Generate Email")
        with gr.Column(scale=1):
            subject_textbox = gr.Textbox(lines=2,
                                label="Subject Line",
                                interactive=True,
                                placeholder="Your generated subject line will appear here.")
            email_body_editor = gr.Textbox(lines=18,
                                    label="Email Body",
                                    interactive=True,
                                    placeholder="Generated email will appear here. Edit as needed, then click Send.")
            with gr.Row():
                preview_button = gr.Button("Looks Good! Preview Email")
                cancel_button = gr.ClearButton(components=[query_textbox, tone_textbox, pdf_upload, email_body_editor, subject_textbox], value="Clear and Refresh")

    gr.Markdown("## Preview Your Email")
    with gr.Row():
        html_output = gr.HTML(label="HTML Output", value="")

    gr.Markdown("## Send Your Email to Multiple Recipients")
    with gr.Column() as email_list_section:
        with gr.Row():
            with gr.Column():
                emails_list_input = gr.Textbox(label="Enter email addresses to send to (comma, space, or newline separated)")
                emails_list_add_button = gr.Button("Add Emails")
                emails_list_clear_button = gr.Button("Clear Emails")
            with gr.Column():
                emails_list_container = gr.Textbox(label="Emails", value="")
                emails_list_send_button = gr.Button("Send Email")

    def toggle_email_section(visible: bool):
        new_visible = not visible
        return new_visible, gr.update(visible=new_visible)

    # event listeners
    should_attach_pdf_checkbox.change(fn=set_should_attach_pdf, inputs=[should_attach_pdf_checkbox])

    generate_button.click(fn=generate_email,
        inputs=[query_textbox, tone_textbox, pdf_upload, subject_textbox, email_body_editor],
        outputs=[subject_textbox, email_body_editor])

    preview_button.click(
        fn=display_html_output,
        inputs=[subject_textbox, email_body_editor],
        outputs=[html_output],
    )
    cancel_button.click(
        fn=toggle_email_section,
        inputs=[email_section_invisible],
        outputs=[email_section_invisible, email_list_section],
    )

    emails_list_add_button.click(fn=add_emails_to_list, inputs=[emails_list_input], outputs=[emails_list_container, emails_list_input])
    emails_list_clear_button.click(fn=clear_emails_list, inputs=None, outputs=emails_list_container)
    emails_list_send_button.click(fn=send_emails_to_recipients, inputs=None, outputs=None)

ui.launch(theme=gr.themes.Default(), inbrowser=True)
