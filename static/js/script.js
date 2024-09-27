const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

let chatHistory = [];

function addMessage(message, isUser) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add(isUser ? 'user-message' : 'ai-message');

    if (isUser) {
        messageElement.innerHTML = marked.parse(message);
    } else {
        messageElement.innerHTML = '<div class="typing-indicator">AI is typing...</div>';
    }

    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return messageElement;
}

function updateAIMessage(messageElement, content) {
    const typingIndicator = messageElement.querySelector('.typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
    messageElement.innerHTML = marked.parse(content);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (message) {
        addMessage(message, true);
        userInput.value = '';

        // Add user message to chat history
        chatHistory.push({ role: 'user', content: message });

        const data = {
            userType: 'patient',
            message: message,
            history: chatHistory
        };

        const aiMessageElement = addMessage('', false);

        try {
            const response = await fetch('/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const responseData = await response.json();
            const aiMessage = responseData.response;
            updateAIMessage(aiMessageElement, aiMessage);

            // Add AI message to chat history
            chatHistory.push({ role: 'assistant', content: aiMessage });

        } catch (error) {
            console.error('Error:', error);
            updateAIMessage(aiMessageElement, "Sorry, there was an error processing your request.");
        }
    }
}

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});