# Ejemplo práctico de instanciación y uso de métodos

## Objetivo del ejemplo

En este ejemplo se demuestra:

- La **instanciación** de un objeto a partir de una clase.
- El uso de un **método** propio del objeto.
- La aplicación del **polimorfismo** en el cálculo de la cuota mensual.

---

## Código del ejemplo

```python
from modelos.clientes import ClientePremium

# Instanciación: creación de un objeto ClientePremium
cliente = ClientePremium(
    cliente_id=4,
    nombre="Mario",
    email="mario@gmail.com",
    telefono="912345678",
    activo=True
)

# Uso de método: cálculo de la cuota mensual
monto_base = 30000
cuota = cliente.calcular_cuota_mensual(monto_base)

print(cliente)
print("Cuota mensual a pagar:", cuota, "CLP")

## Explicación

En primer lugar, se crea un objeto de tipo `ClientePremium`. Este proceso se denomina **instanciación**, ya que se construye un objeto concreto a partir de una clase.

Posteriormente, se utiliza el método `calcular_cuota_mensual()`, el cual recibe un monto base y aplica automáticamente el descuento correspondiente al tipo de cliente (10% en el caso Premium).

Si el objeto fuera de tipo `ClienteRegular` o `ClienteCorporativo`, el método se ejecutaría de la misma forma, pero el descuento aplicado sería diferente. Esto demuestra el uso de **polimorfismo**, ya que cada subclase implementa su propia versión del método `calcular_descuento()`.




