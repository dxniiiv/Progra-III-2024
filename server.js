const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');
const app = express();

app.use(bodyParser.json());

const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',  
    password: 'daniel2704',  
    database: 'parcial'  
});

// Conectar a MariaDB
db.connect((err) => {
    if (err) {
        console.error('Error conectando a la base de datos:', err);
        return;
    }
    console.log('Conectado a MariaDB');
});

// Ruta para crear un nuevo usuario (C - Create)
app.post('/usuarios', (req, res) => {
    const { usuario, clave, nombre, direccion, telefono } = req.body;
    const query = 'INSERT INTO usuarios (usuario, clave, nombre, direccion, telefono) VALUES (?, ?, ?, ?, ?)';
    db.query(query, [usuario, clave, nombre, direccion, telefono], (err, result) => {
        if (err) {
            return res.status(500).json({ message: 'Error al crear el usuario' });
        }
        res.status(201).json({ message: 'Usuario creado correctamente', id: result.insertId });
    });
});

// Ruta para obtener todos los usuarios (R - Read)
app.get('/usuarios', (req, res) => {
    const query = 'SELECT * FROM usuarios';
    db.query(query, (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error al obtener usuarios' });
        }
        res.status(200).json(results);
    });
});

// Ruta para actualizar un usuario por su ID (U - Update)
app.put('/usuarios/:id', (req, res) => {
    const { usuario, clave, nombre, direccion, telefono } = req.body;
    const query = 'UPDATE usuarios SET usuario = ?, clave = ?, nombre = ?, direccion = ?, telefono = ? WHERE id = ?';
    db.query(query, [usuario, clave, nombre, direccion, telefono, req.params.id], (err, result) => {
        if (err) {
            return res.status(500).json({ message: 'Error al actualizar el usuario' });
        }
        res.status(200).json({ message: 'Usuario actualizado correctamente' });
    });
});

// Ruta para eliminar un usuario por su ID (D - Delete)
app.delete('/usuarios/:id', (req, res) => {
    const query = 'DELETE FROM usuarios WHERE id = ?';
    db.query(query, [req.params.id], (err, result) => {
        if (err) {
            return res.status(500).json({ message: 'Error al eliminar el usuario' });
        }
        res.status(200).json({ message: 'Usuario eliminado correctamente' });
    });
});

// Ruta para buscar usuarios por nombre (Búsqueda)
app.get('/usuarios/buscar/:nombre', (req, res) => {
    const query = 'SELECT * FROM usuarios WHERE nombre LIKE ?';
    db.query(query, [`%${req.params.nombre}%`], (err, results) => {
        if (err) {
            return res.status(500).json({ message: 'Error al buscar usuarios' });
        }
        res.status(200).json(results);
    });
});

// Iniciar el servidor
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});


// Ruta para buscar usuarios por nombre (Búsqueda)
app.get('/usuarios/buscar/:nombre', async (req, res) => {
    try {
        const usuariosEncontrados = await Usuario.find({ nombre: new RegExp(req.params.nombre, 'i') });
        res.status(200).json(usuariosEncontrados);
    } catch (error) {
        res.status(500).json({ message: 'Error al buscar usuarios' });
    }
});

// Iniciar el servidor
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
