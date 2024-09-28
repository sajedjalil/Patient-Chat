// apiService.js
import { getCookie } from './utils.js';

export async function sendMessageToAPI(message, chatHistory, userTimestamp) {
    const data = {
        userType: 'patient',
        message: message,
        history: chatHistory,
        timestamp: userTimestamp
    };

    const response = await fetch('/chat/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
}