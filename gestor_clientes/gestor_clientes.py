from typing import List, Optional
from modelos.clientes import Cliente
from repositorio.clientes_repo import ClientesRepositorioJSON


class GestorClientes:

    def __init__(self, repositorio: ClientesRepositorioJSON):
        self.repositorio = repositorio
        self.clientes: List[Cliente] = []

    def cargar_desde_archivo(self) -> None:
        self.clientes = self.repositorio.cargar()

    def guardar_en_archivo(self) -> None:
        self.repositorio.guardar(self.clientes)

    def agregar(self, cliente: Cliente) -> None:
        if self.buscar_por_id(cliente.cliente_id) is not None:
            raise ValueError(f"Ya existe un cliente con id={cliente.cliente_id}")
        self.clientes.append(cliente)
        self.guardar_en_archivo()

    def listar(self, solo_activos: bool = False) -> List[Cliente]:
        if not solo_activos:
            return list(self.clientes)
        return [c for c in self.clientes if c.activo]

    def buscar_por_id(self, cliente_id: int) -> Optional[Cliente]:
        for c in self.clientes:
            if c.cliente_id == cliente_id:
                return c
        return None

    def editar(
        self,
        cliente_id: int,
        nombre: Optional[str] = None,
        email: Optional[str] = None,
        telefono: Optional[str] = None,
        activo: Optional[bool] = None,
    ) -> None:
        cliente = self.buscar_por_id(cliente_id)
        if cliente is None:
            raise ValueError(f"No existe cliente con id={cliente_id}")

        if nombre is not None:
            cliente.nombre = nombre
        if email is not None:
            cliente.email = email
        if telefono is not None:
            cliente.telefono = telefono
        if activo is not None:
            cliente.activo = activo

        self.guardar_en_archivo()

    def eliminar(self, cliente_id: int) -> None:
        cliente = self.buscar_por_id(cliente_id)
        if cliente is None:
            raise ValueError(f"No existe cliente con id={cliente_id}")

        cliente.activo = False
        self.guardar_en_archivo()
