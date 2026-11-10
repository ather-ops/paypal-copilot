
import json
import os

from dotenv import load_dotenv
from groq import Groq

from agent.prompts import AGENT_INSTRUCTIONS
from tools.policy_search import search_paypal_policy
from tools.paypal_tools import (
    get_paypal_disputes,
    get_paypal_dispute_details,
)

load_dotenv()


# Explicit allowlist: the model cannot execute arbitrary Python.
AVAILABLE_TOOLS = {
    "search_paypal_policy": search_paypal_policy,
    "get_paypal_disputes": get_paypal_disputes,
    "get_paypal_dispute_details": get_paypal_dispute_details,
}


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_paypal_policy",
            "description": "Search the PayPal dispute policy knowledge base for relevant rules and evidence requirements.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Specific question about PayPal dispute policies."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_paypal_disputes",
            "description": "Fetch the current dispute list from PayPal Sandbox.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_paypal_dispute_details",
            "description": "Fetch detailed information about one PayPal Sandbox dispute.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dispute_id": {
                        "type": "string",
                        "description": "The PayPal dispute ID."
                    }
                },
                "required": ["dispute_id"]
            }
        }
    }
]


def build_agent():
    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("GROQ_MODEL")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from .env")

    if not model_name:
        raise ValueError("GROQ_MODEL is missing from .env")

    return Groq(api_key=api_key)


def run_agent(question: str):

    if not isinstance(question, str) or not question.strip():
        raise ValueError("Please enter a valid question.")

    client = build_agent()
    model_name = os.getenv("GROQ_MODEL")

    messages = [
        {
            "role": "system",
            "content": AGENT_INSTRUCTIONS
        },
        {
            "role": "user",
            "content": question
        }
    ]

    max_tool_rounds = 5

    for step in range(max_tool_rounds + 1):

        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
            temperature=0.1,
            max_tokens=1800,
        )

        message = response.choices[0].message

        # The model has finished and returned its final answer.
        if not message.tool_calls:
            return message.content or "The agent returned an empty response."

        # Preserve the assistant's tool-call message in conversation history.
        messages.append(message.model_dump(exclude_none=True))

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name
            raw_arguments = tool_call.function.arguments

            if tool_name not in AVAILABLE_TOOLS:
                result = "Error: This tool is not authorized."
            else:
                try:
                    arguments = json.loads(raw_arguments)

                    result = AVAILABLE_TOOLS[tool_name](**arguments)

                    if not isinstance(result, str):
                        result = json.dumps(result, default=str)

                except Exception as error:
                    result = (
                        f"Tool execution failed: "
                        f"{type(error).__name__}: {error}"
                    )

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result[:12000]
            })

    # One final call without tools gives the model a chance to summarize.
    final_response = client.chat.completions.create(
        model=model_name,
        messages=messages + [{
            "role": "system",
            "content": "Provide your final answer now. Do not call any more tools."
        }],
        tool_choice="none",
        temperature=0.1,
        max_tokens=1800,
    )

    return (
        final_response.choices[0].message.content
        or "The agent could not produce a final answer."
    )
