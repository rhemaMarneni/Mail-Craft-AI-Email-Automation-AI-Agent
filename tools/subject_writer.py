from agents import Agent

subject_writer_instructions = "Given an email body text, generate a succinct and appropriate subject line for it."

subject_writer_agent = Agent(name="Email Subject Generator",
                    instructions=subject_writer_instructions,
                    model="gpt-4o-mini")