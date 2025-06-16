# chat_test.py
from bot_engine import BotEngine

def main():
    # Initialize bot
    print("🤖 Initializing FAQ Chatbot...")
    bot = BotEngine()
    bot.load_faq_data("data/faqs.json")
    
    if not bot.faq_data:
        print("❌ No FAQ data loaded. Please check your data file.")
        return
    
    print("✅ Bot ready!\n")
    print("=" * 60)
    print("🤖 WELCOME TO INFOMANIAK FAQ CHATBOT")
    print("=" * 60)
    print("I can help you with:")
    print("  📧 Email configuration and setup")
    print("  🔑 Password reset and account management") 
    print("  💾 Email backup and storage")
    print("  🛠️ Technical troubleshooting")
    print("  ❓ General Infomaniak service questions")
    print("\n💡 Tips:")
    print("  • Ask in English or French")
    print("  • Use specific keywords like 'email', 'password', 'backup'")
    print("  • Try different phrasings if no match is found")
    print("\n📝 Examples:")
    print('  "How to reset my email password?"')
    print('  "Comment configurer l\'email sur mon téléphone?"')
    print('  "Why should I join Infomaniak?"')
    print("\n" + "=" * 60)
    print("Type 'quit' to exit. What can I help you with today?\n")
    
    # Interactive chat loop
    while True:
        # Get user input
        user_question = input("You: ").strip()
        
        # Exit condition
        if user_question.lower() in ['quit', 'exit', 'q']:
            print("👋 bye!")
            break
        
        if not user_question:
            continue
            
        # Get bot response
        result = bot.get_answer(user_question)
        
        # Display response
        print(f"\n🤖 Bot ({result['language']}): {result['response']}")

        if result['matches']:
            for i, match in enumerate(result['matches'], 1):
                print(f"\n📋 Option {i}: {match['question']}")
                print(f"💡 Answer: {match['answer']}")
                print(f"🎯 Confidence: {match['score']}%")

if __name__ == "__main__":
    main()