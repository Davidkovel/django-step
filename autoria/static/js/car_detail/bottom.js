/* Рейтинг */
(function initBottomRating() {
    var container = document.getElementById('bottomStars');
    if (!container) return;
    var stars = [].slice.call(container.querySelectorAll('.bottom-star'));
    var fixedRating = 0;

    container.addEventListener('mouseover', function(e) {
        var star = e.target.closest('.bottom-star');
        if (!star) return;
        var val = parseInt(star.dataset.value);
        stars.forEach(function(s) {
            s.classList.toggle('hovered', parseInt(s.dataset.value) <= val && parseInt(s.dataset.value) > fixedRating);
        });
    });
    container.addEventListener('mouseout', function() {
        stars.forEach(function(s) { s.classList.remove('hovered'); });
    });
    container.addEventListener('click', function(e) {
        var star = e.target.closest('.bottom-star');
        if (!star) return;
        fixedRating = parseInt(star.dataset.value);
        stars.forEach(function(s) {
            s.classList.toggle('active', parseInt(s.dataset.value) <= fixedRating);
            s.classList.remove('hovered');
        });
    });
})();

/* Схожі оголошення — по одній картці */
(function initSimilar() {
    var track = document.getElementById('similarTrack');
    if (!track) return;
    var cards = track.children;
    var currentIndex = 0;
    var total = cards.length;
    var visible = 3;
    var maxIndex = total - visible;
    var isAnimating = false;

    function getCardWidth() {
        return cards[0].offsetWidth + 20;
    }

    function slideTo(index) {
        if (isAnimating) return;
        currentIndex = Math.max(0, Math.min(index, maxIndex));
        isAnimating = true;
        track.style.transform = 'translateX(-' + currentIndex * getCardWidth() + 'px)';
        setTimeout(function() { isAnimating = false; }, 400);
    }

    window.similarPrev = function() { slideTo(currentIndex - 1); };
    window.similarNext = function() { slideTo(currentIndex + 1); };
})();