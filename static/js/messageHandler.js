// messageHandler.js
import { chatMessages } from './uiElements.js';
import { formatTimestamp } from './utils.js';

export function addMessage(message, isUser, timestamp) {
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

export function updateAIMessage(messageElement, content, timestamp) {
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