# Endpoints creados

Este archivo resume los endpoints nuevos implementados para carritos, items, órdenes y pagos.

## 1) Carritos

### GET /carritos
- Descripción: Lista todos los carritos.
- Respuesta: Arreglo de registros de la tabla cart.

### POST /carritos
- Descripción: Crea un carrito.
- Body JSON:

```json
{
  "user_id": 1
}
```

- Respuesta esperada:

```json
{
  "message": "Carrito creado exitosamente",
  "idCarrito": 10
}
```

---

## 2) Cart Items

### GET /cart-items
- Descripción: Lista todos los items de carrito.
- Respuesta: Arreglo de registros de la tabla cart_items.

### POST /cart-items
- Descripción: Crea un item de carrito.
- Body JSON:

```json
{
  "cart_id": 1,
  "product_id": 2,
  "quantity": 3
}
```

- Respuesta esperada:

```json
{
  "message": "Item de carrito creado exitosamente",
  "idCartItem": 20
}
```

---

## 3) Orders

### GET /orders
- Descripción: Lista todas las órdenes.
- Respuesta: Arreglo de registros de la tabla orders.

### POST /orders
- Descripción: Crea una orden.
- Body JSON (mínimo):

```json
{
  "user_id": 1,
  "status": "pending",
  "total": 150.50
}
```

- Body JSON (incluyendo fecha opcional):

```json
{
  "user_id": 1,
  "status": "pending",
  "total": 150.50,
  "created_at": "2026-02-27T10:00:00"
}
```

- Respuesta esperada:

```json
{
  "message": "Orden creada exitosamente",
  "idOrder": 30
}
```

---

## 4) Order Items

### GET /order-items
- Descripción: Lista todos los items de orden.
- Respuesta: Arreglo de registros de la tabla order_items.

### POST /order-items
- Descripción: Crea un item de orden.
- Body JSON:

```json
{
  "order_id": 1,
  "product_id": 2,
  "quantity": 1,
  "price": 49.99
}
```

- Respuesta esperada:

```json
{
  "message": "Item de orden creado exitosamente",
  "idOrderItem": 40
}
```

---

## 5) Payments

### GET /payments
- Descripción: Lista todos los pagos.
- Respuesta: Arreglo de registros de la tabla payments.

### POST /payments
- Descripción: Crea un pago.
- Body JSON (mínimo):

```json
{
  "order_id": 1
}
```

- Body JSON (completo):

```json
{
  "order_id": 1,
  "provider": "stripe",
  "status": "approved",
  "amount": 150.50,
  "created_at": "2026-02-27T10:30:00"
}
```

- Respuesta esperada:

```json
{
  "message": "Pago creado exitosamente",
  "idPayment": 50
}
```

---

## Notas rápidas

- Todos los POST devuelven código 201 cuando se crea correctamente.
- Si ocurre un error de integridad de datos, los endpoints retornan código 400.
