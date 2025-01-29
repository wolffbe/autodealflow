import logging
import json

logger = logging.getLogger(__name__)

def replace_placeholders(prompt_template, replacements):
    for placeholder, replacement in replacements.items():
        if placeholder not in prompt_template:
            raise ValueError(f"Missing placeholder '{placeholder}' in prompt template.")
        prompt_template = prompt_template.replace(placeholder, replacement, 1)
    
    for placeholder in replacements:
        if placeholder in prompt_template:
            raise ValueError(f"Failed to replace placeholder '{placeholder}' in prompt. It still exists in the template.")
    
    logger.debug("Successfully replaced all placeholders in the prompt template.")
    return prompt_template

def compile_is_opp_prompt(is_opportunity_prompt_path, email_json, thesis):
    email_text = "".join(json.dumps(email_json).split())
    replacements = {
        "EMAIL": email_text,
        "THESIS": json.dumps(thesis)
    }

    try:
        logger.debug("Reading 'is_opportunity' prompt file.")
        with open(is_opportunity_prompt_path, 'r') as prompt_file:
            prompt_template = prompt_file.read()

        prompt = replace_placeholders(prompt_template, replacements)

        logger.debug("Successfully compiled 'is_opportunity' prompt.")
        return prompt

    except Exception as e:
        raise ValueError(f"Error reading or formatting 'is_opportunity' prompt file: {e}")

def compile_opp_prompt(opportunity_prompt_path, opportunity_fields, parsed_email):
    replacements = {
        "OPP_FIELDS": json.dumps(opportunity_fields),
        "EMAIL": json.dumps(parsed_email)
    }

    try:
        logger.debug("Reading 'opportunity' prompt file.")
        with open(opportunity_prompt_path, 'r') as prompt_file:
            prompt_template = prompt_file.read()

        prompt = replace_placeholders(prompt_template, replacements)

        logger.debug("Successfully compiled 'opportunity' prompt.")
        return prompt

    except Exception as e:
        raise ValueError(f"Error reading or formatting 'opportunity' prompt file: {e}")