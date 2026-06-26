/* Карусель з disabled стрілками */
function createCarousel(trackId, arrowClass, visible, gap) {
    var track = document.getElementById(trackId);
    if (!track) return null;
    var section = track.closest('section');
    var arrows = section.querySelectorAll('.' + arrowClass);
    var leftArr = arrows[0];
    var rightArr = arrows[1];
    var idx = 0;
    var total = track.children.length;
    var max = Math.max(0, total - visible);
    var animating = false;

    function cardW() { return track.children[0].offsetWidth + gap; }

    function updateArrows() {
        if (leftArr) leftArr.classList.toggle('disabled', idx === 0);
        if (rightArr) rightArr.classList.toggle('disabled', idx >= max);
    }

    function slide(i) {
        if (animating) return;
        idx = Math.max(0, Math.min(i, max));
        animating = true;
        track.style.transform = 'translateX(-' + idx * cardW() + 'px)';
        updateArrows();
        setTimeout(function() { animating = false; }, 400);
    }

    updateArrows();
    return {
        prev: function() { slide(idx - 1); },
        next: function() { slide(idx + 1); }
    };
}

/* Відгуки */
(function() {
    var c = createCarousel('reviewsTrack', 'carousel-nav', 3, 16);
    if (c) {
        window.reviewsPrev = c.prev;
        window.reviewsNext = c.next;
    }
})();

/* Новини */
(function() {
    var c = createCarousel('newsDetailTrack', 'carousel-nav', 3, 20);
    if (c) {
        window.newsDetailPrev = c.prev;
        window.newsDetailNext = c.next;
    }
})();