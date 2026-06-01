# input_handler.py

def get_user_input():
    """
    Get input from the user and normalize it.
    """
    user_input = input("\n🔎 Enter what you want to check (keyword or claim): ").strip()

    if not user_input:
        raise ValueError("Input cannot be empty")

    return {
        "raw": user_input,
        "lower": user_input.lower(),
        "tokens": user_input.lower().split()
    }
