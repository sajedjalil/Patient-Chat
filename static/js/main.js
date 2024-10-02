import {
  userInfoElement, userInput, sendButton, conversationSummary, actions, medicalInsights
} from './uiElements.js';
import { addMessage, updateAIMessage } from './messageHandler.js';
import {sendMessageToAPI, fetchUserInfo, fetchThreadId, sendInsightAPI} from './apiService.js';

let chatHistory = [];
let threadId = null;

const loadUserInfo = async () => {
  try {
    const userInfo = await fetchUserInfo();
    userInfoElement.innerHTML = `
      <h1>${userInfo.first_name} ${userInfo.last_name}</h1>
      ${['date_of_birth', 'phone_number', 'email', 'medical_conditions', 'medication_regimen', 'last_appointment', 'next_appointment', 'doctor_name']
        .map(key => `<p><strong>${key.replace('_', ' ').charAt(0).toUpperCase() + key.slice(1).replace('_', ' ')}:</strong> ${userInfo[key]}</p>`)
        .join('')}
    `;
  } catch (error) {
    console.error('Failed to load user info:', error);
  }
};

const saveThreadId = async () => {
  try {
    const response = await fetchThreadId();
    threadId = response.thread_id;
  } catch (error) {
    console.error('Failed to get thread id:', error);
  }
};

const sendMessage = async () => {
  const message = userInput.value.trim();
  if (!message) return;

  const userTimestamp = Date.now();
  addMessage(message, true, userTimestamp);
  userInput.value = '';

  chatHistory.push({ role: 'user', content: message });

  const aiMessageElement = addMessage('', false, null);

  try {
    // Run both API calls in parallel
    const [responseData, insightResponse] = await Promise.all([
      sendMessageToAPI(message, chatHistory, userTimestamp, threadId),
      sendInsightAPI(message)
    ]);

    updateAIMessage(aiMessageElement, responseData.response, responseData.ai_timestamp);
    conversationSummary.innerText = responseData.summary;
    medicalInsights.innerText = insightResponse.insight;
    updateActionsCards(responseData.tools);

    chatHistory.push({ role: 'assistant', content: responseData.response });
    insightResponse
  } catch (error) {
    console.error('Error:', error);
    updateAIMessage(aiMessageElement, "Sorry, there was an error processing your request.", Date.now());
  }
};

const updateActionsCards = (tools) => {
  actions.innerHTML = tools && tools.length
    ? tools.map(tool => `
      <div class="actions-card">
        <div class="actions-card-icon">&#128295;</div>
        <div class="actions-card-text">${tool}</div>
      </div>
    `).join('')
    : '<div class="actions-card no-actions">No actions available.</div>';
};

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => e.key === 'Enter' && sendMessage());

// Initializers
(async () => {
  await loadUserInfo();
  await saveThreadId();
})();