import { getCookie } from './utils.js';

const BASE_URL = '';  // Add your base URL here if needed

const handleResponse = async (response) => {
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

const fetchWithErrorHandling = async (url, options = {}) => {
  try {
    const response = await fetch(BASE_URL + url, options);
    return await handleResponse(response);
  } catch (error) {
    console.error(`Error fetching ${url}:`, error);
    throw error;
  }
};

export const sendMessageToAPI = async (message, chatHistory, userTimestamp, threadId) => {
  const [lastElement, ...historyWithoutLast] = [...chatHistory].reverse();
  
  const data = {
    userType: 'patient',
    message,
    history: historyWithoutLast.reverse(),
    timestamp: userTimestamp,
    threadId
  };

  return fetchWithErrorHandling('/chat/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(data)
  });
};


export const sendInsightAPI = async (message) => {
  const data = {
    message: message
  };

  return fetchWithErrorHandling('/insight/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(data)
  });
};

export const fetchUserInfo = () => fetchWithErrorHandling('/user-info/');

export const fetchThreadId = () => fetchWithErrorHandling('/thread-id/');