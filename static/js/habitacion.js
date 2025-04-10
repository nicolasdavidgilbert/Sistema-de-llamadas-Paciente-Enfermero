const habitacion = document.getElementById("datos").dataset.habitacion;
const cama = document.getElementById("datos").dataset.cama;

// Botón para registrar la llamada
document.getElementById("btnLlamada").addEventListener("click", () => {
    fetch(`/llamada/${habitacion}/${cama}`, {
        method: "GET",
        credentials: "include"
    })
    .then(() => console.log("Llamada enviada"))
    .catch(err => console.error("Error en la llamada:", err));
});

// Botón para registrar presencia
document.getElementById("btnPresencia").addEventListener("click", () => {
    fetch(`/presencia/${habitacion}/${cama}`, {
        method: "GET"
    })
    .then(() => console.log("Presencia registrada"))
    .catch(err => console.error("Error en presencia:", err));
});

// Animación botón volver
document.addEventListener("DOMContentLoaded", () => {
    const volver = document.getElementById("volver");

    if (volver) {
        volver.addEventListener("click", function (e) {
            e.preventDefault();
            document.body.classList.remove("fade-in");
            document.body.classList.add("fade-out");

            setTimeout(() => {
                window.location.href = this.href;
            }, 200);
        });
    }
});

// Comprobación automática del estado
function actualizarEstado() {
    fetch(`/estado/${habitacion}/${cama}`)
        .then(res => res.json())
        .then(data => {
            const led = document.getElementById("led");
            if (data.estado === "aceptada") {
                led.classList.add("encendido");
            } else {
                led.classList.remove("encendido");
            }
        })
        .catch(err => console.error("Error al obtener estado:", err));
}

setInterval(actualizarEstado, 1000);
