// Chat functionality for the full chat page
class ChatInterface {
    constructor() {
        this.messagesContainer = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('message-input');
        this.sendButton = document.getElementById('send-button');
        this.init();
    }

    init() {
        // Focus on input when page loads
        this.messageInput.focus();
        
        // Scroll to bottom initially
        this.scrollToBottom();
    }

    async sendMessage() {
        const question = this.messageInput.value.trim();
        
        if (!question) return;

        // Disable input while processing
        this.setInputState(false);
        
        // Add user message to chat
        this.addUserMessage(question);
        
        // Clear input
        this.messageInput.value = '';
        
        // Show typing indicator
        const typingId = this.showTypingIndicator();
        
        try {
            // Send to bot API
            const response = await fetch('/api/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question })
            });

            const data = await response.json();
            
            // Remove typing indicator
            this.removeTypingIndicator(typingId);
            
            if (response.ok) {
                // Add bot response
                this.addBotResponse(data);
            } else {
                // Handle error
                this.addErrorMessage(data.error || 'Sorry, something went wrong.');
            }
            
        } catch (error) {
            console.error('Error:', error);
            this.removeTypingIndicator(typingId);
            this.addErrorMessage('Sorry, I\'m having trouble connecting. Please try again.');
        }
        
        // Re-enable input
        this.setInputState(true);
        this.messageInput.focus();
    }

    addUserMessage(message) {
        const messageGroup = document.createElement('div');
        messageGroup.className = 'message-group';
        
        messageGroup.innerHTML = `
            <div class="user-message">
                <div class="message-bubble user">
                    ${this.escapeHtml(message)}
                </div>
                <div class="message-time">${this.getCurrentTime()}</div>
            </div>
        `;
        
        this.messagesContainer.appendChild(messageGroup);
        this.scrollToBottom();
    }

    addBotResponse(data) {
        const messageGroup = document.createElement('div');
        messageGroup.className = 'message-group';
        
        let responseHtml = `
            <div class="bot-message">
                <div class="message-bubble bot">
                    ${this.escapeHtml(data.response)}
        `;
        
        // Add matches if available
        if (data.matches && data.matches.length > 0) {
            responseHtml += '<br><br>';
            data.matches.forEach(match => {
                responseHtml += `
                    <div class="match-card">
                        <div class="confidence">${match.score}% match</div>
                        <h3>${this.escapeHtml(match.question)}</h3>
                        <p class="answer">${this.escapeHtml(match.answer)}</p>
                    </div>
                `;
            });
        }
        
        responseHtml += `
                </div>
                <div class="message-time">${this.getCurrentTime()}</div>
            </div>
        `;
        
        messageGroup.innerHTML = responseHtml;
        this.messagesContainer.appendChild(messageGroup);
        this.scrollToBottom();
    }

    addErrorMessage(error) {
        const messageGroup = document.createElement('div');
        messageGroup.className = 'message-group';
        
        messageGroup.innerHTML = `
            <div class="bot-message">
                <div class="message-bubble bot" style="background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;">
                    ❌ ${this.escapeHtml(error)}
                </div>
                <div class="message-time">${this.getCurrentTime()}</div>
            </div>
        `;
        
        this.messagesContainer.appendChild(messageGroup);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        const typingId = 'typing-' + Date.now();
        const messageGroup = document.createElement('div');
        messageGroup.className = 'message-group';
        messageGroup.id = typingId;
        
        messageGroup.innerHTML = `
            <div class="bot-message">
                <div class="message-bubble bot">
                    <div class="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>
        `;
        
        this.messagesContainer.appendChild(messageGroup);
        this.scrollToBottom();
        
        return typingId;
    }

    removeTypingIndicator(typingId) {
        const element = document.getElementById(typingId);
        if (element) {
            element.remove();
        }
    }

    setInputState(enabled) {
        this.messageInput.disabled = !enabled;
        this.sendButton.disabled = !enabled;
        
        if (enabled) {
            this.sendButton.innerHTML = '<span class="send-icon">→</span>';
        } else {
            this.sendButton.innerHTML = '...';
        }
    }

    scrollToBottom() {
        setTimeout(() => {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }, 100);
    }

    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Handle Enter key press
function handleEnter(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        chat.sendMessage();
    }
}

// Handle send button click
function sendMessage() {
    chat.sendMessage();
}

// Initialize chat when page loads
let chat;
document.addEventListener('DOMContentLoaded', function() {
    chat = new ChatInterface();
});

// Add CSS for typing indicator
const style = document.createElement('style');
style.textContent = `
    .typing-indicator {
        display: flex;
        gap: 4px;
        align-items: center;
    }
    
    .typing-indicator span {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #adb5bd;
        animation: typing 1.4s ease-in-out infinite;
    }
    
    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typing {
        0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.5;
        }
        30% {
            transform: translateY(-10px);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);