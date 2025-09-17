# Migración a PostgreSQL - Sistema de Loterías

Este documento describe el proceso de migración del sistema de ventas de almacenamiento JSON a PostgreSQL.

## Archivos Modificados/Creados

### Nuevos Archivos
- `data/create_ventas_table.py` - Script para crear la tabla de ventas en PostgreSQL
- `services/ventas_service_db.py` - Nuevo servicio de ventas que usa PostgreSQL
- `migrate_to_database.py` - Script de migración automática
- `test_database_ventas.py` - Script de pruebas del sistema
- `MIGRACION_POSTGRESQL.md` - Este archivo de documentación

### Archivos Modificados
- `models/venta_model.py` - Actualizado para soportar campos de base de datos

## Estructura de la Tabla de Ventas

```sql
CREATE TABLE ventas (
    id_venta SERIAL PRIMARY KEY,
    id_loteria INTEGER NOT NULL,
    cantidad_fracciones_vendidas INTEGER NOT NULL CHECK (cantidad_fracciones_vendidas > 0),
    nombre_cliente VARCHAR(100) NOT NULL,
    nombre_vendedor VARCHAR(100) NOT NULL,
    fecha_venta DATE NOT NULL DEFAULT CURRENT_DATE,
    valor_venta DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Índices Creados
- `idx_ventas_id_loteria` - Para consultas por lotería
- `idx_ventas_fecha_venta` - Para consultas por fecha
- `idx_ventas_nombre_cliente` - Para búsquedas por cliente
- `idx_ventas_nombre_vendedor` - Para búsquedas por vendedor

## Proceso de Migración

### Opción 1: Migración Automática (Recomendada)

1. **Ejecutar el script de migración:**
   ```bash
   python migrate_to_database.py
   ```

2. **El script realizará automáticamente:**
   - Crear copia de seguridad de `data/ventas.json`
   - Crear la tabla de ventas en PostgreSQL
   - Migrar todos los datos existentes
   - Verificar la integridad de los datos
   - Actualizar los imports en los archivos principales

### Opción 2: Migración Manual

1. **Crear la tabla:**
   ```bash
   python data/create_ventas_table.py
   ```

2. **Verificar la migración:**
   ```bash
   python test_database_ventas.py
   ```

3. **Actualizar imports manualmente:**
   - Cambiar `from services.ventas_service import` por `from services.ventas_service_db import` en los archivos que lo usen

## Nuevas Funcionalidades

### VentasServiceDB
El nuevo servicio incluye todas las funcionalidades del anterior más:

- **Gestión de conexiones:** Manejo automático de conexiones a la base de datos
- **Transacciones:** Operaciones atómicas con rollback automático en caso de error
- **Estadísticas avanzadas:** Método `get_ventas_stats()` para obtener estadísticas detalladas
- **Actualización de registros:** Método `update_venta()` para modificar ventas existentes
- **Eliminación de registros:** Método `delete_venta()` para eliminar ventas

### Métodos Disponibles

```python
# Obtener todas las ventas
ventas = get_all_ventas()

# Buscar venta por ID
venta = find_venta_by_id(1)

# Buscar ventas por lotería
ventas_loteria = find_ventas_by_loteria(1)

# Agregar nueva venta
nueva_venta = add_new_venta(
    id_loteria=1,
    cantidad_fracciones_vendidas=2,
    nombre_cliente="Juan Pérez",
    nombre_vendedor="María García"
)

# Obtener ventas por rango de fechas
ventas_rango = get_ventas_by_date_range(
    fecha_inicio=date(2025, 1, 1),
    fecha_fin=date(2025, 12, 31)
)

# Calcular totales
total = calculate_total_ventas()
ventas_por_loteria = calculate_ventas_por_loteria()

# Obtener estadísticas
stats = get_ventas_stats()
```

## Verificación Post-Migración

### 1. Ejecutar Pruebas
```bash
python test_database_ventas.py
```

### 2. Verificar Datos
- Comparar el número de ventas en JSON vs PostgreSQL
- Verificar que los totales coincidan
- Probar operaciones CRUD básicas

### 3. Verificar Rendimiento
- Las consultas deben ejecutarse en menos de 1 segundo
- Los índices mejoran el rendimiento de las consultas

## Rollback (Si es necesario)

Si necesitas volver al sistema JSON:

1. **Restaurar el servicio original:**
   - Cambiar imports de `ventas_service_db` a `ventas_service`

2. **Restaurar datos (si es necesario):**
   - Usar la copia de seguridad creada en `data/ventas_backup_YYYYMMDD_HHMMSS.json`

## Consideraciones de Seguridad

- Las contraseñas de la base de datos están en `config/database.py`
- Se recomienda usar variables de entorno para datos sensibles en producción
- La conexión usa SSL (sslmode=require)

## Mantenimiento

### Backup Regular
```sql
-- Crear backup de la tabla ventas
pg_dump -h hostname -U username -d database -t ventas > ventas_backup.sql
```

### Monitoreo
- Revisar logs de conexión
- Monitorear el rendimiento de consultas
- Verificar el espacio en disco

## Soporte

Si encuentras problemas durante la migración:

1. Revisar los logs de error en la consola
2. Verificar la conexión a PostgreSQL
3. Ejecutar las pruebas de verificación
4. Revisar que todos los archivos de configuración estén correctos

## Próximos Pasos

Después de la migración exitosa:

1. **Eliminar archivos JSON:** Una vez verificado que todo funciona, puedes eliminar `data/ventas.json`
2. **Optimizar consultas:** Revisar y optimizar consultas frecuentes
3. **Implementar cache:** Considerar implementar cache para consultas frecuentes
4. **Monitoreo:** Configurar alertas para problemas de conexión o rendimiento
