import json
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

def respond_to_prompt(api_key, model, message_json):
    client = OpenAI(api_key=api_key)

    if not isinstance(message_json, dict):
        try:
            message_json = json.loads(message_json)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")

    if "prompt" not in message_json:
        raise ValueError("Missing 'prompt' field")

    prompt = message_json["prompt"]
    
    response = client.chat.completions.create(
        model=model,
        store=False,
        messages=[{"role": "user", "content": prompt}]
    )
        
    return response