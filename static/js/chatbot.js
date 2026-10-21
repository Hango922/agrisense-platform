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

        // 1. Format Choice Cards [choice:Title|Desc|Icon](query)
        escaped = escaped.replace(/\[choice:([^|]+)\|([^|]+)\|([^\]]+)\]\(([^\)]+)\)/g, function(_, title, desc, icon, query) {
            return `<button type="button" class="chat-choice-card" data-query="${query}">` +
                   `<span class="choice-icon">${icon.trim()}</span>` +
                   `<span class="choice-content">` +
                   `<span class="choice-title">${title.trim()}</span>` +
                   `<span class="choice-desc">${desc.trim()}</span>` +
                   `</span>` +
                   `<span class="choice-arrow"><i class="bi bi-chevron-right"></i></span>` +
                   `</button>`;
        });

        // 2. Format Choice Cards không có icon [choice:Title|Desc](query)
        escaped = escaped.replace(/\[choice:([^|]+)\|([^\]]+)\]\(([^\)]+)\)/g, function(_, title, desc, query) {
            return `<button type="button" class="chat-choice-card" data-query="${query}">` +
                   `<span class="choice-icon">⚡</span>` +
                   `<span class="choice-content">` +
                   `<span class="choice-title">${title.trim()}</span>` +
                   `<span class="choice-desc">${desc.trim()}</span>` +
                   `</span>` +
                   `<span class="choice-arrow"><i class="bi bi-chevron-right"></i></span>` +
                   `</button>`;
        });

        // 3. Tương thích định dạng cũ hoặc tin nhắn có kèm mô tả sau gạch ngang:
        // Ví dụ: 1️⃣ [button:💵 Thanh toán khi nhận hàng (COD)](COD) — Trả tiền mặt khi nhận hàng
        escaped = escaped.replace(/(?:[0-9]️⃣\s*)?\[button:([^\s\]]+(?:\s+[^\]]+)?)\]\(([^\)]+)\)(?:\s*(?:—|-|–)\s*([^\n<]+))?/g, function(full, label, query, desc) {
            label = label.trim();
            query = query.trim();
            let icon = '⚡';
            let title = label;
            const emojiMatch = label.match(/^(\p{Extended_Pictographic}|\p{Emoji})\s*(.*)$/u);
            if (emojiMatch) {
                icon = emojiMatch[1];
                title = emojiMatch[2];
            }
            if (desc && desc.trim()) {
                return `<button type="button" class="chat-choice-card" data-query="${query}">` +
                       `<span class="choice-icon">${icon}</span>` +
                       `<span class="choice-content">` +
                       `<span class="choice-title">${title}</span>` +
                       `<span class="choice-desc">${desc.trim()}</span>` +
                       `</span>` +
                       `<span class="choice-arrow"><i class="bi bi-chevron-right"></i></span>` +
                       `</button>`;
            }
            return `<button type="button" class="chat-quick-action" data-query="${query}"><i class="bi bi-cursor-fill me-1"></i>${label}</button>`;
        });

        // 4. Standalone action button [button:Label](query)
        escaped = escaped.replace(/\[button:(.*?)\]\(([^\)]+)\)/g, '<button type="button" class="chat-quick-action" data-query="$2"><i class="bi bi-cursor-fill me-1"></i>$1</button>');

        // 5. Format markdown bold **text**
        escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        // 6. Format markdown image ![alt](url)
        escaped = escaped.replace(/!\[(.*?)\]\(([^\)]+)\)/g, '<div class="text-center my-2"><img src="$2" alt="$1" class="img-fluid rounded border shadow-sm" style="max-width: 180px; background: #fff;" /><div class="small text-muted mt-1">$1</div></div>');

        // 7. Format markdown link [title](url) - chỉ áp dụng cho URL hợp lệ bắt đầu bằng / hoặc http/https
        escaped = escaped.replace(/\[(.*?)\]\(((?:https?:\/\/|\/(?:orders|products|cart|trace|accounts)[^\s\)]*)[^\)]*)\)/g, '<a href="$2" class="fw-bold text-success text-decoration-underline" target="_blank" rel="noopener noreferrer">$1</a>');

        // 8. Format newlines
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
            if (typeof updateArrowVisibility === 'function') {
                setTimeout(updateArrowVisibility, 150);
            }
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

    const closeBtn = document.getElementById('chatbot-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            widget.classList.remove('active');
        });
    }

    // ==============================================================
    // XỬ LÝ THANH GỢI Ý CHAT (KÉO RÊ CHUỘT, LĂN CHUỘT, NÚT CUỘN)
    // ==============================================================
    const chipsContainer = document.getElementById('chatbot-chips');
    const scrollLeftBtn = document.getElementById('chip-scroll-left');
    const scrollRightBtn = document.getElementById('chip-scroll-right');

    function updateArrowVisibility() {
        if (!chipsContainer || !scrollLeftBtn || !scrollRightBtn) return;
        const canScrollLeft = chipsContainer.scrollLeft > 6;
        const canScrollRight = chipsContainer.scrollLeft < (chipsContainer.scrollWidth - chipsContainer.clientWidth - 6);
        scrollLeftBtn.style.display = canScrollLeft ? 'inline-flex' : 'none';
        scrollRightBtn.style.display = canScrollRight ? 'inline-flex' : 'none';
    }

    if (chipsContainer) {
        let isDown = false;
        let startX = 0;
        let scrollLeftPos = 0;
        let hasMoved = false;

        // 1. Kéo rê chuột qua lại (Mouse Drag-to-Scroll)
        chipsContainer.addEventListener('mousedown', (e) => {
            isDown = true;
            hasMoved = false;
            chipsContainer.classList.add('is-dragging');
            startX = e.pageX - chipsContainer.offsetLeft;
            scrollLeftPos = chipsContainer.scrollLeft;
        });

        window.addEventListener('mouseup', () => {
            if (isDown) {
                isDown = false;
                chipsContainer.classList.remove('is-dragging');
            }
        });

        chipsContainer.addEventListener('mouseleave', () => {
            if (isDown) {
                isDown = false;
                chipsContainer.classList.remove('is-dragging');
            }
        });

        chipsContainer.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            const x = e.pageX - chipsContainer.offsetLeft;
            const walk = (x - startX) * 1.5;
            if (Math.abs(walk) > 4) {
                hasMoved = true;
            }
            chipsContainer.scrollLeft = scrollLeftPos - walk;
            updateArrowVisibility();
        });

        // 2. Cuộn con lăn chuột ngang tự nhiên (Wheel scroll)
        chipsContainer.addEventListener('wheel', (e) => {
            if (e.deltaY !== 0) {
                e.preventDefault();
                chipsContainer.scrollLeft += e.deltaY;
                updateArrowVisibility();
            }
        }, { passive: false });

        // 3. Nút cuộn trái & phải
        if (scrollLeftBtn) {
            scrollLeftBtn.addEventListener('click', (e) => {
                e.preventDefault();
                chipsContainer.scrollBy({ left: -140, behavior: 'smooth' });
                setTimeout(updateArrowVisibility, 300);
            });
        }
        if (scrollRightBtn) {
            scrollRightBtn.addEventListener('click', (e) => {
                e.preventDefault();
                chipsContainer.scrollBy({ left: 140, behavior: 'smooth' });
                setTimeout(updateArrowVisibility, 300);
            });
        }

        chipsContainer.addEventListener('scroll', updateArrowVisibility);
        setTimeout(updateArrowVisibility, 250);

        // 4. Bấm vào Chip: Nếu đang kéo rê chuột thì bỏ qua click, nếu bấm thông thường thì gửi tin
        chipsContainer.addEventListener('click', (e) => {
            if (hasMoved) {
                e.preventDefault();
                e.stopPropagation();
                hasMoved = false;
                return;
            }
            const chip = e.target.closest('.chip-btn');
            if (chip) {
                const query = chip.getAttribute('data-query');
                if (query && input) {
                    input.value = query;
                    sendMessage();
                }
            }
        });
    }

    // Xử lý khi nhấn vào Choice Card hoặc Quick Action bên trong tin nhắn bot
    messages.addEventListener('click', (e) => {
        // 1. Nhấp vào Choice Card (COD, VietQR, v.v.)
        const choiceCard = e.target.closest('.chat-choice-card');
        if (choiceCard) {
            e.preventDefault();
            const query = choiceCard.getAttribute('data-query');
            if (query && input) {
                input.value = query;
                sendMessage();
            }
            return;
        }

        // 2. Nhấp vào Quick Action Button
        const btn = e.target.closest('.chat-quick-action');
        if (btn) {
            e.preventDefault();
            const query = btn.getAttribute('data-query');
            if (query && input) {
                input.value = query;
                sendMessage();
            }
            return;
        }

        // 3. Đảm bảo không bao giờ điều hướng sang URL /COD hoặc /VietQR nếu lỡ click vào liên kết
        const link = e.target.closest('a');
        if (link) {
            const href = (link.getAttribute('href') || '').trim();
            const text = (link.textContent || '').trim();
            if (href === 'COD' || href === '/COD' || href.toLowerCase() === 'cod' || href.toLowerCase() === '/cod') {
                e.preventDefault();
                if (input) {
                    input.value = 'COD';
                    sendMessage();
                }
                return;
            }
            if (href.includes('VietQR') || text.includes('VietQR')) {
                e.preventDefault();
                if (input) {
                    input.value = 'Chuyển khoản VietQR';
                    sendMessage();
                }
                return;
            }
        }
    });

    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        // 1. Hiển thị tin nhắn người dùng ngay lập tức
        messages.innerHTML += `<div class="chat-msg user">${escapeHtml(text)}</div>`;
        input.value = '';

        // 2. Hiển thị hiệu ứng AI đang soạn thảo với 3 chấm nhịp điệu (Wave)
        const typingId = 'typing-' + Date.now();
        messages.innerHTML += `
            <div class="chat-msg bot" id="${typingId}">
                <div class="d-flex align-items-center gap-2">
                    <span class="typing-wave">
                        <span class="typing-dot"></span>
                        <span class="typing-dot"></span>
                        <span class="typing-dot"></span>
                    </span>
                    <span class="small text-muted">Trợ lý AI đang soạn câu trả lời...</span>
                </div>
            </div>`;
        scrollToBottom();

        // 3. Khóa nút gửi tạm thời
        if (send) {
            send.disabled = true;
            send.innerHTML = '<i class="bi bi-hourglass-split" style="font-size: 13px;"></i>';
        }
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
            if (send) {
                send.disabled = false;
                send.innerHTML = '<i class="bi bi-send-fill" style="font-size: 14px;"></i>';
            }
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
