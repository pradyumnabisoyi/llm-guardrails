# import re

BLOCKED_OUTPUT_PATTERNS = [
    "api key",
    "api_key",
    "secret key",
    "password",
    "private key",
]

# OUTPUT GUARDRAILS
def check_output(output: str) -> dict:
    """
    Validate Gemini Output.
    Return:
    Allowed
    category
    message
    """

# 1 . empty Output
    if not output or not output.strip():
        return{
                "allowed":False,
                "category": "EMPTY_OUTPUT",
                "message": (
                    "Model Returned an empty response."
                )
            }
# 2. Normalize
    text = output.lower()

# 3. Sensitive Information
    for pattern in BLOCKED_OUTPUT_PATTERNS:
        if pattern in text:
            return{
                "allowed":False,
                "category": "SENSITIVE_OUTPUT",
                "message": (
                    "Potrntially sensitive information "
                    "detected in model output."
                )
            }
# 4. safe output
    return{
            "allowed":True,
            "category": "SAFE",
            "message": "optput passed all guardrails."
        } 
    