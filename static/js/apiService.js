// apiService.js
import { getCookie } from './utils.js';

export async function sendMessageToAPI(message, chatHistory, userTimestamp, threadId) {
    const data = {
        userType: 'patient',
        message: message,
        history: chatHistory,
        timestamp: userTimestamp,
        threadId: threadId
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

export async function fetchUserInfo() {
    try {
        const response = await fetch('/user-info/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching user info:', error);
        throw error;
    }
}


export async function fetchThreadId() {
    try {
        const response = await fetch('/thread-id/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching user info:', error);
        throw error;
    }
}