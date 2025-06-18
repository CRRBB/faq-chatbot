// Chat plugin functionality for homepage
class ChatPlugin {
    constructor() {
        this.plugin = document.getElementById('chat-plugin');
        this.floatBtn = document.getElementById('chat-float-btn');
        this.messagesContainer = document.getElementById('plugin-messages');
        this.input = document.getElementById('plugin-input');
        this.isOpen = false;
    }

    async sendMessage(message) {
        if (!message) {
            message = this.input.value.trim();
        }
        
        if (!message) return;

        // Add user message
        this.addUserMessage(message);
        
        // Clear input if it was typed (not clicked from sample)
        if (!arguments[0]) {
            this.input.value = '';
        }
        
        // Show typing
        const typingId = this.showTypingIndicator();
        
        try {
            const response = await fetch('/api/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: message })
            });

            const data = await response.json();
            
            this.removeTypingIndicator(typingId);
            
            if (response.ok) {
                this.addBotResponse(data);
            } else {
                this.addErrorMessage(data.error || 'Sorry, something went wrong.');
            }
            
        } catch (error) {
            console.error('Error:', error);
            this.removeTypingIndicator(typingId);
            this.addErrorMessage('Sorry, I\'m having trouble connecting.');
        }
    }

    addUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'user-message';
        messageDiv.innerHTML = '<div class="message-bubble user">' + this.escapeHtml(message) + '</div>';
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    addBotResponse(data) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'bot-message';
        
        let responseHtml = '<div class="message-bubble bot">';
        
        // Add first match only (plugin space is limited)
        if (data.matches && data.matches.length > 0) {
            const match = data.matches[0];
            
            responseHtml += '<div style="background: #f8f9fa; padding: 12px; border-radius: 8px; margin-top: 8px;">';
            responseHtml += '<div style="background: #667eea; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.75em; display: inline-block; margin-bottom: 8px; font-weight: 600;">';
            responseHtml += match.score + '% match';
            responseHtml += '</div>';
            responseHtml += '<div style="font-weight: 600; margin-bottom: 8px; font-size: 0.9em; color: #333;">';
            responseHtml += this.escapeHtml(match.question);
            responseHtml += '</div>';
            responseHtml += '<div style="font-size: 0.85em; color: #555; line-height: 1.4;">';
            responseHtml += this.escapeHtml(match.answer);
            responseHtml += '</div>';
            responseHtml += '</div>';
            
            if (data.matches.length > 1) {
                responseHtml += '<div style="margin-top: 10px; text-align: center;">';
                responseHtml += '<a href="/chat" style="color: #667eea; font-size: 0.8em; text-decoration: none; font-weight: 500;">';
                responseHtml += 'View ' + (data.matches.length - 1) + ' more result(s) in full chat →';
                responseHtml += '</a>';
                responseHtml += '</div>';
            }
        } else {
            // No matches found - show the error message
            responseHtml += this.escapeHtml(data.response);
        }
        
        responseHtml += '</div>';
        messageDiv.innerHTML = responseHtml;
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    addErrorMessage(error) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'bot-message';
        messageDiv.innerHTML = '<div class="message-bubble bot" style="background: #f8d7da; color: #721c24;">❌ ' + this.escapeHtml(error) + '</div>';
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        const typingId = 'plugin-typing-' + Date.now();
        const messageDiv = document.createElement('div');
        messageDiv.className = 'bot-message';
        messageDiv.id = typingId;
        messageDiv.innerHTML = '<div class="message-bubble bot"><div class="typing-indicator"><span></span><span></span><span></span></div></div>';
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        return typingId;
    }

    removeTypingIndicator(typingId) {
        const element = document.getElementById(typingId);
        if (element) {
            element.remove();
        }
    }

    scrollToBottom() {
        setTimeout(() => {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }, 100);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    open() {
        this.plugin.classList.add('active');
        this.floatBtn.style.display = 'none';
        this.isOpen = true;
        setTimeout(() => {
            this.input.focus();
        }, 300);
    }

    close() {
        this.plugin.classList.remove('active');
        this.floatBtn.style.display = 'block';
        this.isOpen = false;
    }
}

// Global functions for HTML onclick events
let chatPlugin;

function openChatPlugin() {
    if (!chatPlugin) {
        chatPlugin = new ChatPlugin();
    }
    chatPlugin.open();
}

function closeChatPlugin() {
    if (chatPlugin) {
        chatPlugin.close();
    }
}

function sendPluginMessage() {
    if (chatPlugin) {
        chatPlugin.sendMessage();
    }
}

function handlePluginEnter(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendPluginMessage();
    }
}

function askSample(question) {
    // Open plugin if not open
    openChatPlugin();
    
    // Wait for plugin to open, then send message
    setTimeout(() => {
        if (chatPlugin) {
            chatPlugin.sendMessage(question);
        }
    }, 400);
}