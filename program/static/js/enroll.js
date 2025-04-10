document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-enroll");

    if (form?.dataset.error) {
        // Asegura que solo se agite una vez
        form.addEventListener("animationend", () => {
            form.classList.remove("shake");
        }, { once: true });

        form.classList.add("shake");

        const input = document.getElementById("codigo");
        if (input) input.focus();
    }
});
