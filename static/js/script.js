const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

let chatHistory = [];

function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    let dateString;
    if (date.toDateString() === today.toDateString()) {
        dateString = 'Today';
    } else if (date.toDateString() === yesterday.toDateString()) {
        dateString = 'Yesterday';
    } else {
        dateString = date.toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' });
    }

    const timeString = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    return `${dateString} at ${timeString}`;
}

function addMessage(message, isUser, timestamp) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add(isUser ? 'user-message' : 'ai-message');

    const formattedTimestamp = formatTimestamp(timestamp);

    if (isUser) {
        messageElement.innerHTML = `
            <div class="message-content">${marked.parse(message)}</div>
            <div class="timestamp">${formattedTimestamp}</div>
        `;
    } else {
        messageElement.innerHTML = '<div class="typing-indicator">AI is typing...</div>';
    }

    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return messageElement;
}

function updateAIMessage(messageElement, content, timestamp) {
    const typingIndicator = messageElement.querySelector('.typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
    const formattedTimestamp = formatTimestamp(timestamp);
    messageElement.innerHTML = `
        <div class="message-content">${marked.parse(content)}</div>
        <div class="timestamp">${formattedTimestamp}</div>
    `;
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (message) {
        const userTimestamp = Date.now();
        addMessage(message, true, userTimestamp);
        userInput.value = '';

        chatHistory.push({ role: 'user', content: message });

        const data = {
            userType: 'patient',
            message: message,
            history: chatHistory,
            timestamp: userTimestamp
        };

        const aiMessageElement = addMessage('', false, null);

        try {
            const response = await fetch('/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')  // Add this line for CSRF protection
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const responseData = await response.json();
            const aiMessage = responseData.response;
            const aiTimestamp = responseData.ai_timestamp;
            updateAIMessage(aiMessageElement, aiMessage, aiTimestamp);

            chatHistory.push({ role: 'assistant', content: aiMessage });

        } catch (error) {
            console.error('Error:', error);
            updateAIMessage(aiMessageElement, "Sorry, there was an error processing your request.", Date.now());
        }
    }
}

// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});