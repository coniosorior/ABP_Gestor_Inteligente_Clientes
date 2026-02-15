from modelos.clientes import ClienteRegular, ClientePremium, ClienteCorporativo
from repositorio.clientes_repo import ClientesRepositorioJSON
from gestor_clientes.gestor_clientes import GestorClientes
from validaciones.validaciones import email_es_valido, telefono_chile_es_valido


def pedir_int(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print("Debes ingresar un número entero.")


def pedir_texto(mensaje: str, obligatorio: bool = True):
    val = input(mensaje).strip()
    if not val and not obligatorio:
        return None
    if not val and obligatorio:
        print("No puede estar vacío.")
        return pedir_texto(mensaje, obligatorio=obligatorio)
    return val


def pedir_email(mensaje: str) -> str:
    while True:
        email = pedir_texto(mensaje, obligatorio=True)
        if email_es_valido(email):
            return email
        print("Correo no válido. Ejemplo: nombre@correo.com / nombre@correo.cl")


def pedir_telefono_chile(mensaje: str) -> str:
    while True:
        telefono = pedir_texto(mensaje, obligatorio=True)
        if telefono_chile_es_valido(telefono):
            return telefono.strip().replace(" ", "")
        print("Teléfono inválido. Formato Chile: 9XXXXXXXX (9 dígitos, comienza con 9).")


def pedir_cliente_id_disponible(gestor: GestorClientes) -> int:
    while True:
        cid = pedir_int("cliente_id (número): ")
        if gestor.buscar_por_id(cid) is None:
            return cid
        print("ID ocupado. Agrega uno diferente.")


def mostrar_lista(clientes, titulo: str):
    print(f"\n{titulo}")
    if not clientes:
        print("No hay ningún cliente en la lista.")
        return
    for c in clientes:
        print(" -", c)


def listar_activos(gestor: GestorClientes):
    clientes = gestor.listar(solo_activos=True)
    mostrar_lista(clientes, "Clientes Activos")


def listar_inactivos(gestor: GestorClientes):
    clientes = [c for c in gestor.listar() if not c.activo]
    mostrar_lista(clientes, "Clientes Inactivos")


def submenu_listar_clientes(gestor: GestorClientes):
    while True:
        print("\nListar clientes")
        print("1) Clientes Activos")
        print("2) Clientes Inactivos")
        print("3) Volver")
        op = input("Elige una opción: ").strip()

        if op == "1":
            listar_activos(gestor)
        elif op == "2":
            listar_inactivos(gestor)
        elif op == "3":
            break
        else:
            print("Opción inválida.")


def accion_agregar_cliente(gestor: GestorClientes):
    print("\nCompletar los campos solicitados:")

    tipo = input("Tipo (regular/premium/corporativo): ").strip().lower()
    if tipo not in ("regular", "premium", "corporativo"):
        print("Tipo inválido.")
        return

    cliente_id = pedir_cliente_id_disponible(gestor)
    nombre = pedir_texto("Nombre: ")
    email = pedir_email("Email: ")
    telefono = pedir_telefono_chile("Celular (ejemplo: 912345678): ")

    activo = True

    if tipo == "regular":
        cliente = ClienteRegular(
            cliente_id=cliente_id, nombre=nombre, email=email, telefono=telefono, activo=activo
        )
    elif tipo == "premium":
        cliente = ClientePremium(
            cliente_id=cliente_id, nombre=nombre, email=email, telefono=telefono, activo=activo
        )
    else:
        empresa = pedir_texto("Empresa: ")
        cliente = ClienteCorporativo(
            cliente_id=cliente_id, nombre=nombre, email=email, telefono=telefono, activo=activo, empresa=empresa
        )

    gestor.agregar(cliente)
    print("\nCliente agregado:")
    print(" -", cliente)


def accion_editar_cliente(gestor: GestorClientes):
    mostrar_lista(gestor.listar(), "Lista de clientes (para editar)")

    cid = pedir_int("\nIngresa el cliente_id a editar: ")
    cliente = gestor.buscar_por_id(cid)
    if cliente is None:
        print("No existe ese cliente.")
        return

    print("\nEditar cliente (Enter para dejar igual):")

    nombre = pedir_texto("Nuevo nombre: ", obligatorio=False)

    email = None
    while True:
        intento = pedir_texto("Nuevo email: ", obligatorio=False)
        if intento is None:
            break
        if email_es_valido(intento):
            email = intento
            break
        print("Formato de correo invalido. Por favor, inténtelo otra vez.")

    telefono = None
    while True:
        intento = pedir_texto("Nuevo celular (Chile): ", obligatorio=False)
        if intento is None:
            break
        if telefono_chile_es_valido(intento):
            telefono = intento.strip().replace(" ", "")
            break
        print("Formato de número invalido. Por favor, ingresar correctamente (ejemplo: 9XXXXXXXX).")

    gestor.editar(cid, nombre=nombre, email=email, telefono=telefono)

    actualizado = gestor.buscar_por_id(cid)
    print("\nCliente editado exitosamente.")
    print(" -", actualizado)


def submenu_activar_desactivar(gestor: GestorClientes):
    mostrar_lista(gestor.listar(), "Lista de clientes (activar/desactivar)")

    while True:
        print("\nActivar/Desactivar cliente")
        print("1) Activar cliente")
        print("2) Desactivar cliente")
        print("3) Volver")
        op = input("Elige una opción: ").strip()

        if op == "3":
            break

        if op not in ("1", "2"):
            print("Opción inválida.")
            continue

        cid = pedir_int("Ingresa el cliente_id: ")
        cliente = gestor.buscar_por_id(cid)
        if cliente is None:
            print("No existe ese cliente.")
            continue

        if op == "1":
            if cliente.activo:
                print("El cliente se encuentra activado.")
            else:
                gestor.editar(cid, activo=True)
                print("\nCliente activado:")
                print(" -", gestor.buscar_por_id(cid))

        elif op == "2":
            if not cliente.activo:
                print("El cliente se encuentra desactivado.")
            else:
                gestor.editar(cid, activo=False)
                print("\nCliente desactivado:")
                print(" -", gestor.buscar_por_id(cid))


def accion_calcular_cuota(gestor: GestorClientes):
    cid = pedir_int("cliente_id: ")
    cliente = gestor.buscar_por_id(cid)
    if cliente is None:
        print("No existe ese cliente.")
        return

    tarifa = pedir_int("Monto / tarifa base (CLP): ")
    cuota = cliente.calcular_cuota_mensual(tarifa)

    # MODIFICACIÓN: usar __str__ para mantener formato uniforme
    print(f"{cliente} | Cuota mensual a pagar: {cuota} CLP")


def mostrar_menu_principal():
    print("\nGESTOR DE CLIENTES (GIC)")
    print("1) Listar clientes")
    print("2) Activar/Desactivar cliente")
    print("3) Agregar cliente")
    print("4) Editar cliente")
    print("5) Calcular cuota mensual")
    print("6) Salir")


def main():
    repo = ClientesRepositorioJSON("base_de_datos/clientes.json")
    gestor = GestorClientes(repo)
    gestor.cargar_desde_archivo()

    while True:
        mostrar_menu_principal()
        opcion = input("Elige una opción: ").strip()

        try:
            if opcion == "1":
                submenu_listar_clientes(gestor)
            elif opcion == "2":
                submenu_activar_desactivar(gestor)
            elif opcion == "3":
                accion_agregar_cliente(gestor)
            elif opcion == "4":
                accion_editar_cliente(gestor)
            elif opcion == "5":
                accion_calcular_cuota(gestor)
            elif opcion == "6":
                print("Saliendo...")
                break
            else:
                print("Opción inválida.")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()

