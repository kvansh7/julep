import os
from julep import Julep
import uuid
import yaml
import time


# Retrieve Julep API key from environment
BRAVE_API_KEY = os.environ.get('BRAVE_API_KEY')
JULEP_API_KEY = os.environ['JULEP_API_KEY']
client = Julep(api_key=JULEP_API_KEY)

# Create the agent
agent = client.agents.create(
  name="Research agent",
  model="claude-3.5-sonnet",
  about="A agent which can research about topic",
)


task_definition = yaml.safe_load("""
name: Structured Wikipedia Research Task
description: Research a topic and present it in a structured format (summary, bullet points, or short report)

main:
  # Step 0: Gather information on the provided topic
  - prompt: |-
      You are a helpful research assistant. Your goal is to gather reliable information on the topic provided below. Use credible sources, such as Wikipedia or other authoritative references, and prepare a concise collection of relevant facts and details.
      Topic: {steps[0].input.topic}
    unwrap: true

  # Step 1: Format the gathered information into the requested structure
  - prompt: |-
      Using the information gathered below, structure it into the requested output format (e.g., 'summary', 'bullet points', 'short report') as specified: "{steps[0].input.output_format}".
      Information to format:
      {steps[0].output}
    unwrap: true

  # Step 2: Conditionally apply the final formatting
  - prompt: |-
      Maintain a neutral, objective tone. Strictly adhere to the requested output format, i.e., "{steps[0].input.output_format}". Use the rules below and produce ONLY that format:

      if "{steps[0].input.output_format}" == "summary":
      - Write a concise summary of the topic in 3-4 sentences.

      elif "{steps[0].input.output_format}" == "bullet points":
      - Present the information in a maximum of 5 concise bullet points.

      elif "{steps[0].input.output_format}" == "short report":
      - Write a short report under 150 words.

      else:
      - Invalid format requested. Only 'summary', 'bullet points', or 'short report' are supported.

      If the information below is unreliable or insufficient, respond with: "No reliable information could be found on this topic."

      Content to finalize:
      {steps[1].output}
    unwrap: true                            
    """)

task = client.tasks.create(
    agent_id=agent.id,
    **task_definition # Unpack the task definition
)
execution = client.executions.create(
    task_id=task.id,
    input={
        "topic": "cristiano ronaldo",
        "output_format": "summary"
    }
)

print(f"Agent created with ID: {agent.id}")
print(f"Task created with ID: {task.id}")