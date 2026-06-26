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