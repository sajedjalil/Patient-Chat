// main.js
import { userInput, sendButton } from './uiElements.js';
import { addMessage, updateAIMessage } from './messageHandler.js';
import { sendMessageToAPI } from './apiService.js';

let chatHistory = [];

async function sendMessage() {
    const message = userInput.value.trim();
    if (message) {
        const userTimestamp = Date.now();
        addMessage(message, true, userTimestamp);
        userInput.value = '';

        chatHistory.push({ role: 'user', content: message });

        const aiMessageElement = addMessage('', false, null);

        try {
            const responseData = await sendMessageToAPI(message, chatHistory, userTimestamp);
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

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});