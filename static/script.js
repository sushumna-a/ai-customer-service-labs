let totalQueries = 0;

function sendQuery() {
    let input = document.getElementById('user-input');
    let query = input.value.trim();
    if (!query) return;
    appendMessage('user', query);
    input.value = '';
    fetch('/predict', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({query: query})
    })
    .then(response => response.json())
    .then(data => {
        let entities = data.entities.map(e => `<span class="entity">${e.text} (${e.label})</span>`).join(', ');
        let botMsg = `<b>Intent:</b> ${data.intent}<br><b>Entities:</b> ${entities || 'None'}`;
        appendMessage('bot', botMsg);
        totalQueries++;
        document.getElementById('total-queries').innerText = totalQueries;
        document.getElementById('recent-intent').innerText = data.intent;
    });
}

function appendMessage(sender, text) {
    let chatBox = document.getElementById('chat-box');
    let msgClass = sender === 'user' ? 'user-msg' : 'bot-msg';
    chatBox.innerHTML += `<div class="${msgClass}">${text}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}

function quickQuery(text) {
    document.getElementById('user-input').value = text;
    sendQuery();
}

document.getElementById('user-input').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') sendQuery();
});
