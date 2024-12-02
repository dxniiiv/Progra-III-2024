Crear el entorno virtual

`
python -m venv venv
`

Activar el entorno virtual

`
venv\Scripts\activate
`

Instalacion de dependecias

` 
pip install -r backend/requirements.txt
`
Migrar base de datos

`
cd backend
`

`
python manage.py migrate
`

Iniciar servidor
`
python manage.py runserver
`
