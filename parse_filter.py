import json
import os
import re
import openai
from pathlib import Path

def filter_content(content, openai_api_key):
    openai.api_key = openai_api_key

    prompt = f"""
        You are an expert in industrial control protocols. Given a Markdown document of a protocol specification, your task is to determine whether the content is related to the protocol’s grammar and communication state machine.
        In this context, “protocol grammar” refers to the formal rules that define:
            - the structure and format of protocol messages (e.g., data frames, packets),
            - the types and fields within a message,
            - command and response formats,
            - state machines or state transitions,
            - encoding rules,
            - byte-level layout and field semantics.
        The content **does not** count as grammar-related if it only cover general descriptions, system architecture, device roles or applications, device installation, or application scenarios and so on. Note: Grammar-related content may often include technical keywords such as: **Encapsulation, Messages, Data Flow, Layering, Frame, Format, Header, Payload, Field, Offset, Encoding, Bit Order** — but your decision should be based on semantic meaning, not the presence of keywords alone.
        Your response must be either:
            - "true" — if the Markdown content is related to protocol grammar
            - "false" — otherwise
        Respond with a single word only: "true" or "false". 
        Markdown content is as follows:
        === BEGIN SPEC ===
        {content}
        === END SPEC ===
    """

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt}
                ]
            }
        ],
        temperature=0.3,
        max_tokens=10
    )
    
    result = response.choices[0].message.content.strip().lower()
    print("LLM raw response:", response.choices[0].message.content)
    return result == "true"

def process_markdown(markdown_path, openai_api_key):
    markdown_path = Path(markdown_path)
    
    # Read the markdown file
    try:
        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading markdown file: {str(e)}")
        return False
    
    # Filter the content
    is_protocol_related = filter_content(content, openai_api_key)
    
    return is_protocol_related

if __name__ == "__main__":
    openai_api_key = "PLACEHOLDER_API_KEY"
    markdown_path = "dnp-2.md"
    
    try:
        result = process_markdown(markdown_path, openai_api_key)
        print(f"{markdown_path} is {result}")
    except Exception as e:
        print(f"Error processing markdown: {str(e)}") 