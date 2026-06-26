const carouselState = {};
function slide(name, direction) {
    const carousel = document.querySelector(`[data-carousel="${name}"]`);
    const track = carousel.querySelector('.carousel__track');
    const visible = parseInt(carousel.dataset.visible);
    const items = track.children;
    const total = items.length;
    const gap = 16;
    if (!carouselState[name]) carouselState[name] = 0;
    carouselState[name] += direction * visible;
    const maxSlide = total - visible;
    carouselState[name] = Math.max(0, Math.min(carouselState[name], maxSlide));
    const itemWidth = items[0].offsetWidth + gap;
    track.style.transform = `translateX(-${carouselState[name] * itemWidth}px)`;
    const section = carousel.closest('section');
    const leftBtn = section.querySelector('.carousel-arrow--left');
    const rightBtn = section.querySelector('.carousel-arrow--right');
    leftBtn.classList.toggle('disabled', carouselState[name] === 0);
    rightBtn.classList.toggle('disabled', carouselState[name] >= maxSlide);
}