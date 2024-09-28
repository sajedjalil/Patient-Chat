import { chatMessages, userInput, sendButton } from './uiElements.js';
import { addMessage, updateAIMessage } from './messageHandler.js';
import { sendMessageToAPI } from './apiService.js';
import { fetchUserInfo } from './apiService.js';

let chatHistory = [];

async function loadUserInfo() {
    try {
        const userInfo = await fetchUserInfo();
        const userInfoElement = document.getElementById('user-info');
        userInfoElement.innerHTML = `
            <h1>${userInfo.first_name} ${userInfo.last_name}</h1>
            <p><strong>Date of Birth:</strong> ${userInfo.date_of_birth}</p>
            <p><strong>Phone:</strong> ${userInfo.phone_number}</p>
            <p><strong>Email:</strong> ${userInfo.email}</p>
            <p><strong>Medical Conditions:</strong> ${userInfo.medical_conditions}</p>
            <p><strong>Medication:</strong> ${userInfo.medication_regimen}</p>
            <p><strong>Last Appointment:</strong> ${userInfo.last_appointment}</p>
            <p><strong>Next Appointment:</strong> ${userInfo.next_appointment}</p>
            <p><strong>Doctor:</strong> ${userInfo.doctor_name}</p>
        `;
    } catch (error) {
        console.error('Failed to load user info:', error);
        // Optionally, display an error message to the user
    }
}

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

// Load user info when the page loads
loadUserInfo();