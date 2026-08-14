# Manual de uso — Liseth · Papas y Pollerías

Guía sencilla para el celular o la computadora.  
*(Para quien anota los despachos y gastos del día a día.)*

---

## ¿Para qué sirve?

Es el **cuaderno digital** del negocio. Sirve para:

1. Anotar **cuántos kilos** salieron cada día y a qué pollería  
2. Registrar si pagaron **efectivo**, **transferencia** o si **deben (fiado)**  
3. Anotar **gastos** (compra de papas, transporte, personal, etc.)  
4. Ver **facturación, gastos y utilidad neta** de la semana  
5. Ver **gráficos** (quién compra más, ventas por día, gastos)  
6. Ver **quién debe plata** y marcar cobros  
7. Descargar **Excel** y **PDF** del resumen  

Con la nube conectada, **los datos no se pierden** al cerrar la página.

---

## Cómo entrar

1. Abre el enlace de la app.  
2. Escribe **Usuario** y **Contraseña**.  
3. Toca **Ingresar**.

| Si… | Entonces… |
|-----|-----------|
| Usuario o clave mal | Sale error. Intenta de nuevo. |
| Entraste bien | Ves el menú y el cuaderno. |

> No compartas la contraseña. Solo con gente de confianza.

### Cerrar sesión

En el menú de la izquierda (en el celular: ícono de menú arriba a la izquierda) → **Cerrar sesión**.

---

## El menú (4 partes)

| Opción | Para qué |
|--------|----------|
| **Cuaderno Semanal** | Anotar cada despacho del día |
| **Gastos** | Compra de papas, flete, personal u otros |
| **Resumen Semanal** | Totales, utilidad, gráficos, Excel y PDF |
| **Cuentas por Cobrar** | Pollerías que **deben** |

Si hay nube, también verás **Recargar desde la nube** (por si algo no aparece al instante).

---

## 1) Cuaderno Semanal — anotar un despacho

Úsalo **todos los días**.

1. Entra a **Cuaderno Semanal**.  
2. Elige la **Semana de trabajo**.  
3. Toca el **día** (Lun · Mar · Mié · Jue · Vie · Sáb · Dom).  
4. Completa:

   | Campo | Qué poner |
   |-------|-----------|
   | **Pollería** | Cliente de la lista |
   | **Kilos (kg)** | Cantidad real (ej. 12, 37.5, 200) |
   | **Precio por kilo (S/)** | Precio en soles |
   | **Estado del pago** | Efectivo / Transferencia / Fiado |

5. Toca **Guardar despacho**.

Abajo verás la tabla del día y los totales (**Kilos hoy** y **Total hoy**).

### Si anotaste mal

En **Corregir o borrar**:

1. Elige el despacho.  
2. Cambia lo que esté mal → **Guardar corrección**  
   **o** → **Borrar despacho**.

### Consejos

- Anota el mismo día del reparto.  
- Si es fiado, elige **Fiado / Debe** para que salga en Cuentas por Cobrar.  
- Cuando te paguen, ve a **Cuentas por Cobrar** y registra el cobro.

---

## 2) Gastos — lo que inviertes

Para saber la **utilidad real** (ventas − gastos).

1. Entra a **Gastos**.  
2. Elige la **semana**.  
3. Completa:

   | Campo | Ejemplo |
   |-------|---------|
   | **Día** | Lunes |
   | **Categoría** | Compra de papas, Transporte, Personal… |
   | **Monto (S/)** | 150.00 |
   | **Concepto** | Nota opcional (ej. “mayorista”) |

4. Toca **Guardar gasto**.

También puedes **corregir o borrar** un gasto igual que en el cuaderno.

---

## 3) Resumen Semanal — cierre

1. Entra a **Resumen Semanal**.  
2. Elige la semana.

Verás:

| Bloque | Qué muestra |
|--------|-------------|
| **Totales** | Kilos, facturación, gastos, **utilidad neta** |
| **Clientes sin pedido** | Pollerías a las que aún no despachaste |
| **Gráficos** | Por pollería, por día, gastos por categoría, semanas |
| **Tablas** | Detalle de ventas y gastos |
| **Descargas** | Excel del cuaderno y PDF resumen |

En el celular el archivo se abre con Excel, Drive o el lector de PDF.

---

## 4) Cuentas por Cobrar — quién debe

1. Entra a **Cuentas por Cobrar**.  
2. Si nadie debe → **todo cobrado**.  
3. Si hay deudas → lista con cliente, día, kilos y monto.  
4. Para cobrar:
   - Elige la entrega  
   - Elige **efectivo** o **transferencia**  
   - Toca **Registrar cobro**  

Esa entrega **sale de la lista de deudas**.

---

## ¿Se pierden los datos?

| Situación | Qué pasa |
|-----------|----------|
| Nube conectada (Supabase en secrets) | **No se pierden.** |
| Sin nube | Solo en esa sesión; se pueden perder al cerrar. |

Si algo no carga: **Recargar desde la nube**.

---

## En el celular

1. Abre el enlace en Chrome o Safari.  
2. Menú lateral: ícono arriba a la izquierda.  
3. Mejor en vertical.  
4. Puedes **Agregar a la pantalla de inicio** para usarla como app.

---

## Problemas frecuentes

| Problema | Qué hacer |
|----------|-----------|
| No entra el usuario | Revisa mayúsculas y clave. |
| Guardé y no aparece | Espera un momento o **Recargar desde la nube**. |
| Error en Gastos / falta tabla | Quien instaló debe ejecutar el SQL de gastos en Supabase. |
| Falta una pollería en la lista | Pedirle al dueño que la agregue en el sistema. |
| No baja el Excel | Probar en computadora o revisar permisos de descarga. |
| Página en blanco | Refrescar. Si sigue, avisar con captura. |

---

## Resumen corto (WhatsApp)

```
1. Entra con usuario y contraseña
2. Cuaderno → semana → día → pollería + kilos + precio + pago → Guardar
3. Gastos → anota compra / flete / personal
4. Si te equivocaste → Corregir o borrar
5. Resumen → utilidad, gráficos, Excel o PDF
6. Deudas → Cuentas por Cobrar → Registrar cobro
7. Cerrar sesión al terminar
```

---

## Contacto

Si algo no funciona o hay que cambiar la clave, avisa a quien instaló la app (Streamlit / Supabase).

---

*Manual Liseth · Papas y Pollerías · uso diario en terreno.*
