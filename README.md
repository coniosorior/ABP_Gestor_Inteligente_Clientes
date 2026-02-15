# Gestor Inteligente de Clientes (GIC)

## Descripción del sistema
Es un sistema por consola desarrollada en Python que permite administrar clientes con suscripción mensual, aplicando descuentos diferenciados según su categoría. El sistema fue diseñado utilizando principios de **Programación Orientada a Objetos (POO)**, garantizando modularidad, mantenibilidad y escalabilidad.

La aplicación permite registrar, editar, activar o desactivar clientes, así como calcular automáticamente la cuota mensual en función del tipo de cliente (Regular, Premium o Corporativo). La información se almacena de manera persistente en un archivo JSON (`base_de_datos/clientes.json`), asegurando la conservación de datos entre ejecuciones.

## Ariquitectura del Sistema

- **Modelos**: Definen la estructura y comportamiento de los clientes.
- **Gestor de Clientes**: Implementa la lógica de negocio.
- **Repositorio JSON**: Gestiona la persistencia de datos.
- **Validaciones**: Controla la integridad de los datos ingresados.
- **Interfaz por Consola**: Permite la interacción mediante menú estructurado.

Esta organización favorece la claridad del código y facilita futuras extensiones.

## Estructura carpetas

- `modelos/`: clases del dominio (Cliente y subclases)
- `repositorio/`: persistencia en archivo JSON
- `gestor_clientes/`: lógica del sistema (operaciones CRUD + estado activo)
- `validaciones/`: validaciones de formato (email y celular)
- `docs/`: diagrama UML (PlantUML) y documentación teórica


## Aplicación de Programación Orientada a Objetos

El sistema implementa los principales caracteristicas de la POO:

### Abstracción
Se define una clase abstracta `Cliente` que establece la estructura común y obliga a implementar el cálculo de descuento en cada tipo específico.

### Herencia
Las clases `ClienteRegular`, `ClientePremium` y `ClienteCorporativo` heredan de `Cliente`, reutilizando atributos comunes y especializando el comportamiento de descuento.

En el caso de `ClienteCorporativo`, se utiliza el método `super()` para reutilizar el constructor de la clase padre y evitar duplicación de código. De esta manera, los atributos comunes se inicializan desde la clase `Cliente`, y luego se agrega el atributo adicional `empresa`, propio del cliente corporativo.

### Polimorfismo
El método `calcular_cuota_mensual()` se ejecuta de manera uniforme para todos los clientes, aplicando automáticamente el descuento correspondiente según el tipo del objeto.

### Encapsulamiento
La manipulación de datos se realiza exclusivamente a través del `GestorClientes`, evitando acceso directo no controlado a la estructura interna de los objetos.

## Funcionalidades

El sistema permite:

1. **Listar clientes**
   - Listar clientes **activos**
   - Listar clientes **inactivos**

2. **Activar / Desactivar clientes**
   - Cambia el estado del cliente usando el atributo `activo` (baja lógica, sin borrar datos)

3. **Agregar cliente**
   - Tipos disponibles: **regular**, **premium**, **corporativo**
   - Validación de **correo electrónico** (formato válido)
   - Validación de **celular formato utilizado en Chile** (formato: `9XXXXXXXX`)
   - Validación de **ID único** (no permite IDs repetidos)

4. **Editar cliente**
   - Permite modificar **nombre, email y celular**
   - Si se intenta ingresar un email o celular inválido, el sistema solicita reintentar.

5. **Calcular cuota mensual**
   - Solicita un **monto base**
   - Calcula la cuota final aplicando descuento según el tipo de cliente:
     - Regular: 5%
     - Premium: 10%
     - Corporativo: 20%

## Cómo ejecutar

Para ejecutar el sistema existen dos opciones:

### Opción 1: Clonar el repositorio desde GitHub

1. Abrir una terminal.

2. Clonar el repositorio: 
https://github.com/coniosorior/ABP_Gestor_Inteligente_Clientes.git

3. Abrir la carpeta **Abp4** en Visual Studio Code (VS Code).

4. Ejecutar el sistema desde el archivo main.py

---

### Opción 2: Ejecutar desde archivo .zip

1. Descargar el archivo comprimido (.zip).

2. Descomprimir el archivo.

3. Abrir la carpeta **Abp4** en Visual Studio Code.

4. Ejecutar: main.py

El sistema mostrará un menú interactivo en la consola para gestionar los clientes.



