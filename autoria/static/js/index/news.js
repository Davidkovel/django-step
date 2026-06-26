/* ===== Табки новин (візуальне перемикання) ===== */
document.querySelectorAll('.news-tab').forEach(tab => {
    tab.addEventListener('click', function() {
        document.querySelectorAll('.news-tab').forEach(t => t.classList.remove('news-tab--active'));
        this.classList.add('news-tab--active');
    });
});

/* ===== Табки AUTO.RIA рекомендує ===== */
function switchRia(btn, panel) {
    btn.closest('.ria-tabs').querySelectorAll('.transport-tab').forEach(t => t.classList.remove('transport-tab--active'));
    btn.classList.add('transport-tab--active');
    document.querySelectorAll('.ria-panel').forEach(p => p.classList.remove('ria-panel--active'));
    document.querySelector(`[data-ria="${panel}"]`).classList.add('ria-panel--active');
}