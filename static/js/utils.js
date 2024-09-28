// utils.js
export function formatTimestamp(timestamp) {
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

export function getCookie(name) {
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