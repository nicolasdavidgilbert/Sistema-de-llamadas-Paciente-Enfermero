let modoActivo = false;
let ids_eliminar = [];
let datos_updatear = [];

function reload(){
    modoActivo = !modoActivo;
    location.reload();
    ids_eliminar = [];
    datos_updatear = [];
}

async function cancelar(){
    const confirmar = await mostrarModalConfirmacion("¿Desea cancelar los cambios?");
    if (confirmar){
        reload();
    }
}


async function modoEditar() {
    const confirmar = await mostrarModalConfirmacion("¿Desea entrar en el modo edición?");
    if (confirmar){
        modoActivo = !modoActivo;
        const btns = document.querySelectorAll('.modo-edicion');
        btns.forEach(c => c.style.display = modoActivo ? '' : 'none');
        const ocultar = document.querySelectorAll('.ocultar');
        ocultar.forEach(c => c.style.display = modoActivo ? 'none' : '');  
    }
}

async function añadirEliminar(id) {
    const confirmar = await mostrarModalConfirmacion("¿Eliminar?");
    if (confirmar){
        ids_eliminar.push(id);
    
        // Buscar la fila <tr> que contiene ese botón o checkbox
        const fila = document.querySelector(`tr[data-id='${id}']`);
        if (fila) {
            fila.style.display = 'none';
        }
    }
}

async function añadirUpdatear(id) {
    const confirmar = await mostrarModalConfirmacion("¿Guardar cambios?");
    if (confirmar){
        const fila = document.querySelector(`tr[data-id='${id}']`);
        const inputs = fila.querySelectorAll('input');

        const datos = {
            id: id,
            nombre: inputs[0].value.trim(),
            telefono: inputs[1].value.trim(),
            codigo: inputs[2].value.trim()
        };

        datos_updatear.push(datos)
        const celdas = fila.querySelectorAll('td');

        // Nombre (columna 3)
        const celdaNombre = celdas[3];
        const inputNombre = celdaNombre.querySelector('input');
        const nombre = inputNombre.value.trim();
        celdaNombre.textContent = nombre;

        // Teléfono (columna 4)
        const celdaTlf = celdas[4];
        const inputTlf = celdaTlf.querySelector('input');
        const tlf = inputTlf.value.trim();
        celdaTlf.textContent = tlf;

        // Código (columna 5)
        const celdaCodigo = celdas[5];
        const inputCodigo = celdaCodigo.querySelector('.codigo-real input');
        const valorCodigo = inputCodigo.value.trim();

        // Restaurar contenido original
        const spanOculto = celdaCodigo.querySelector('.codigo-oculto');
        const spanReal = celdaCodigo.querySelector('.codigo-real');
        spanReal.textContent = valorCodigo;
        spanReal.style.display = "none"; // Ocultar de nuevo
        if (spanOculto) spanOculto.style.display = "inline";

        // Restaurar los botones de edición 📝
        const celdaEdit = celdas[0];
        celdaEdit.innerHTML = `
            <button class="btn-editar" onclick="editar('${id}')">📝</button>
        `;       
    }

}

function editar(id) {
    const fila = document.querySelector(`tr[data-id='${id}']`);
    if (!fila) return;

    const celdas = fila.querySelectorAll('td');

    // Guardar valores originales en dataset
    const nombreOriginal = celdas[3].textContent.trim();
    const tlfOriginal = celdas[4].textContent.trim();
    const codigoOriginal = celdas[5].querySelector('.codigo-real').textContent.trim();

    fila.dataset.nombreOriginal = nombreOriginal;
    fila.dataset.tlfOriginal = tlfOriginal;
    fila.dataset.codigoOriginal = codigoOriginal;

    // Cambiar botones
    const celdaEdit = celdas[0];
    celdaEdit.innerHTML = `
        <div class="aceptar-cancelar">
            <button class="btn-aceptar" onclick="añadirUpdatear('${id}')">✅</button>
            <button class="btn-cancelar" onclick="cancelar_id('${id}')">❌</button>
        </div>
    `;

    // Mostrar inputs
    celdas[3].innerHTML = `<input type="text" value="${nombreOriginal}" />`;
    celdas[4].innerHTML = `<input type="text" value="${tlfOriginal}" maxlength="9" />`;

    const celdaCodigo = celdas[5];
    const spanReal = celdaCodigo.querySelector('.codigo-real');
    spanReal.innerHTML = `<input type="text" value="${codigoOriginal}" maxlength="6">`;
    spanReal.style.display = "inline";

    const spanOculto = celdaCodigo.querySelector('.codigo-oculto');
    if (spanOculto) spanOculto.style.display = "none";
}

function cancelar_id(id) {
    const confirmar = confirm("¿Cancelar cambios?");
    if (confirmar) {

        const fila = document.querySelector(`tr[data-id='${id}']`);
        if (!fila) return;

        const celdas = fila.querySelectorAll('td');

        // Recuperar datos originales del dataset
        const nombre = fila.dataset.nombreOriginal;
        const tlf = fila.dataset.tlfOriginal;
        const codigo = fila.dataset.codigoOriginal;

        // Restaurar contenido
        celdas[3].textContent = nombre;
        celdas[4].textContent = tlf;

        const celdaCodigo = celdas[5];
        const spanReal = celdaCodigo.querySelector('.codigo-real');
        const spanOculto = celdaCodigo.querySelector('.codigo-oculto');

        spanReal.textContent = codigo;
        spanReal.style.display = "none";
        if (spanOculto) spanOculto.style.display = "inline";

        // Restaurar botón 📝
        const celdaEdit = celdas[0];
        celdaEdit.innerHTML = `
            <button class="btn-editar" onclick="editar('${id}')">📝</button>
        `;
    }
}




function confirmar() {
    // Ejecutar ambas peticiones y esperar a que terminen
    const confirmar = confirm("¿Guardar cambios? No hay vuleta atrás");
    if (confirmar) {
        Promise.all([
            fetch('/admin/updatear_asistentes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(datos_updatear)
            }),
            fetch('/admin/eliminar_asistentes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(ids_eliminar)
            })            
        ])
        .then(([res1, res2]) => {
            if (res1.ok && res2.ok) {
                reload();
            } else {
                alert("❌ Error aplicando cambios.");
            }
        })
        .catch(() => {
            alert("❌ Error de red.");
        });
    }
}




async function crearAsistente() {
    const nombre = document.getElementById('nuevo-nombre').value.trim();
    const telefono = document.getElementById('nuevo-telefono').value.trim();
    const codigo = document.getElementById('nuevo-codigo').value.trim();
    const mensaje = document.getElementById('mensaje');

    if (!nombre || !telefono || !codigo) {
    mensaje.textContent = "⚠️ Todos los campos son obligatorios.";
    mensaje.style.color = "red";
    return;
    }

    if (codigo.length > 6) {
        mensaje.textContent = "⚠️ El código debe tener como máximo 6 caracteres.";
        mensaje.style.color = "red";
        return;
    }
    

    const datos = {
        nombre: nombre,
        telefono: telefono,
        password: codigo
    };

    try {
        const res = await fetch("/admin/asistente-nuevo", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(datos)
        });

        const result = await res.json();

        if (res.ok) {
            mensaje.textContent = "✅ Asistente creado correctamente.";
            mensaje.style.color = "green";
            setTimeout(() => reload(), 500);
        } else {
            mensaje.textContent = "❌ Error: " + result.error;
            mensaje.style.color = "red";
        }

    } catch (err) {
        mensaje.textContent = "❌ Error de red.";
        mensaje.style.color = "red";
    }
}

document.querySelectorAll('.show-hide').forEach(icono => {
    icono.addEventListener('click', () => {
      const fila = icono.closest('td');
      const oculto = fila.querySelector('.codigo-oculto');
      const real = fila.querySelector('.codigo-real');
      
      if (real.style.display === 'none') {
        oculto.style.display = 'none';
        real.style.display = 'inline';
        icono.classList.replace('bx-hide', 'bx-show');
      } else {
        oculto.style.display = 'inline';
        real.style.display = 'none';
        icono.classList.replace('bx-show', 'bx-hide');
      }
    });
  });
  




function mostrarModalConfirmacion(mensaje) {
    return new Promise((resolver) => {
      const modal = document.getElementById('modalConfirmacion');
      const mensajeElemento = document.getElementById('modalMensaje');
      const botonSi = document.getElementById('modalSi');
      const botonNo = document.getElementById('modalNo');
  
      mensajeElemento.innerText = mensaje;
      modal.style.display = 'block';
  
      // Limpiar handlers previos por seguridad
      botonSi.onclick = () => {
        modal.style.display = 'none';
        resolver(true);
      };
  
      botonNo.onclick = () => {
        modal.style.display = 'none';
        resolver(false);
      };
    });
}
  