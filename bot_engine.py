import json
from fuzzywuzzy import fuzz

class BotEngine:
    def __init__(self):
        self.faq_data = []
        print("BotEngine initialized")
    
    def load_faq_data(self, json_file_path):
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                self.faq_data = json.load(file)
            print(f"✅ Loaded {len(self.faq_data)} FAQ entries")
        except FileNotFoundError:
            print(f"❌ Error: Could not find {json_file_path}")
            self.faq_data = []
        except json.JSONDecodeError:
            print("❌ Error: Invalid JSON format")
            self.faq_data = []

    def detect_language(self, text):
        
        text = text.lower()
        words = text.split()
        
        french_indicators = [
            "comment", "où", "que", "qu", "le", "la", "les", "un", "une", 
            "de", "du", "des", "mon", "ma", "mes", "dans", "avec", "pour",
            "je", "puis", "suis", "est", "sont", "réinitialiser", "mot"
        ]
        
        english_indicators = [
            "how", "what", "where", "when", "the", "a", "an", "my", "your",
            "in", "on", "with", "for", "do", "can", "is", "are", "reset",
            "password", "i", "you", "we", "they"
        ]
        
        french_count = sum(1 for word in words if word in french_indicators)
        english_count = sum(1 for word in words if word in english_indicators)
        
        if french_count > english_count:
            return "french"
        elif english_count > french_count:
            return "english"
        else:
            return "french"


    def find_best_matches(self, user_question, num_results=3):
        if not self.faq_data:
            return []
        
        # Calculate similarity scores for all FAQs
        matches = []
        for faq in self.faq_data:
            similarity = fuzz.ratio(user_question.lower(), faq["question"].lower())
            match_data = {
                "question": faq["question"],
                "answer": faq["answer"], 
                "score": similarity
            }

            if "url" in faq:
                match_data["url"] = faq["url"]

            
            matches.append(match_data)


        # Sort by score (highest first) and filter by minimum threshold
        matches.sort(key=lambda x: x["score"], reverse=True)
        good_matches = [match for match in matches if match["score"] >= 70]
        return good_matches[:num_results]
    
    
    def get_answer(self, user_question):
        # Detect language (for future multilingual features)
        language = self.detect_language(user_question)
        
        # Find best matches
        matches = self.find_best_matches(user_question)
        
        # Format response
        if not matches:
            if language == "french":
                error_msg = "Désolé, je n'ai pas trouvé de réponse pertinente à votre question. Essayez de reformuler avec des mots-clés comme 'email', 'mot de passe', 'configuration', ou 'problème'."
            else:
                error_msg = "Sorry, I couldn't find a good answer to your question. Could you try rephrasing it?"

            return {
                "language": language,
                "response": error_msg,
                "matches": []
            }

        response_msg = f"I found {len(matches)} relevant answer(s):" if language == "english" else f"J'ai trouvé {len(matches)} réponse(s) pertinente(s):"
    
        return {
            "language": language,
            "response": response_msg,
            "matches": matches
        }