document.getElementById('registroForm').addEventListener('submit', function(event) {
    event.preventDefault();  

    const usuario = document.getElementById('usuario').value;
    const clave = document.getElementById('clave').value;
    const nombre = document.getElementById('nombre').value;
    const direccion = document.getElementById('direccion').value;
    const telefono = document.getElementById('telefono').value

    fetch('/usuarios', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ usuario, clave, nombre, direccion, telefono })
    })
    .then(response => response.json())
    .then(data => {
        alert('Usuario registrado correctamente');
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

document.getElementById('btn-modificar').addEventListener('click', function() {
    const idUsuario = prompt('Ingresa el ID del usuario que deseas modificar');
    const nuevoNombre = prompt('Ingresa el nuevo nombre');

    fetch(`/usuarios/${idUsuario}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre: nuevoNombre })
    })
    .then(response => response.json())
    .then(data => {
        alert('Usuario modificado correctamente');
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('btn-eliminar').addEventListener('click', function() {
    const idUsuario = prompt('Ingresa el ID del usuario que deseas eliminar');

    fetch(`/usuarios/${idUsuario}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.status === 200) {
            alert('Usuario eliminado correctamente');
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('btn-buscar').addEventListener('click', function() {
    const nombre = document.getElementById('buscarNombre').value;

    fetch(`/usuarios/buscar/${nombre}`)
        .then(response => response.json())
        .then(data => {
            const resultadosBusqueda = document.getElementById('resultadosBusqueda');
            resultadosBusqueda.innerHTML = '';
            if (data.length > 0) {
                data.forEach(usuario => {
                    resultadosBusqueda.innerHTML += `<p>ID: ${usuario.id}, Nombre: ${usuario.nombre}</p>`;
                });
            } else {
                resultadosBusqueda.innerHTML = '<p>No se encontraron usuarios</p>';
            }
        })
        .catch(error => console.error('Error:', error));
});
