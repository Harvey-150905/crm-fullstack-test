# DECISIONES.md

# MODULO BACKEND

## 1. Uso de Django ORM en lugar de lógica en Python

Se optó por utilizar agregaciones (`Sum`, `Count`) directamente en la base de datos en lugar de calcular resultados con `sum(...)` en Python.

### Motivo
- Mejora de rendimiento (evita traer grandes volúmenes de datos a memoria).
- Cumple con el requisito de performance (<400 ms con 10.000 ventas).

---

## 2. Manejo de timezone basado en shop.tz

Las fechas recibidas en el endpoint se convierten primero a la zona horaria del comercio (`shop.tz`) y luego a UTC para filtrar correctamente en base de datos.

### Motivo
- Django almacena fechas en UTC.
- El enunciado exige que el filtrado sea según la zona horaria del comercio.

---

## 3. Exclusión de ventas refundidas

Se añadió el filtro `refunded=False` en todas las consultas de ventas.

### Motivo
- Requisito funcional explícito del enunciado.

---

## 4. Cálculo correcto del ticket promedio

El promedio se calcula como:

total_cents / número de ventas

en lugar de usar el número de items.

### Motivo
- `avg_ticket` representa el valor medio por venta, no por producto.

---

## 5. Cálculo de top productos con agregaciones

Se utilizó:

- `annotate`
- `Sum`
- `ExpressionWrapper`

para calcular revenue por producto.

### Motivo
- Evitar N+1 queries.
- Ejecutar todos los cálculos en base de datos.

---

## 6. Validación de parámetros

Se validan:
- parámetros obligatorios
- formato de fechas
- existencia del shop

### Motivo
- Robustez del endpoint.
- Cumplimiento de respuestas HTTP 400 y 404.

---

## 7. No uso de InternalReporter

Se evitó completamente el uso de `InternalReporter`.

### Motivo
- Realiza llamadas síncronas de red que bloquean el worker.
- Existe penalización explícita en el test.

---

## 8. Diseño de tests con pytest-django

Se implementaron tests para:

- caso normal
- sin ventas
- exclusión de refunds
- manejo de timezone
- orden de top productos

### Motivo
- Validar lógica crítica del endpoint.
- Asegurar cumplimiento de requisitos funcionales.

# MODULO FRONT

## 1. Uso de Server Component para carga inicial

La página `/reports` se implementó como Server Component para realizar el primer fetch al backend.

### Motivo
- Mejora el tiempo de carga inicial.
- El usuario recibe datos ya renderizados.

## 2. Uso de Client Component para interacción

Se utilizó un Client Component (`ReportsClient`) para manejar cambios de filtros y estado.

### Motivo
- Permite interacción sin recargar la página.
- Mejora la experiencia de usuario.

## 3. Estrategia de fetch

Se realiza un fetch inicial en servidor y posteriores fetch en cliente al cambiar filtros.

### Motivo
- Combina SSR con interactividad.
- Evita recargas completas de la página.


## 4. Uso de skeleton loaders por componente

Se implementaron skeleton loaders independientes para cada sección.

### Motivo
- Mejora la experiencia de carga.
- Evita el uso de un loader global.


## 5. Manejo diferenciado de errores

Se manejan errores 422, 404 y 500 con mensajes distintos en la UI.

### Motivo
- Mejora la claridad para el usuario.
- Facilita identificar el tipo de error.

## 6. Memoización de ShopSelector

Se utilizó `React.memo` en el componente `<ShopSelector/>`.

### Motivo
- Evita re-render innecesario al cambiar solo fechas.
- Mejora el rendimiento.

## 7. Uso de fetch nativo

Se utilizó `fetch` en lugar de librerías externas.

### Motivo
- Cumple con la restricción del enunciado.
- Reduce dependencias.

## 8. Formateo de moneda

Se utilizó `Intl.NumberFormat` para mostrar valores monetarios.

### Motivo
- Cumple con el requisito del enunciado.

## 9. Accesibilidad en tabla

Se añadieron `caption`, `scope="col"` y `aria-busy`.

### Motivo
- Mejora la accesibilidad.
- Cumple con requisitos de accesibilidad.

## Corrección del DateRangeInput

Se evitó el uso de `new Date()` para formatear fechas y se implementó un formateo manual.

### Motivo
- Evita problemas de timezone en frontend.
- Maneja valores vacíos correctamente.

## 10 Validación de rango de fechas

Se valida en el frontend que la fecha "desde" no sea mayor que la fecha "hasta".

### Motivo
- Mejora la experiencia de usuario mostrando errores de forma inmediata.

# Módulo 4 — Selenium

## 1. Estrategia de automatización

Se implementó un flujo básico de automatización utilizando Selenium para realizar el login y simular la interacción inicial con el panel.

### Motivo
- Permite automatizar el acceso al sistema.
- Punto de partida para interactuar con funcionalidades internas.

## 2. Limitación del entorno

El servicio en http://localhost:8765/panel/ no estaba disponible durante la ejecución del test, por lo que no fue posible validar completamente la automatizacion.

### Motivo
- El entorno requerido no fue proporcionado.
- No se pudo inspeccionar el tráfico real del panel.

## 3. Enfoque propuesto

Se planteó el uso de Selenium para autenticación y posteriormente el uso de requests reutilizando la sesión para consumir el endpoint interno.

### Motivo
- Evita depender del DOM.
- Mejora rendimiento frente a scraping tradicional.
- Se alinea con lo solicitado en el enunciado.