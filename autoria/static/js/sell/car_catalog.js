(function () {
    var catalogElement = document.getElementById('car-catalog-data');
    var brandInput = document.querySelector('[data-car-catalog="brand"]');
    var modelInput = document.querySelector('[data-car-catalog="model"]');
    var modelOptions = document.getElementById('car-model-options');

    if (!catalogElement || !brandInput || !modelInput || !modelOptions) {
        return;
    }

    var catalog = JSON.parse(catalogElement.textContent);

    function findBrand(value) {
        var normalizedValue = value.trim().toLowerCase();
        return Object.keys(catalog).find(function (brand) {
            return brand.toLowerCase() === normalizedValue;
        });
    }

    function renderModels() {
        var brand = findBrand(brandInput.value);
        var currentModel = modelInput.value;
        modelOptions.innerHTML = '';

        if (!brand) {
            modelInput.placeholder = 'Спочатку виберіть марку';
            return;
        }

        catalog[brand].forEach(function (model) {
            var option = document.createElement('option');
            option.value = model;
            modelOptions.appendChild(option);
        });

        modelInput.placeholder = 'Почніть вводити модель';
        if (currentModel && catalog[brand].indexOf(currentModel) === -1) {
            modelInput.value = '';
        }
    }

    brandInput.addEventListener('input', renderModels);
    brandInput.addEventListener('change', renderModels);
    renderModels();
}());
