# 📘 Instrucciones para Conexión a SQL Server

## ✅ Estado Actual

### Completado:
- ✅ Tablas creadas en SQL Server con prefijo `app_`
- ✅ Dependencias de Python instaladas (`pyodbc`, `pymssql`)
- ✅ Modelos actualizados con nombres de tabla correctos
- ✅ Script SQL ejecutado exitosamente

### Resultados de la Base de Datos:
```sql
tabla           registros
app_finca       1
app_usuario     1
app_supervisor  0
app_area        0
app_codigo      0
```

## 🔧 Configuración Actual

### Servidor SQL Server:
- **Host**: 181.198.42.195
- **Puerto**: 5010
- **Base de datos**: Rend_Cultivo
- **Usuario**: sa
- **Password**: 6509

### Usuario Admin:
- **Email**: david.herrera@tessacorporation.com
- **Password**: admin123
- **Rol**: admin

## ⚠️ Problema Actual: Conexión desde Python

La conexión desde Azure Data Studio funciona, pero Python no puede conectarse debido a restricciones de firewall/red.

### Posibles Soluciones:

#### Opción 1: Agregar IP al Firewall de Azure (Recomendado)
Si tu SQL Server está en Azure, necesitas agregar la IP de tu máquina al firewall:

1. Ve al Azure Portal
2. Encuentra tu SQL Server
3. Ve a "Firewalls and virtual networks"
4. Agrega tu IP pública actual
5. Guarda los cambios

Para saber tu IP pública:
```bash
curl https://api.ipify.org
```

#### Opción 2: Habilitar Acceso desde Servicios de Azure
En el firewall de Azure SQL Server, habilita "Allow Azure services and resources to access this server"

#### Opción 3: Usar Azure Data Studio para Desarrollo
Mantén usando Azure Data Studio para probar queries y usa SQLite local para desarrollo de la aplicación Flask.

#### Opción 4: VPN o Túnel SSH
Si tu empresa usa VPN, conéctate a la VPN antes de ejecutar la aplicación.

## 🚀 Opciones para Ejecutar la Aplicación

### Opción A: Usar SQL Server (cuando la conexión esté disponible)

1. **Asegurar que Python puede conectarse:**
```bash
python test_connection.py
```

2. **Si la conexión es exitosa, ejecutar:**
```bash
python main.py
```

3. **Acceder a:**
```
http://127.0.0.1:5000
```

### Opción B: Usar SQLite para Desarrollo Local

1. **Editar `app/config.py`** y cambiar la línea 21-24 por:
```python
# Usar SQLite local en lugar de SQL Server
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{basedir}/instance/agricultura.db'
```

2. **Recrear base de datos local:**
```bash
python migrate_db.py
```

3. **Ejecutar aplicación:**
```bash
python main.py
```

4. **Las credenciales serán:**
   - Email: admin@agricultura.com
   - Password: admin123

### Opción C: Desplegar en Azure/Servidor (Recomendado para Producción)

Desplegar la aplicación Flask en el mismo servidor/red donde está SQL Server para evitar problemas de conectividad.

## 📋 Verificar Conexión Manualmente

### Desde Python:
```python
import pymssql

try:
    conn = pymssql.connect(
        server='181.198.42.195',
        port='5010',
        user='sa',
        password='6509',
        database='Rend_Cultivo'
    )
    print("✅ Conexión exitosa!")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM app_usuario")
    print(f"Usuarios: {cursor.fetchone()[0]}")
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")
```

### Desde Azure Data Studio (Ya funciona):
```sql
USE [Rend_Cultivo]
GO

SELECT * FROM app_usuario
SELECT * FROM app_finca
SELECT * FROM app_area
SELECT * FROM app_supervisor
SELECT * FROM app_codigo
```

## 🎯 Próximos Pasos

1. **Resolver conectividad:**
   - Contacta al administrador de Azure/IT para agregar tu IP al firewall
   - O usa VPN si está disponible

2. **Una vez conectado:**
```bash
python test_connection.py  # Verificar conexión
python main.py             # Ejecutar aplicación
```

3. **Acceder a la aplicación:**
   - URL: http://127.0.0.1:5000
   - Email: david.herrera@tessacorporation.com
   - Password: admin123

## 📞 Soporte

Si necesitas ayuda con:
- Firewall de Azure → Contacta al administrador de Azure
- VPN → Contacta al equipo de IT
- Errores de la aplicación → Revisa los logs en la terminal

## 🔐 Seguridad

**IMPORTANTE**: Las credenciales están en texto plano en `app/config.py`. En producción, usa variables de entorno:

```bash
export DB_SERVER="181.198.42.195"
export DB_PORT="5010"
export DB_NAME="Rend_Cultivo"
export DB_USER="sa"
export DB_PASSWORD="6509"
```

Y actualiza `app/config.py`:
```python
SQL_SERVER_CONFIG = {
    'server': os.environ.get('DB_SERVER'),
    'port': os.environ.get('DB_PORT'),
    'database': os.environ.get('DB_NAME'),
    'username': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
}
```

