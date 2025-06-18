from bot_engine import BotEngine

# Initialize bot
bot = BotEngine()
bot.load_faq_data('data/faqs.json')

# Test the specific question
test_question = "comment changer mot de passe"
print(f"Testing question: '{test_question}'")
print(f"Total FAQ entries loaded: {len(bot.faq_data)}")
print()

# Get the raw matches with scores
matches = bot.find_best_matches(test_question, num_results=5)

print(f"Number of matches returned: {len(matches)}")
print("Top 5 matches with scores:")

if not matches:
    print("No matches found!")
    
    # Let's test manually with a few questions
    print("\nTesting manual fuzzy matching:")
    from fuzzywuzzy import fuzz
    
    test_questions = [
        "Comment réinitialiser mon mot de passe email ?",
        "Pourquoi rejoindre Infomaniak ?",
        "Comment configurer l'email sur mon téléphone ?"
    ]
    
    for faq_q in test_questions:
        score = fuzz.ratio(test_question.lower(), faq_q.lower())
        print(f"'{test_question}' vs '{faq_q}' = {score}%")

else:
    for i, match in enumerate(matches, 1):
        print(f"{i}. Score: {match['score']}% - Question: {match['question']}")
        print(f"   Answer: {match['answer'][:100]}...")
        print()

print(f"\nThreshold: 70%")
print(f"Matches above threshold: {len([m for m in matches if m['score'] >= 70])}")