# 1. Storing data in variables
total_messages_to_scan = 3
spam_keyword = "FREE MONEY"

print("--- STARTING AI SPAM SCANNER ---")

# 2. Using a loop to simulate scanning 3 separate messages
for message_number in range(1, total_messages_to_scan + 1):
    
    print("Scanning message number:", message_number)
    
    # Simulating different text messages arriving at our system
    if message_number == 2:
        user_text = "FREE MONEY"
    else:
        user_text = "Hello, how are you today?"
        
    # 3. Using an IF statement to make a decision based on the text
    if user_text == spam_keyword:
        print("⚠️ ALERT: Spam detected in message!", message_number)
    else:
        print("✅ Message is clean.")
        
    print("---------------------------------") # A simple separator line

print("--- SCANNING COMPLETE ---")