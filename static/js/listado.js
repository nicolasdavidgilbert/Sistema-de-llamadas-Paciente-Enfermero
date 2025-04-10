document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.tarjeta').forEach(enlace => {
        enlace.addEventListener('click', e => {
            e.preventDefault();
            document.body.classList.remove('fade-in');
            document.body.classList.add('fade-out');

            setTimeout(() => {
                window.location.href = enlace.href;
            }, 700); // ⬅ más suave
        });
    });
});
