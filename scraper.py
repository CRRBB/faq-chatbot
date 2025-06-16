import requests
from bs4 import BeautifulSoup
import json

url = "https://www.infomaniak.com/en/support/faq/admin2"
print(f"Connecting to: {url}")

response = requests.get(url)
print(f"Response status : {response.status_code}")

if response.status_code == 200:
    print("Successfully connected to Infomaniak FAQ!")
else:
    print("Failed to connect")

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('title')
    print(f"Page title: {title.text if title else 'No title found'}")

    links = soup.find_all('a')
    print(f"Found {len(links)} links on the page")

    print("\nFirst 5 links:")
    for i, link in enumerate(links[:5]):
        print(f"{i+1}. {link.get('href')} - {link.text.strip()}")

    # Clean extraction of FAQ categories
faq_categories = []
    
for link in links:
        href = link.get('href')
        text = link.text.strip()
        
        # Look specifically for FAQ category pages
        if href and '/support/faq/admin2/' in href and text and len(text) > 5:
            if href not in [item['url'] for item in faq_categories]:  # Avoid duplicates
                faq_categories.append({
                    'url': href,
                    'title': text
                })
    
print(f"\nFound {len(faq_categories)} FAQ categories:")
for i, faq in enumerate(faq_categories[:10]):
    print(f"{i+1}. {faq['title']}")
    print(f"   URL: {faq['url']}")
    print()

def scrape_faq_content(faq_url):
    """Scrape actual FAQ questions and answers from a specific FAQ page"""
    
    print(f"\n=== Scraping FAQ content from: {faq_url} ===")
    
    response = requests.get(faq_url)
    if response.status_code != 200:
        print(f"❌ Failed to access {faq_url}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Look for FAQ-specific patterns
    faq_items = []
    
    # Try different patterns for FAQ content
    # Pattern 1: Look for elements with "faq" in class name
    faq_elements = soup.find_all(class_=lambda x: x and 'faq' in x.lower())
    
    # Pattern 2: Look for question-like headings
    headings = soup.find_all(['h2', 'h3', 'h4'])
    
    for heading in headings:
        text = heading.text.strip()
        if '?' in text or len(text) > 20:  # Likely a question
            # Find the next paragraph or content
            next_content = heading.find_next(['p', 'div'])
            answer = next_content.text.strip() if next_content else "No answer found"
            
            if len(answer) > 20:  # Only keep substantial answers
                faq_items.append({
                    'question': text,
                    'answer': answer[:500] + "..." if len(answer) > 500 else answer
                })
    
    return faq_items

# Test with Email Service
email_faq_url = "https://www.infomaniak.com/en/support/faq/admin2/email-service"
faqs = scrape_faq_content(email_faq_url)

if faqs:
    print(f"Found {len(faqs)} FAQ questions:")
    for i, faq in enumerate(faqs[:3]):
        print(f"\n{i+1}. Q: {faq['question']}")
        print(f"   A: {faq['answer']}")
else:
    print("No FAQ questions found - might need to adjust scraping strategy")


if faqs:
    print(f"\n💾 Saving {len(faqs)} FAQs to data/faqs.json...")
    
    # Create data directory if it doesn't exist
    import os
    os.makedirs('data', exist_ok=True)
    
    # Save to JSON file in the format our bot expects
    with open('data/faqs.json', 'w', encoding='utf-8') as f:
        json.dump(faqs, f, indent=2, ensure_ascii=False)
    
    print("✅ FAQs saved successfully!")
    print("🤖 Your bot can now use this real data!")
else:
    print("❌ No FAQs to save")