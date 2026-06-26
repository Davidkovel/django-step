(function initHistoryRating() {
    var container = document.getElementById('historyStars');
    if (!container) return;
    var stars = [].slice.call(container.querySelectorAll('.history-star'));
    var fixedRating = 0;

    container.addEventListener('mouseover', function(e) {
        var star = e.target.closest('.history-star');
        if (!star) return;
        var val = parseInt(star.dataset.value);
        stars.forEach(function(s) {
            var v = parseInt(s.dataset.value);
            s.classList.toggle('hovered', v <= val && v > fixedRating);
        });
    });

    container.addEventListener('mouseout', function() {
        stars.forEach(function(s) { s.classList.remove('hovered'); });
    });

    container.addEventListener('click', function(e) {
        var star = e.target.closest('.history-star');
        if (!star) return;
        fixedRating = parseInt(star.dataset.value);
        stars.forEach(function(s) {
            var v = parseInt(s.dataset.value);
            s.classList.toggle('active', v <= fixedRating);
            s.classList.remove('hovered');
        });
    });
})();