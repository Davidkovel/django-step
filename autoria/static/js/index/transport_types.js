/* ===== Перемикання табок транспорту ===== */
function switchTransport(btn, panel) {
    document.querySelectorAll('.transport-tab').forEach(t => t.classList.remove('transport-tab--active'));
    btn.classList.add('transport-tab--active');
    document.querySelectorAll('.transport-panel').forEach(p => p.classList.remove('transport-panel--active'));
    document.querySelector(`[data-panel="${panel}"]`).classList.add('transport-panel--active');
}

/* ===== Рейтинг зірками ===== */
(function initRating() {
    const container = document.getElementById('ratingStars');
    if (!container) return;
    const stars = [...container.querySelectorAll('.star-item')];
    let fixedRating = 0;

    container.addEventListener('mouseover', function(e) {
        const star = e.target.closest('.star-item');
        if (!star) return;
        const val = parseInt(star.dataset.value);
        stars.forEach(s => {
            const v = parseInt(s.dataset.value);
            s.classList.toggle('hovered', v <= val && v > fixedRating);
        });
    });

    container.addEventListener('mouseout', function() {
        stars.forEach(s => s.classList.remove('hovered'));
    });

    container.addEventListener('click', function(e) {
        const star = e.target.closest('.star-item');
        if (!star) return;
        fixedRating = parseInt(star.dataset.value);
        stars.forEach(s => {
            const v = parseInt(s.dataset.value);
            s.classList.toggle('active', v <= fixedRating);
            s.classList.remove('hovered');
        });
    });
})();