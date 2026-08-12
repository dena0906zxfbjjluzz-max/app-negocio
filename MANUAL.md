# Manual de uso — Control de Papas y Pollerías

Guía sencilla para usar la app en el celular o en la computadora.  
*(Para tu amiga / la persona que anota los despachos del día a día.)*

---

## ¿Para qué sirve?

Es un **cuaderno digital** de la venta de papas a pollerías. Sirve para:

1. Anotar **cuántos kilos** salieron cada día y a qué pollería  
2. Saber si pagaron **en efectivo**, por **transferencia** o si **deben (fiado)**  
3. Ver al final de la semana **cuánto se facturó** y a **quién le falta** pedir  
4. Ver **quién debe plata**  
5. Bajar un **Excel** bonito y un **PDF** de resumen  

Si la nube está conectada, **los datos no se pierden** al cerrar la página o apagar el celular.

---

## Cómo entrar

1. Abre el enlace de la app (te lo pasa quien la instaló).  
   Ejemplo: `https://…….streamlit.app`
2. Verás la pantalla de **Usuario** y **Contraseña**.
3. Escribe los datos que te dieron y toca **Ingresar**.

| Si… | Entonces… |
|-----|-----------|
| Usuario o clave mal | Sale error. Vuelve a intentar. |
| Entraste bien | Aparece el menú y el cuaderno. |

> **Importante:** no compartas la contraseña por redes públicas. Solo a la gente de confianza.

### Cerrar sesión

En el menú de la izquierda (o menú lateral en el celular):

1. Toca el icono de **>** o el menú para abrir la barra  
2. Toca **Cerrar sesión**

---

## El menú (4 partes)

Al entrar, a la izquierda (en el celular se abre con el menú):

| Opción | Para qué |
|--------|----------|
| **Cuaderno Semanal** | Anotar cada despacho del día |
| **Gastos** | Compra de papas, transporte, personal, etc. |
| **Resumen Semanal** | Totales, utilidad, gráficos, Excel y PDF |
| **Cuentas por Cobrar** | Solo las pollerías que **deben** |

---

## 1) Cuaderno Semanal — anotar un despacho

Esto es lo que usarás **todos los días**.

### Paso a paso

1. Entra a **Cuaderno Semanal**.  
2. Elige la **Semana de trabajo** (normalmente la de “esta semana”).  
3. Arriba hay pestañas de días: **Lun · Mar · Mié · Jue · Vie · Sáb · Dom**.  
4. Toca el **día de hoy**.  
5. Completa el formulario:

   | Campo | Qué poner |
   |-------|-----------|
   | **Pollería** | Elige el cliente de la lista |
   | **Kilos (kg)** | Escriba la cantidad que quiera (ej. 12, 37.5, 200). No hay saco automático. |
   | **Precio por kilo (S/)** | Precio en soles por kilo |

6. Toque **Guardar despacho**.

Abajo verás la **tabla del día** con:

- Cliente  
- Kilos  
- Precio  
- Monto  
- Estado  

Y los totales: **Kilos hoy** y **Total hoy (S/)**.

### Si anotaste mal (corregir o borrar)

Más abajo de la tabla, en **Corregir o borrar**:

1. Elige el despacho incorrecto en la lista.  
2. Cambia lo que esté mal (cliente, kilos, precio o estado).  
3. Toca **Guardar corrección**  
   **o**  
4. Toca **Borrar despacho** si no debió existir.

Los totales se actualizan solos.

### Consejos del día a día

- Anota en el momento, o al final del reparto — no dejes varios días sin cargar.  
- Si es **fiado**, elige siempre **Fiado / Debe**, así aparece en Cuentas por Cobrar.  
- Cuando te pague, ve a **Cuentas por Cobrar** y márcalo como cobrado (o edítalo en el día y cambia el estado).

---

## 2) Resumen Semanal — cierre de la semana

Úsalo al final de la semana (o cuando quieras ver cómo vas).

1. Entra a **Resumen Semanal**.  
2. Elige la **semana** que quieres ver.  

Verás:

### Clientes sin pedido  
Pollerías de la lista a las que **aún no les despachaste** esa semana.  
(Así no se te olvida alguna del reparto habitual.)

### Totales  
- Kilos de la semana  
- Facturación en soles  

### Tabla completa  
Todos los despachos de esa semana.

### Descargar reportes  

| Botón | Qué entrega |
|-------|-------------|
| **Descargar Excel del cuaderno** | Archivo `.xlsx` con varias hojas (resumen, días, por cobrar). Ideal para guardar o imprimir. |
| **Descargar PDF resumen** | Una hoja de resumen con totales y detalle. |

En el celular: el archivo se descarga y lo puedes abrir con Excel, Google Drive o el lector de PDF.

---

## 3) Cuentas por Cobrar — quién debe

1. Entra a **Cuentas por Cobrar**.  
2. Si nadie debe → mensaje de **todo cobrado**.  
3. Si hay deudas → lista con cliente, día, kilos y **monto que debe**.  
4. Para marcar un cobro:
   - Elige la entrega  
   - Elige cómo pagó: **efectivo** o **transferencia**  
   - Toca **Registrar cobro**  

Esa fila **sale de la lista de deudas**.

---

## ¿Se pierden los datos si cierro la app?

| Situación | Qué pasa |
|-----------|----------|
| La app dice **“Datos en la nube (Supabase)”** (menú lateral) | **No se pierden.** Quedan guardados en internet. |
| La app dice **“Sin nube: se pierden al cerrar”** | Solo están en esa sesión. **Avisa a quien instaló la app** para conectar la nube. |

Si algo no carga, en el menú hay **Recargar desde la nube** (solo cuando hay nube).

---

## En el celular

1. Abre el enlace en **Chrome** o **Safari**.  
2. Para el menú lateral, usa la flecha o el icono de menú (arriba a la izquierda).  
3. Es más cómodo **vertical** (celular de pie).  
4. Puedes agregar la página a la pantalla de inicio (como una app):
   - Chrome → menú → **Agregar a la pantalla de inicio**

---

## Problemas frecuentes

| Problema | Qué hacer |
|----------|-----------|
| No entra el usuario | Revisa mayúsculas y la clave. Pídele al dueño que te confirme. |
| Guardé y no aparece | Espera un segundo; o cierra y vuelve a entrar. Si hay nube, usa **Recargar desde la nube**. |
| Falta una pollería en la lista | Pídele al dueño que la agregue en el sistema (por ahora la lista se configura en la app). |
| No puedo bajar el Excel | Prueba en computadora o revisa permisos de descarga del celular. |
| Página en blanco o error raro | Refresca la página. Si sigue, avisa al dueño con una captura. |

---

## Resumen ultra corto (para imprimir o WhatsApp)

```
1. Entra con usuario y contraseña
2. Cuaderno Semanal → elige la semana → elige el día
3. Pollería + kilos + precio + forma de pago → Guardar
4. Si te equivocaste → Corregir o borrar
5. Al final de la semana → Resumen → Excel o PDF
6. Deudas → Cuentas por Cobrar → Registrar cobro
7. Cerrar sesión cuando termines
```

---

## Contacto

Si algo no funciona o necesitas cambiar la clave, avisa a quien te pasó este sistema (quien instaló la app y tiene el acceso a Streamlit / Supabase).

---

*Manual de uso — Control de Papas y Pollerías · pensado para uso diario en terreno.*
