-- =============================================
-- Script para crear tablas en SQL Server
-- Base de datos: Rend_Cultivo
-- Prefijo: app_
-- =============================================

USE [Rend_Cultivo]
GO

-- =============================================
-- 1. Tabla app_finca
-- =============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='app_finca' AND xtype='U')
BEGIN
    CREATE TABLE [dbo].[app_finca](
        [id] [int] IDENTITY(1,1) NOT NULL,
        [nombre] [nvarchar](100) NOT NULL,
        [ubicacion] [nvarchar](200) NULL,
        [descripcion] [ntext] NULL,
        [activa] [bit] NOT NULL DEFAULT 1,
        [fecha_creacion] [datetime] NOT NULL DEFAULT GETDATE(),
        CONSTRAINT [PK_app_finca] PRIMARY KEY CLUSTERED ([id] ASC)
    )
    PRINT 'Tabla app_finca creada exitosamente'
END
ELSE
BEGIN
    PRINT 'Tabla app_finca ya existe'
END
GO

-- =============================================
-- 2. Tabla app_usuario
-- =============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='app_usuario' AND xtype='U')
BEGIN
    CREATE TABLE [dbo].[app_usuario](
        [id] [int] IDENTITY(1,1) NOT NULL,
        [username] [nvarchar](80) NOT NULL,
        [email] [nvarchar](120) NOT NULL,
        [password_hash] [nvarchar](120) NOT NULL,
        [rol] [nvarchar](20) NOT NULL,
        [finca_id] [int] NULL,
        [activo] [bit] NOT NULL DEFAULT 1,
        [fecha_creacion] [datetime] NOT NULL DEFAULT GETDATE(),
        CONSTRAINT [PK_app_usuario] PRIMARY KEY CLUSTERED ([id] ASC),
        CONSTRAINT [UQ_app_usuario_username] UNIQUE ([username]),
        CONSTRAINT [UQ_app_usuario_email] UNIQUE ([email])
    )
    
    -- Foreign Key a app_finca
    ALTER TABLE [dbo].[app_usuario] 
    ADD CONSTRAINT [FK_app_usuario_finca] 
    FOREIGN KEY([finca_id]) REFERENCES [dbo].[app_finca] ([id])
    
    PRINT 'Tabla app_usuario creada exitosamente'
END
ELSE
BEGIN
    PRINT 'Tabla app_usuario ya existe'
END
GO

-- =============================================
-- 3. Tabla app_supervisor
-- =============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='app_supervisor' AND xtype='U')
BEGIN
    CREATE TABLE [dbo].[app_supervisor](
        [id] [int] IDENTITY(1,1) NOT NULL,
        [nombre] [nvarchar](100) NOT NULL,
        [apellido] [nvarchar](100) NOT NULL,
        [telefono] [nvarchar](20) NULL,
        [email] [nvarchar](120) NULL,
        [clave_acceso] [nvarchar](50) NOT NULL,
        [activo] [bit] NOT NULL DEFAULT 1,
        [fecha_creacion] [datetime] NOT NULL DEFAULT GETDATE(),
        [fecha_ultimo_acceso] [datetime] NULL,
        CONSTRAINT [PK_app_supervisor] PRIMARY KEY CLUSTERED ([id] ASC),
        CONSTRAINT [UQ_app_supervisor_clave] UNIQUE ([clave_acceso])
    )
    PRINT 'Tabla app_supervisor creada exitosamente'
END
ELSE
BEGIN
    PRINT 'Tabla app_supervisor ya existe'
END
GO

-- =============================================
-- 4. Tabla app_area
-- =============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='app_area' AND xtype='U')
BEGIN
    CREATE TABLE [dbo].[app_area](
        [id] [int] IDENTITY(1,1) NOT NULL,
        [nombre] [nvarchar](100) NOT NULL,
        [descripcion] [ntext] NULL,
        [finca_id] [int] NOT NULL,
        [supervisor_id] [int] NULL,
        [activa] [bit] NOT NULL DEFAULT 1,
        [fecha_creacion] [datetime] NOT NULL DEFAULT GETDATE(),
        CONSTRAINT [PK_app_area] PRIMARY KEY CLUSTERED ([id] ASC)
    )
    
    -- Foreign Keys
    ALTER TABLE [dbo].[app_area] 
    ADD CONSTRAINT [FK_app_area_finca] 
    FOREIGN KEY([finca_id]) REFERENCES [dbo].[app_finca] ([id])
    
    ALTER TABLE [dbo].[app_area] 
    ADD CONSTRAINT [FK_app_area_supervisor] 
    FOREIGN KEY([supervisor_id]) REFERENCES [dbo].[app_supervisor] ([id])
    
    PRINT 'Tabla app_area creada exitosamente'
END
ELSE
BEGIN
    PRINT 'Tabla app_area ya existe'
END
GO

-- =============================================
-- 5. Tabla app_codigo
-- =============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='app_codigo' AND xtype='U')
BEGIN
    CREATE TABLE [dbo].[app_codigo](
        [id] [int] IDENTITY(1,1) NOT NULL,
        [codigo] [nvarchar](20) NOT NULL,
        [nombre_persona] [nvarchar](100) NOT NULL,
        [apellido_persona] [nvarchar](100) NOT NULL,
        [telefono] [nvarchar](20) NULL,
        [area_id] [int] NULL,
        [finca_id] [int] NOT NULL,
        [activo] [bit] NOT NULL DEFAULT 1,
        [fecha_creacion] [datetime] NOT NULL DEFAULT GETDATE(),
        CONSTRAINT [PK_app_codigo] PRIMARY KEY CLUSTERED ([id] ASC)
    )
    
    -- Foreign Keys
    ALTER TABLE [dbo].[app_codigo] 
    ADD CONSTRAINT [FK_app_codigo_area] 
    FOREIGN KEY([area_id]) REFERENCES [dbo].[app_area] ([id])
    
    ALTER TABLE [dbo].[app_codigo] 
    ADD CONSTRAINT [FK_app_codigo_finca] 
    FOREIGN KEY([finca_id]) REFERENCES [dbo].[app_finca] ([id])
    
    -- Constraint único: código debe ser único dentro de cada finca
    ALTER TABLE [dbo].[app_codigo] 
    ADD CONSTRAINT [UQ_app_codigo_finca] 
    UNIQUE ([codigo], [finca_id])
    
    PRINT 'Tabla app_codigo creada exitosamente'
END
ELSE
BEGIN
    PRINT 'Tabla app_codigo ya existe'
END
GO

-- =============================================
-- 6. Insertar datos iniciales
-- =============================================

-- Usuario admin por defecto
IF NOT EXISTS (SELECT 1 FROM [dbo].[app_usuario] WHERE username = 'admin')
BEGIN
    INSERT INTO [dbo].[app_usuario] (username, email, password_hash, rol, activo)
    VALUES ('admin', 'admin@agricultura.com', 'scrypt:32768:8:1$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4L/8KzK1aK', 'admin', 1)
    PRINT 'Usuario admin creado'
END
ELSE
BEGIN
    PRINT 'Usuario admin ya existe'
END

-- Finca de ejemplo
IF NOT EXISTS (SELECT 1 FROM [dbo].[app_finca] WHERE nombre = 'Finca Ejemplo')
BEGIN
    INSERT INTO [dbo].[app_finca] (nombre, ubicacion, descripcion, activa)
    VALUES ('Finca Ejemplo', 'Ubicación de ejemplo', 'Finca creada automáticamente', 1)
    PRINT 'Finca de ejemplo creada'
END
ELSE
BEGIN
    PRINT 'Finca de ejemplo ya existe'
END

-- =============================================
-- 7. Crear índices para optimizar consultas
-- =============================================

-- Índices para app_usuario
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_app_usuario_finca_id')
BEGIN
    CREATE INDEX [IX_app_usuario_finca_id] ON [dbo].[app_usuario] ([finca_id])
END

-- Índices para app_area
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_app_area_finca_id')
BEGIN
    CREATE INDEX [IX_app_area_finca_id] ON [dbo].[app_area] ([finca_id])
END

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_app_area_supervisor_id')
BEGIN
    CREATE INDEX [IX_app_area_supervisor_id] ON [dbo].[app_area] ([supervisor_id])
END

-- Índices para app_codigo
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_app_codigo_area_id')
BEGIN
    CREATE INDEX [IX_app_codigo_area_id] ON [dbo].[app_codigo] ([area_id])
END

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_app_codigo_finca_id')
BEGIN
    CREATE INDEX [IX_app_codigo_finca_id] ON [dbo].[app_codigo] ([finca_id])
END

PRINT 'Índices creados exitosamente'
GO

-- =============================================
-- 8. Verificar creación de tablas
-- =============================================
SELECT 
    'app_finca' as tabla, COUNT(*) as registros FROM [dbo].[app_finca]
UNION ALL
SELECT 
    'app_usuario' as tabla, COUNT(*) as registros FROM [dbo].[app_usuario]
UNION ALL
SELECT 
    'app_supervisor' as tabla, COUNT(*) as registros FROM [dbo].[app_supervisor]
UNION ALL
SELECT 
    'app_area' as tabla, COUNT(*) as registros FROM [dbo].[app_area]
UNION ALL
SELECT 
    'app_codigo' as tabla, COUNT(*) as registros FROM [dbo].[app_codigo]

PRINT '============================================='
PRINT 'Script completado exitosamente'
PRINT 'Tablas creadas con prefijo app_'
PRINT 'Usuario admin: admin@agricultura.com'
PRINT 'Password: admin123'
PRINT '============================================='
