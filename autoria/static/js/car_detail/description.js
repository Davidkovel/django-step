function toggleSpecs() {
    var extra = document.getElementById('specsExtra');
    var btn = document.getElementById('specsToggle');
    var isVisible = extra.classList.toggle('is-visible');
    btn.textContent = isVisible ? 'Приховати' : 'Дивитись всі опції';
}