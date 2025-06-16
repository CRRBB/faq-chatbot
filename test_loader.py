# test_loader.py
import json
from bot_engine import BotEngine

# Create bot instance
bot = BotEngine()

# Test the loader
print("Testing FAQ loader...")
bot.load_faq_data("data/faqs.json")

# Check if it worked
print(f"Loaded {len(bot.faq_data)} FAQ entries")
print("\nFirst FAQ entry:")
if bot.faq_data:
    print(f"Question: {bot.faq_data[0]['question']}")
    print(f"Answer: {bot.faq_data[0]['answer']}")
else:
    print("No data loaded!")


# Test language detection
print("\n--- Testing Language Detection ---")
print("French test:", bot.detect_language("Comment puis-je réinitialiser mon mot de passe?"))
print("English test:", bot.detect_language("How do I reset my password?"))


# Test fuzzy matching
print("\n--- Testing Best Matches ---")
results = bot.find_best_matches("How can I change my password?")
for i, match in enumerate(results, 1):
    print(f"{i}. {match['question']} (Score: {match['score']}%)")

    # Test complete bot engine
print("\n--- Testing Complete Bot ---")
result = bot.get_answer("How can I reset my password?")
print(f"Language detected: {result['language']}")
print(f"Response: {result['response']}")
print("Matches found:")
for i, match in enumerate(result['matches'], 1):
    print(f"  {i}. {match['question']} ({match['score']}%)")
    print(f"     Answer: {match['answer'][:50]}...")