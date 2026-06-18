function toggleDetailFav(btn) {
    btn.classList.toggle('is-liked');
}

function copyVin(vin) {
    navigator.clipboard.writeText(vin).catch(function() {});
}

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


(function initParts() {
    var track = document.getElementById('partsTrack');
    if (!track) return;
    var leftBtn = document.getElementById('partsLeft');
    var rightBtn = document.getElementById('partsRight');
    var idx = 0;
    var total = track.children.length;
    var visible = 4;
    var step = 2;
    var max = total - visible;
    var animating = false;

    function cardW() { return track.children[0].offsetWidth + 16; }

    function updateArrows() {
        leftBtn.classList.toggle('disabled', idx === 0);
        rightBtn.classList.toggle('disabled', idx >= max);
    }

    function slide(i) {
        if (animating) return;
        idx = Math.max(0, Math.min(i, max));
        animating = true;
        track.style.transform = 'translateX(-' + idx * cardW() + 'px)';
        updateArrows();
        setTimeout(function() { animating = false; }, 400);
    }

    window.partsPrev = function() { slide(idx - step); };
    window.partsNext = function() { slide(idx + step); };
    updateArrows();
})();


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

var currentSlide = 0;
var totalSlides = 6;

function galleryGo(index) {
    currentSlide = Math.max(0, Math.min(index, totalSlides - 1));
    document.getElementById('galleryCounter').textContent = (currentSlide + 1) + ' з ' + totalSlides;

    var thumbs = document.querySelectorAll('.gallery__thumb');
    thumbs.forEach(function(t) { t.classList.remove('gallery__thumb--active'); });
    thumbs[currentSlide].classList.add('gallery__thumb--active');

    scrollThumbsToActive();
}

function galleryPrev() { galleryGo(currentSlide - 1); }
function galleryNext() { galleryGo(currentSlide + 1); }

function scrollThumbsToActive() {
    var track = document.getElementById('galleryThumbs');
    var thumbs = track.children;
    if (thumbs.length === 0) return;

    var thumbWidth = thumbs[0].offsetWidth + 8;
    var viewport = track.parentElement;
    var viewportWidth = viewport.offsetWidth;
    var maxScroll = track.scrollWidth - viewportWidth;

    var targetScroll = currentSlide * thumbWidth;
    targetScroll = Math.min(targetScroll, maxScroll);
    targetScroll = Math.max(targetScroll, 0);

    track.style.transform = 'translateX(-' + targetScroll + 'px)';
}

function toggleSpecs() {
    var extra = document.getElementById('specsExtra');
    var btn = document.getElementById('specsToggle');
    var isVisible = extra.classList.toggle('is-visible');
    btn.textContent = isVisible ? 'Приховати' : 'Дивитись всі опції';
}

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