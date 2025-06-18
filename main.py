from flask import Flask, render_template, request, jsonify
from bot_engine import BotEngine

app = Flask(__name__)

# Create bot instance
bot = BotEngine()
bot.load_faq_data('data/faqs.json')

@app.route('/')
def homepage():
    """English homepage"""
    return render_template('homepage.html', lang='en')

@app.route('/fr')
def homepage_fr():
    """French homepage"""
    return render_template('homepage_fr.html', lang='fr')

@app.route('/chat')
def chat_page():
    """English chat page"""
    return render_template('chat.html', lang='en')

@app.route('/chat/fr')
def chat_page_fr():
    """French chat page"""
    return render_template('chat_fr.html', lang='fr')

@app.route('/api/ask', methods=['POST'])
def api_ask():
    """API endpoint for chatbot - returns JSON"""
    data = request.get_json()
    user_question = data.get('question', '')
    
    if not user_question:
        return jsonify({'error': 'No question provided'}), 400
    
    # Use your existing bot logic
    result = bot.get_answer(user_question)
    
    return jsonify({
        'question': user_question,
        'response': result['response'],
        'matches': result['matches'],
        'language': result['language']
    })

@app.route('/demo')
def demo_page():
    """Demo page showing plugin integration"""
    return render_template('demo.html')

if __name__ == '__main__':
    app.run(debug=True)