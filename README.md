## Instrucciones para correr el codigo

1. Crear una base de datos en MySQL con el nombre que se desee.

2. Ejecutar el contenido del archivo [schema.sql](https://github.com/gmr458/proyecto/blob/master/schema_mysql.sql) para crear las tablas.

3. Crear en la raiz del proyecto un archivo `.env` y alli poner los valores de configuración para la conexión con la base de datos.
En el archivo `.env` tambien van los datos del usuario administrador que se crea automaticamente cuando la API se ejecuta por primera vez.

```sh
MYSQL_USER=user
MYSQL_PASSWORD=password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DBNAME=dbname

ADMIN_NOMBRE=Usuario
ADMIN_APELLIDO=Admin
ADMIN_TELEFONO=1234567890
ADMIN_EMAIL=admin@email.com
ADMIN_CONTRASENA=admin123
```

4. Crear un entorno virtual de Python con el siguiente comando:

En Linux:
```sh
python3 -m venv venv
```

En el CMD o PowerShell de Windows:
```sh
py -3 -m venv venv
```

5. Activar el entorno virtual con el siguiente comando:

En Linux:
```sh
source venv/bin/activate
```

En el CMD de Windows:
```sh
venv\Scripts\activate
```

En el PowerShell de Windows:
```sh
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
```
```sh
venv\Scripts\Activate.ps1
```

6. Instalar las dependencias con el siguiente comando:
```sh
pip install -r requirements.txt
```

7. Ejecutar el siguiende comando en la raiz del proyecto.
```sh
uvicorn app.main:app --reload
```
