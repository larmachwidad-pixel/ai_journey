"""
AI Spam Scanner
---------------
A step-by-step script to scan text for spam.
"""

SPAM_KEYWORDS = ["FREE MONEY", "URGENT", "WINNER"]

def check_message(text: str) -> int:
    clean_text = text.upper()
    spam_count = 0  # Start our counter at 0
    
    for keyword in SPAM_KEYWORDS:
        if keyword in clean_text:
            spam_count = spam_count + 1  # Found one! Add 1 to the count
            
    return spam_count  # Return the final number instead of True/False

if __name__ == "__main__":
    my_message = "URGENT: You are a WINNER! Claim your prize now."
    print(check_message(my_message))




