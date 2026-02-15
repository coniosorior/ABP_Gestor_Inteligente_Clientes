from abc import ABC, abstractmethod


class Cliente(ABC):

    campos = ["cliente_id", "nombre", "email", "telefono", "activo"]

    def __init__(self, **kwargs):
        for c in self.campos:
            setattr(self, c, kwargs.get(c))

        if self.activo is None:
            self.activo = True

    @property
    @abstractmethod
    def tipo(self) -> str:
        pass

    @abstractmethod
    def calcular_descuento(self, tarifa_base: int) -> int:
        pass

    def calcular_cuota_mensual(self, tarifa_base: int) -> int:
        return tarifa_base - self.calcular_descuento(tarifa_base)

    def a_dict(self) -> dict:
        data = {
            "cliente_id": self.cliente_id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "activo": self.activo,
            "tipo": self.tipo
        }

        if hasattr(self, "empresa"):
            data["empresa"] = self.empresa

        return data


    def __str__(self) -> str:
        estado = "Activo" if self.activo else "Inactivo"

        texto = (
            f"[{self.tipo.upper()}] "
            f"ID: {self.cliente_id} | "
            f"{self.nombre}"
        )

        if self.tipo == "corporativo":
            empresa_val = getattr(self, "empresa", None) or self.nombre
            texto += f" | Empresa: {empresa_val}"

        texto += (
            f" | {self.email}"
            f" | {self.telefono}"
            f" | {estado}"
        )

        return texto


class ClienteRegular(Cliente):

    @property
    def tipo(self) -> str:
        return "regular"

    def calcular_descuento(self, tarifa_base: int) -> int:
        return (tarifa_base * 5) // 100


class ClientePremium(Cliente):

    @property
    def tipo(self) -> str:
        return "premium"

    def calcular_descuento(self, tarifa_base: int) -> int:
        return (tarifa_base * 10) // 100


class ClienteCorporativo(Cliente):

    campos = Cliente.campos + ["empresa"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.empresa = kwargs.get("empresa")

    @property
    def tipo(self) -> str:
        return "corporativo"

    def calcular_descuento(self, tarifa_base: int) -> int:
        return (tarifa_base * 20) // 100
