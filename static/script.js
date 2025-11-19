const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const questionInput = document.getElementById('questionInput');
const sendButton = document.getElementById('sendButton');
const historyButton = document.getElementById('historyButton');
const clearChatButton = document.getElementById('clearChatButton');

// Format text with markdown-like syntax for code blocks
function formatMessage(text) {
    // Convert markdown code blocks to HTML
    text = text.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
    
    // Convert inline code
    text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Convert line breaks
    text = text.replace(/\n/g, '<br>');
    
    return text;
}

// Add a message to the chat
function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const icon = document.createElement('div');
    icon.className = 'message-icon';
    icon.textContent = isUser ? '👤' : '🤖🎓';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.innerHTML = formatMessage(content);
    
    messageDiv.appendChild(icon);
    messageDiv.appendChild(messageContent);
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Show thinking indicator
function showThinking() {
    const thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'message bot-message thinking';
    thinkingDiv.id = 'thinking-indicator';
    
    const icon = document.createElement('div');
    icon.className = 'message-icon';
    icon.textContent = '🤖🎓';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.innerHTML = 'Thinking<span class="thinking-dots"><span>.</span><span>.</span><span>.</span></span>';
    
    thinkingDiv.appendChild(icon);
    thinkingDiv.appendChild(messageContent);
    
    chatMessages.appendChild(thinkingDiv);
    scrollToBottom();
}

// Remove thinking indicator
function removeThinking() {
    const thinkingDiv = document.getElementById('thinking-indicator');
    if (thinkingDiv) {
        thinkingDiv.remove();
    }
}

// Scroll to bottom of chat
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Load conversation history (for registered users only)
async function loadHistory() {
    try {
        const response = await fetch('/history');
        
        if (!response.ok) {
            if (response.status === 403) {
                addMessage('History is only available for registered users. Please create an account to save your conversations.', false);
                return;
            }
            throw new Error('Failed to load history');
        }
        
        const data = await response.json();
        
        if (data.conversations.length === 0) {
            addMessage('No saved conversations yet! Start chatting to build your history.', false);
            return;
        }
        
        // Clear current chat
        chatMessages.innerHTML = '';
        
        // Add header
        const headerDiv = document.createElement('div');
        headerDiv.className = 'message bot-message';
        headerDiv.innerHTML = `
            <div class="message-icon">📚</div>
            <div class="message-content">
                <strong>Your Conversation History (${data.count} saved conversations)</strong>
                <p style="font-size: 12px; margin-top: 5px; opacity: 0.8;">Click "Clear Chat" to start a new conversation</p>
            </div>
        `;
        chatMessages.appendChild(headerDiv);
        
        // Add all saved conversations
        data.conversations.forEach((conv, index) => {
            addMessage(conv.question, true);
            addMessage(conv.answer, false);
            
            // Add separator between conversations
            if (index < data.conversations.length - 1) {
                const separator = document.createElement('div');
                separator.style.borderTop = '1px solid #e0e0e0';
                separator.style.margin = '10px 0';
                chatMessages.appendChild(separator);
            }
        });
        
    } catch (error) {
        console.error('Error loading history:', error);
        addMessage('Failed to load conversation history. Please try again.', false);
    }
}

// Clear current chat display (not the saved history)
function clearChat() {
    chatMessages.innerHTML = '';
    
    // Add welcome message back
    const welcomeDiv = document.createElement('div');
    welcomeDiv.className = 'message bot-message';
    welcomeDiv.innerHTML = `
        <div class="message-icon">🤖🎓</div>
        <div class="message-content">
            <p>Hello! I'm your AI teaching assistant for INFO 6200. Ask me any questions about Python coding and course content!</p>
        </div>
    `;
    chatMessages.appendChild(welcomeDiv);
}

// Handle form submission
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const question = questionInput.value.trim();
    if (!question) return;
    
    // Add user message
    addMessage(question, true);
    
    // Clear input and disable button
    questionInput.value = '';
    sendButton.disabled = true;
    
    // Show thinking indicator
    showThinking();
    
    try {
        // Send question to server
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question })
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        
        // Remove thinking indicator
        removeThinking();
        
        // Add bot response
        addMessage(data.answer, false);
        
    } catch (error) {
        console.error('Error:', error);
        removeThinking();
        addMessage('I apologize, but I encountered an error. Please try again.', false);
    } finally {
        // Re-enable button and focus input
        sendButton.disabled = false;
        questionInput.focus();
    }
});

// History button event (only exists for registered users)
if (historyButton) {
    historyButton.addEventListener('click', loadHistory);
}

// Clear chat button event
clearChatButton.addEventListener('click', clearChat);

// Auto-focus on input when page loads
window.addEventListener('load', () => {
    questionInput.focus();
});
