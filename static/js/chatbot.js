// File: static/js/chatbot.js
document.addEventListener('DOMContentLoaded', function() {
    const widget = document.getElementById('chatbot-widget');
    const toggle = document.getElementById('chatbot-toggle');
    const input = document.getElementById('chatbot-input');
    const send = document.getElementById('chatbot-send');
    const messages = document.getElementById('chatbot-messages');

    if (!widget || !toggle) return;

    toggle.addEventListener('click', () => widget.classList.toggle('active'));

    function getCookie(name) {
        const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return v ? v.pop() : '';
    }

    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        messages.innerHTML += `<div class="chat-msg user">${text}</div>`;
        input.value = '';

        try {
            const resp = await fetch('/chatbot/send/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') || document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '',
                },
                body: JSON.stringify({message: text}),
            });
            const data = await resp.json();
            messages.innerHTML += `<div class="chat-msg bot">${data.reply}</div>`;
        } catch (e) {
            messages.innerHTML += `<div class="chat-msg bot">Xin lỗi, có lỗi xảy ra.</div>`;
        }
        messages.scrollTop = messages.scrollHeight;
    }

    if (send) {
        send.addEventListener('click', sendMessage);
    }
    if (input) {
        input.addEventListener('keypress', e => { if (e.key === 'Enter') sendMessage(); });
    }
});
