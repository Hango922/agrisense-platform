// File: static/js/chatbot.js
document.addEventListener('DOMContentLoaded', function() {
    const widget = document.getElementById('chatbot-widget');
    const toggle = document.getElementById('chatbot-toggle');
    const input = document.getElementById('chatbot-input');
    const send = document.getElementById('chatbot-send');
    const messages = document.getElementById('chatbot-messages');
    const clearBtn = document.getElementById('chatbot-clear');

    if (!widget || !toggle || !messages) return;

    function getCookie(name) {
        const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return v ? v.pop() : '';
    }

    function getCsrfToken() {
        return getCookie('csrftoken') || document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
    }

    function escapeHtml(str) {
        if (!str) return '';
        return str.replace(/[&<>"']/g, function(m) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m];
        });
    }

    function formatBotMessage(text) {
        if (!text) return '';
        let escaped = escapeHtml(text);
        // Format markdown bold
        escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Format markdown link [title](url)
        escaped = escaped.replace(/\[(.*?)\]\(((?:\/|[a-zA-Z0-9#_.-]+)[^\)]*)\)/g, '<a href="$2" class="fw-bold text-success text-decoration-underline">$1</a>');
        // Format newlines
        escaped = escaped.replace(/\n/g, '<br>');
        return escaped;
    }

    function scrollToBottom() {
        messages.scrollTop = messages.scrollHeight;
    }

    // Tải lịch sử đoạn chat từ phiên làm việc
    async function loadChatHistory() {
        try {
            const resp = await fetch('/chatbot/messages/', {
                method: 'GET',
                headers: { 'Accept': 'application/json' }
            });
            if (resp.ok) {
                const data = await resp.json();
                if (data.messages && data.messages.length > 0) {
                    messages.innerHTML = '';
                    data.messages.forEach(m => {
                        if (m.role === 'user') {
                            messages.innerHTML += `<div class="chat-msg user">${escapeHtml(m.content)}</div>`;
                        } else if (m.role === 'assistant') {
                            messages.innerHTML += `<div class="chat-msg bot">${formatBotMessage(m.content)}</div>`;
                        }
                    });
                    scrollToBottom();
                }
            }
        } catch (e) {
            console.error('Không thể tải lịch sử chat:', e);
        }
    }

    // Tải lịch sử ngay khi trang sẵn sàng
    loadChatHistory();

    toggle.addEventListener('click', () => {
        widget.classList.toggle('active');
        if (widget.classList.contains('active')) {
            scrollToBottom();
            if (input) input.focus();
        }
    });

    if (clearBtn) {
        clearBtn.addEventListener('click', async (e) => {
            e.stopPropagation();
            if (confirm('Bạn có muốn xóa cuộc trò chuyện này để bắt đầu lại không?')) {
                try {
                    await fetch('/chatbot/clear/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCsrfToken(),
                        }
                    });
                    messages.innerHTML = '<div class="chat-msg bot">Xin chào! Tôi có thể giúp bạn tìm nông sản sạch hoặc giải đáp thắc mắc gì?</div>';
                    scrollToBottom();
                } catch (err) {
                    console.error('Lỗi khi xóa lịch sử chat:', err);
                }
            }
        });
    }

    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        // 1. Hiển thị tin nhắn người dùng ngay lập tức
        messages.innerHTML += `<div class="chat-msg user">${escapeHtml(text)}</div>`;
        input.value = '';

        // 2. Hiển thị hiệu ứng AI đang suy nghĩ
        const typingId = 'typing-' + Date.now();
        messages.innerHTML += `<div class="chat-msg bot typing" id="${typingId}">🌾 Đang suy nghĩ câu trả lời...</div>`;
        scrollToBottom();

        // 3. Khóa nút gửi tạm thời
        if (send) { send.disabled = true; send.innerText = '...'; }
        if (input) { input.disabled = true; }

        try {
            const resp = await fetch('/chatbot/send/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({ message: text }),
            });

            const typingEl = document.getElementById(typingId);
            if (typingEl) typingEl.remove();

            if (resp.ok) {
                const data = await resp.json();
                messages.innerHTML += `<div class="chat-msg bot">${formatBotMessage(data.reply)}</div>`;
            } else {
                messages.innerHTML += `<div class="chat-msg bot text-danger">Xin lỗi, máy chủ chưa phản hồi. Bạn vui lòng thử lại!</div>`;
            }
        } catch (e) {
            const typingEl = document.getElementById(typingId);
            if (typingEl) typingEl.remove();
            messages.innerHTML += `<div class="chat-msg bot text-danger">Có lỗi kết nối. Bạn vui lòng kiểm tra lại mạng!</div>`;
        } finally {
            if (send) { send.disabled = false; send.innerText = 'Gửi'; }
            if (input) {
                input.disabled = false;
                input.focus();
            }
            scrollToBottom();
        }
    }

    if (send) {
        send.addEventListener('click', sendMessage);
    }
    if (input) {
        input.addEventListener('keypress', e => {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendMessage();
            }
        });
    }
});
