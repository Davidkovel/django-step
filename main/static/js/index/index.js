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


/* ================================================
   КАТАЛОГ АВТОМОБІЛІВ
   ================================================ */
var CATALOG_FILTERS = {
    used:  [{ key: 'brand', label: 'по марці' }, { key: 'region', label: 'по регіону' }, { key: 'type', label: 'по типу' }, { key: 'fuel', label: 'по паливу' }],
    new:   [{ key: 'brand', label: 'по марці' }, { key: 'region', label: 'по регіону' }, { key: 'type', label: 'по типу' }],
    parts: [{ key: 'brand', label: 'по марці' }, { key: 'region', label: 'по регіону' }, { key: 'type', label: 'по типу' }],
    news: null,
    topics: null,
    reviews: null
};

var currentCatalogTab = 'used';

function switchCatalog(btn, tab) {
    /* Табки */
    document.querySelectorAll('.catalog-tab').forEach(function(t) { t.classList.remove('catalog-tab--active'); });
    btn.classList.add('catalog-tab--active');

    /* Панелі */
    document.querySelectorAll('.catalog-panel').forEach(function(p) { p.classList.remove('catalog-panel--active'); });
    document.querySelector('[data-catalog="' + tab + '"]').classList.add('catalog-panel--active');

    currentCatalogTab = tab;

    /* Сортування: показати/сховати + оновити опції */
    var sortEl = document.getElementById('catalogSort');
    var filters = CATALOG_FILTERS[tab];
    if (filters) {
        sortEl.style.display = '';
        buildSortDropdown(filters);
        applyCatalogFilter(filters[0].key, filters[0].label);
    } else {
        sortEl.style.display = 'none';
        closeCatalogSort();
    }
}

function buildSortDropdown(filters) {
    var dd = document.getElementById('catalogSortDropdown');
    dd.innerHTML = '';
    filters.forEach(function(f, i) {
        var label = document.createElement('label');
        label.className = 'catalog-sort__option';
        label.innerHTML = '<span>' + f.label + '</span><input type="radio" name="catalog_sort" value="' + f.key + '" class="catalog-sort__radio"' + (i === 0 ? ' checked' : '') + '>';
        label.querySelector('input').addEventListener('change', function() {
            applyCatalogFilter(f.key, f.label);
            closeCatalogSort();
        });
        dd.appendChild(label);
    });
}

function applyCatalogFilter(key, label) {
    document.getElementById('catalogSortText').textContent = label;

    var panel = document.querySelector('.catalog-panel--active');
    panel.querySelectorAll('.catalog-data').forEach(function(d) {
        d.classList.remove('catalog-data--active');
    });
    var target = panel.querySelector('[data-sort="' + key + '"]');
    if (target) target.classList.add('catalog-data--active');
}

function toggleCatalogSort() {
    var dd = document.getElementById('catalogSortDropdown');
    dd.classList.toggle('is-open');
}

function closeCatalogSort() {
    document.getElementById('catalogSortDropdown').classList.remove('is-open');
}

/* Закриття дропдауну при кліку за межами */
document.addEventListener('click', function(e) {
    var sortEl = document.getElementById('catalogSort');
    if (sortEl && !sortEl.contains(e.target)) {
        closeCatalogSort();
    }
});

/* Ініціалізація: побудувати дропдаун для першого табу */
(function initCatalog() {
    var filters = CATALOG_FILTERS[currentCatalogTab];
    if (filters) buildSortDropdown(filters);
})();

/* ===== Мокові дані ===== */
const MODELS = {
    'Toyota': ['Camry', 'Corolla', 'RAV4', 'Land Cruiser'],
    'BMW': ['320d', 'X5', 'M3', '520d'],
    'Volkswagen': ['Golf', 'Passat', 'Tiguan', 'Polo'],
    'Chevrolet': ['Lacetti', 'Aveo', 'Bolt EUV', 'Malibu'],
    'Hyundai': ['Tucson', 'Elantra', 'Sonata', 'Kona']
};
let currentCurrency = '$';

function switchTab(clicked) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('tab--active'));
    clicked.classList.add('tab--active');
}

document.querySelectorAll('.dropdown__trigger').forEach(trigger => {
    trigger.addEventListener('click', function(e) {
        if (e.target.closest('.dropdown__clear')) return;
        const dropdown = this.closest('.dropdown');
        const wasOpen = dropdown.classList.contains('is-open');
        closeAllDropdowns();
        if (!wasOpen) dropdown.classList.add('is-open');
    });
});
document.addEventListener('click', function(e) { if (!e.target.closest('.dropdown')) closeAllDropdowns(); });
document.addEventListener('keydown', function(e) { if (e.key === 'Escape') closeAllDropdowns(); });
function closeAllDropdowns() { document.querySelectorAll('.dropdown.is-open').forEach(d => d.classList.remove('is-open')); }

document.querySelectorAll('[data-dropdown="type"] .dropdown__radio').forEach(radio => {
    radio.addEventListener('change', function() {
        const dd = this.closest('.dropdown');
        dd.querySelector('.dropdown__value').textContent = this.nextElementSibling.textContent;
        dd.classList.remove('is-open');
    });
});

let selectedBrand = '';
let selectedModels = [];
function selectBrand(radio) {
    selectedBrand = radio.value; selectedModels = [];
    const dd = radio.closest('.dropdown');
    dd.querySelector('.brand-step--brands').style.display = 'none';
    dd.querySelector('.brand-step--models').style.display = 'block';
    dd.querySelector('.brand-search__value').textContent = selectedBrand;
    const modelList = dd.querySelector('.dropdown__list--models');
    modelList.innerHTML = '';
    (MODELS[selectedBrand] || []).forEach(model => {
        const label = document.createElement('label');
        label.className = 'dropdown__option';
        label.innerHTML = `<input type="checkbox" name="model" value="${model}" class="dropdown__checkbox"><span>${model}</span>`;
        modelList.appendChild(label);
    });
    updateBrandValue(dd);
}
function resetBrand() {
    selectedBrand = ''; selectedModels = [];
    const dd = document.querySelector('[data-dropdown="brand"]');
    dd.querySelector('.brand-step--brands').style.display = 'block';
    dd.querySelector('.brand-step--models').style.display = 'none';
    dd.querySelectorAll('[name="brand_select"]').forEach(r => r.checked = false);
    updateBrandValue(dd);
}
function applyBrand() {
    const dd = document.querySelector('[data-dropdown="brand"]');
    selectedModels = [...dd.querySelectorAll('.dropdown__list--models .dropdown__checkbox:checked')].map(cb => cb.value);
    updateBrandValue(dd); dd.classList.remove('is-open');
}
function updateBrandValue(dd) {
    const trigger = dd.querySelector('.dropdown__trigger');
    const valueEl = dd.querySelector('.dropdown__value');
    if (!selectedBrand) { valueEl.textContent = 'Марка, Модель'; trigger.classList.remove('has-label'); }
    else if (selectedModels.length === 0) { valueEl.textContent = selectedBrand + ', Модель'; trigger.classList.add('has-label'); }
    else { valueEl.textContent = selectedBrand + ', ' + selectedModels.join(', '); trigger.classList.add('has-label'); }
}

(function initYears() {
    const fromEl = document.getElementById('yearFrom');
    const toEl = document.getElementById('yearTo');
    for (let y = 2026; y >= 1900; y--) {
        fromEl.innerHTML += `<label class="dropdown__option"><input type="radio" name="year_from" value="${y}" class="dropdown__radio"><span>${y}</span></label>`;
        toEl.innerHTML += `<label class="dropdown__option"><input type="radio" name="year_to" value="${y}" class="dropdown__radio"><span>${y}</span></label>`;
    }
})();
function applyYear() {
    const dd = document.querySelector('[data-dropdown="year"]');
    const from = dd.querySelector('[name="year_from"]:checked');
    const to = dd.querySelector('[name="year_to"]:checked');
    const trigger = dd.querySelector('.dropdown__trigger');
    const valueEl = dd.querySelector('.dropdown__value');
    if (from || to) { const p = []; if (from) p.push('Від ' + from.value); if (to) p.push('до ' + to.value); valueEl.textContent = p.join(' '); trigger.classList.add('has-label'); }
    else { valueEl.textContent = 'Рік випуску'; trigger.classList.remove('has-label'); }
    dd.classList.remove('is-open');
}

function switchCurrency(btn, currency) {
    currentCurrency = currency;
    btn.closest('.currency-tabs').querySelectorAll('.currency-tab').forEach(t => t.classList.remove('currency-tab--active'));
    btn.classList.add('currency-tab--active');
}
function applyPrice() {
    const dd = document.querySelector('[data-dropdown="price"]');
    const from = document.getElementById('priceFrom').value;
    const to = document.getElementById('priceTo').value;
    const trigger = dd.querySelector('.dropdown__trigger');
    const valueEl = dd.querySelector('.dropdown__value');
    if (from || to) { const p = []; if (from) p.push('Від ' + Number(from).toLocaleString() + ' ' + currentCurrency); if (to) p.push('до ' + Number(to).toLocaleString() + ' ' + currentCurrency); valueEl.textContent = p.join(' '); trigger.classList.add('has-label'); }
    else { valueEl.textContent = 'Вартість'; trigger.classList.remove('has-label'); }
    dd.classList.remove('is-open');
}

function applyCheckbox(name) {
    const dd = document.querySelector(`[data-dropdown="${name}"]`);
    const checked = [...dd.querySelectorAll('.dropdown__checkbox:checked')];
    const trigger = dd.querySelector('.dropdown__trigger');
    const valueEl = dd.querySelector('.dropdown__value');
    const placeholder = dd.querySelector('.dropdown__label').textContent;
    if (checked.length > 0) { valueEl.textContent = checked.map(cb => cb.nextElementSibling.textContent).join(', '); trigger.classList.add('has-label'); }
    else { valueEl.textContent = placeholder; trigger.classList.remove('has-label'); }
    dd.classList.remove('is-open');
}

function clearDropdown(e, name) {
    e.stopPropagation();
    const dd = document.querySelector(`[data-dropdown="${name}"]`);
    const trigger = dd.querySelector('.dropdown__trigger');
    const valueEl = dd.querySelector('.dropdown__value');
    const placeholder = dd.querySelector('.dropdown__label').textContent;
    dd.querySelectorAll('input').forEach(inp => { if (inp.type === 'checkbox' || inp.type === 'radio') inp.checked = false; else inp.value = ''; });
    if (name === 'brand') resetBrand();
    valueEl.textContent = placeholder; trigger.classList.remove('has-label'); dd.classList.remove('is-open');
}


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