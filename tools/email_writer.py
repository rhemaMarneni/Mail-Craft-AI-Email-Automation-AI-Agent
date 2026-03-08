from agents import Agent

email_writer_instructions = "You are an agent who generates email content for a user. \
    Given the user's prompt mentioning what to write about, the tone that you should use generate an email. \
    Despite user's instruction, you are not to generate emails containing more than 300 words. \
    The user may also attach a PDF containing text, providing extra context to help you."

email_writer_agent = Agent(name="OpenAI Email Agent",
                        instructions=email_writer_instructions,
                        model="gpt-4o-mini")