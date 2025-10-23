# Sistema de Gestión Agrícola 🌾

Sistema web para la administración de fincas, áreas de cultivo, supervisores y códigos de cosechadores.

## 🚀 Características Principales

### ✅ Gestión de Usuarios y Roles
- **Admin**: Control total del sistema
- **RRHH**: Gestión de personal y asignaciones
- **Jefe de Cultivo**: Administración de áreas y códigos

### ✅ Gestión de Fincas
- Crear y administrar múltiples fincas
- Asignar usuarios específicos a cada finca
- Aislamiento de datos por finca

### ✅ Gestión de Áreas de Cultivo
- Creación individual o masiva (1,2,3,4,5)
- Asignación de supervisores a áreas
- Control de áreas activas/inactivas

### ✅ Gestión de Códigos de Cosechadores
- **Códigos únicos por finca** (no hay conflictos entre fincas)
- Creación individual o por rangos (001-060)
- **Selección múltiple con checkboxes**
- **Selección arrastrando (drag-to-select)** 🎯
- Asignación flexible a áreas

### ✅ Gestión de Supervisores
- Creación con claves de acceso
- Asignación a áreas específicas
- Control de accesos activos/inactivos

## 🛠️ Instalación

### Requisitos
- Python 3.8+
- pip

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
```bash
cd Rendimientos_CRUD_MASTER
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**
- En macOS/Linux:
```bash
source venv/bin/activate
```
- En Windows:
```bash
venv\Scripts\activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Crear la base de datos**

**Opción A: SQLite (Desarrollo local)**
```bash
python migrate_db.py
```

**Opción B: SQL Server (Producción)**
```bash
# 1. Ejecutar el script SQL en Azure Data Studio
# Abre el archivo sql_server_schema.sql y ejecútalo en tu SQL Server

# 2. Migrar con Python
python migrate_sql_server.py
```

6. **Ejecutar la aplicación**
```bash
python main.py
```

7. **Acceder a la aplicación**
Abrir el navegador en: `http://127.0.0.1:5000`

## 🔑 Credenciales por Defecto

- **Email**: admin@agricultura.com
- **Password**: admin123

## 📋 Flujo de Trabajo

### Como Administrador:

1. **Crear Fincas**
   - Ve a "Fincas" → "Nueva Finca"
   - Ingresa nombre y ubicación

2. **Crear Usuarios**
   - Ve a "Usuarios" → "Nuevo Usuario"
   - Selecciona rol (RRHH o Jefe de Cultivo)
   - El usuario se crea sin finca asignada

3. **Asignar Usuarios a Fincas**
   - En "Usuarios", haz clic en "Asignar Finca"
   - Selecciona la finca correspondiente

### Como Usuario RRHH/Jefe de Cultivo:

1. **Crear Áreas**
   - Ve a "Áreas" → "Nueva Área"
   - Opción individual: Ingresa nombre de área
   - Opción múltiple: Ingresa "1,2,3,4,5" para crear 5 áreas

2. **Crear Supervisores**
   - Ve a "Supervisores" → "Nuevo Supervisor"
   - Ingresa datos y clave de acceso
   - Luego asigna a un área

3. **Crear Códigos**
   - Ve a "Códigos" → "Nuevo Código"
   - Opción individual: Ingresa datos de un código
   - Opción rango: Ingresa "001-060" para crear 60 códigos
   - Puedes crear sin área (se asigna después)

4. **Asignar Códigos a Áreas** 🎯
   - Ve a "Códigos" → "Asignar Códigos a Área"
   - **Método 1**: Haz clic en cada fila para seleccionar
   - **Método 2**: Mantén presionado y arrastra el mouse sobre las filas
   - **Método 3**: Usa "Seleccionar Todos"
   - Selecciona el área destino
   - Haz clic en "Asignar"

## 🎨 Funcionalidades Destacadas

### Selección Drag-to-Select
La interfaz permite seleccionar múltiples códigos de manera rápida y eficiente:
- Haz clic en una fila para seleccionarla
- Mantén presionado el botón del mouse y arrastra sobre las filas
- Todos los códigos por los que pases quedarán seleccionados
- Contador en tiempo real de códigos seleccionados

### Códigos Únicos por Finca
Cada finca tiene su propio conjunto de códigos:
- Finca A puede tener códigos 001-060
- Finca B puede tener códigos 001-060
- No hay conflictos ni duplicados
- Los usuarios solo ven códigos de su finca

### Creación Masiva
Ahorra tiempo con las opciones de creación masiva:
- **Áreas**: "1,2,3,4,5" crea 5 áreas
- **Códigos**: "001-060" crea 60 códigos automáticamente

## 📁 Estructura del Proyecto

```
Rendimientos_CRUD_MASTER/
├── app/
│   ├── __init__.py          # Inicialización de Flask
│   ├── config.py            # Configuración
│   ├── models.py            # Modelos de base de datos
│   ├── routes/
│   │   ├── auth.py          # Autenticación
│   │   ├── dashboard.py     # Dashboard
│   │   ├── usuarios.py      # Gestión de usuarios
│   │   ├── fincas.py        # Gestión de fincas
│   │   ├── areas.py         # Gestión de áreas
│   │   ├── supervisores.py  # Gestión de supervisores
│   │   └── codigos.py       # Gestión de códigos
│   └── templates/           # Plantillas HTML
├── instance/
│   └── agricultura.db       # Base de datos SQLite
├── main.py                  # Punto de entrada
├── migrate_db.py            # Script de migración
└── README.md                # Este archivo
```

## 🔧 Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **ORM**: SQLAlchemy
- **Base de Datos**: SQLite
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Iconos**: Font Awesome

## 📝 Notas Importantes

1. **Entorno de Desarrollo**: Esta aplicación usa SQLite y el servidor de desarrollo de Flask. Para producción, considera usar PostgreSQL y un servidor WSGI.

2. **Seguridad**: Cambia la `SECRET_KEY` en `app/config.py` antes de usar en producción.

3. **Backup**: Haz copias de seguridad regulares de `instance/agricultura.db`.

4. **Migración de Datos**: Si cambias el modelo de datos, ejecuta `python migrate_db.py` (esto recreará la base de datos).

## 🐛 Solución de Problemas

### Error: "Unable to open database file"
- Asegúrate de que existe el directorio `instance/`
- Ejecuta `python migrate_db.py`

### Error: "UNIQUE constraint failed"
- Los códigos deben ser únicos dentro de cada finca
- Verifica que no estés intentando crear códigos duplicados

### La aplicación no carga
- Verifica que el entorno virtual esté activado
- Asegúrate de tener todas las dependencias instaladas
- Revisa que el puerto 5000 no esté en uso

## 📞 Soporte

Para reportar problemas o sugerencias, contacta al equipo de desarrollo.

---

**Versión**: 1.0  
**Última actualización**: Octubre 2025
