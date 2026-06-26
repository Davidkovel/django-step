function hideCard(btn) {
    const card = btn.closest('[data-card]');
    card.querySelector('.car-card__visual').style.display = 'none';
    card.querySelector('.car-card__hidden').style.display = 'block';
}

function unhideCard(btn) {
    const card = btn.closest('[data-card]');
    card.querySelector('.car-card__visual').style.display = '';
    card.querySelector('.car-card__hidden').style.display = 'none';
}

function toggleFav(btn) {
    const isLiked = btn.classList.toggle('is-liked');
    showToast(isLiked ? 'Пропозицію додано до Обраного' : 'Пропозицію видалено з Обраного');
}

function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => toast.classList.remove('show'), 2500);
}

function showMore() {
    document.getElementById('recsGrid').classList.add('show-all');
    document.getElementById('recsMoreWrap').style.display = 'none';
}