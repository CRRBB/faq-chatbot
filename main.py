print("Hello! I'm learning to build an FAQ bot")

bot_name ="SmartFAQ Assisstant"
version = 1.0
is_learning = True

print(f"Bot name: {bot_name}")
print(f"Version: {version}")
print(f"Am I learning ? {is_learning}")

user_question = "How do I reset my password ?"
confidence_score = 85.5
faq_count = 0
faqs_loaded = False

print(f"Question: {user_question}")
print(f"Confidence: {confidence_score}")
print(f"FAQ count : {faq_count}")
print(f"FAQs loaded : {faqs_loaded}")

faq_topics = ["Password Reset", "Email Setup", "Billing Questions", "Technical Support"]
faq_urls = []

print("Abailable FAQ topics:")
for topic in faq_topics:
    print(f"- {topic}")

print(f"Number of topics: {len(faq_topics)}")