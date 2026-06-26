var currentSlide = 0;
var galleryImagesElement = document.getElementById('gallery-images-data');
var galleryImages = galleryImagesElement ? JSON.parse(galleryImagesElement.textContent) : [];
var totalSlides = galleryImages.length || document.querySelectorAll('.gallery__thumb').length || 1;

function galleryGo(index) {
    currentSlide = Math.max(0, Math.min(index, totalSlides - 1));
    document.getElementById('galleryCounter').textContent = (currentSlide + 1) + ' з ' + totalSlides;

    var image = document.getElementById('galleryImage');
    if (image && galleryImages[currentSlide]) {
        image.src = galleryImages[currentSlide];
    }

    var thumbs = document.querySelectorAll('.gallery__thumb');
    thumbs.forEach(function(t) { t.classList.remove('gallery__thumb--active'); });
    if (thumbs[currentSlide]) {
        thumbs[currentSlide].classList.add('gallery__thumb--active');
    }

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
