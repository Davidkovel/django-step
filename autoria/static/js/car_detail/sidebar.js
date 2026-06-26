function toggleDetailFav(btn) {
    btn.classList.toggle('is-liked');
}

function copyVin(vin) {
    navigator.clipboard.writeText(vin).catch(function() {});
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.seller-message').forEach(function(form) {
        var input = form.querySelector('.seller-message__input');
        var status = form.querySelector('.seller-message__status');

        form.addEventListener('submit', function(event) {
            event.preventDefault();

            if (!input.value.trim()) {
                status.textContent = 'Напишіть коротке повідомлення продавцю.';
                status.classList.add('is-error');
                input.focus();
                return;
            }

            status.textContent = 'Повідомлення підготовлено. Продавець скоро відповість.';
            status.classList.remove('is-error');
            input.value = '';
        });
    });
});
