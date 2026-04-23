# BUGS.md

## 1. Rango de fechas incorrecto
El codigo utilizaba "created_at__date__lt=d_to", esto hace que se excluya el ultimo dia.

### Impacto
Mal calculo de ventas.

### Corrección
Se cambio a un rango inclusivo y se implemento manejo correcto de timezone basado en "shop.tz".

---

## 2. Cálculo incorrecto del promedio

El promedio se calculaba dividiendo el total entre el número de "SaleItem", en lugar del número de ventas.

### Impacto
El valor de "avg_ticket" era incorrecto.

### Corrección
Se cambió para usar el número de ventas ("sales.count()"), que corresponde al ticket.

---

## 3. No se excluían ventas refundidas

El query no filtraba las ventas con "refunded=True".

### Impacto
Las ventas reembolsadas se incluían en los cálculos, incumpliendo los requisitos.

### Corrección
Se añadió el filtro "refunded=False".

---

## 4. Formateo incorrecto de fechas en frontend

El componente utilizaba "new Date(d).toLocaleDateString()" para formatear fechas.

### Impacto
Dependiendo del navegador y timezone, la fecha podía mostrarse con un día incorrecto o generar inconsistencias.

### Corrección
Se reemplazó por un formateo manual para evitar problemas de timezone y manejar valores vacíos correctamente.