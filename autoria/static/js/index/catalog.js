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