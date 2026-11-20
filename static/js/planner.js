(() => {
    const requestForm = document.getElementById('planner-request');
    const requestButton = requestForm?.querySelector('button[type="submit"]');
    if (requestButton) {
        const originalLabel = requestButton.innerHTML;
        requestForm.addEventListener('submit', () => {
            requestButton.disabled = true;
            requestButton.textContent = 'AI đang chuẩn bị gợi ý…';
            requestForm.setAttribute('aria-busy', 'true');
        });
        window.addEventListener('pageshow', () => {
            requestButton.disabled = false;
            requestButton.innerHTML = originalLabel;
            requestForm.removeAttribute('aria-busy');
        });
    }
    const form = document.getElementById('plan-selection');
    if (!form) return;
    const format = value => new Intl.NumberFormat('vi-VN').format(value) + 'đ';
    const update = () => {
        let subtotal = 0;
        form.querySelectorAll('[data-price]').forEach(input => {
            subtotal += Number(input.dataset.price) * Math.max(0, Number(input.value) || 0);
        });
        const shipping = subtotal && subtotal < 500000 ? 30000 : 0;
        const remaining = Number(form.dataset.budget) - subtotal - shipping;
        document.getElementById('plan-subtotal').textContent = format(subtotal);
        document.getElementById('plan-shipping').textContent = format(shipping);
        document.getElementById('plan-total').textContent = format(subtotal + shipping);
        document.getElementById('plan-remaining').textContent = remaining >= 0 ? `Còn ${format(remaining)} trong ngân sách` : `Vượt ngân sách ${format(-remaining)}`;
        document.getElementById('plan-add').disabled = remaining < 0 || subtotal <= 0;
    };
    form.addEventListener('input', update);
    update();
})();
