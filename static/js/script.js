document.addEventListener("DOMContentLoaded", () => {
  // 1. Confirmación de eliminación dinámica para cualquier formulario con atributo 'data-confirm'
  const deleteForms = document.querySelectorAll("form[data-confirm]");
  
  deleteForms.forEach((form) => {
    form.addEventListener("submit", (e) => {
      const mensaje = form.getAttribute("data-confirm") || "¿Estás seguro de realizar esta acción?";
      if (!confirm(mensaje)) {
        e.preventDefault();
      }
    });
  });

  // 2. Búsqueda y filtrado dinámico en la tabla
  const searchInput = document.getElementById("tabla-busqueda");
  if (searchInput) {
    searchInput.addEventListener("keyup", () => {
      const filtro = searchInput.value.toLowerCase();
      const filas = document.querySelectorAll("tbody tr");

      filas.forEach((fila) => {
        const textoFila = fila.innerText.toLowerCase();
        if (textoFila.includes(filtro)) {
          fila.style.display = "";
        } else {
          fila.style.display = "none";
        }
      });
    });
  }

  // 3. Formateador automático simple para RUT chileno (ejemplo: 12345678-k)
  const rutInputs = document.querySelectorAll("input[name='rut']");
  rutInputs.forEach((input) => {
    input.addEventListener("input", (e) => {
      let valor = e.target.value.replace(/[^0-9kK]/g, "");
      if (valor.length > 1) {
        const cuerpo = valor.slice(0, -1);
        const dv = valor.slice(-1).toUpperCase();
        e.target.value = `${cuerpo}-${dv}`;
      }
    });
  });
});