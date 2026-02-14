import json
import os
from typing import List

from modelos.clientes import Cliente, ClienteRegular, ClientePremium, ClienteCorporativo


class ClientesRepositorioJSON:
    def __init__(self, ruta_archivo: str = "base_datos/clientes.json"):
        # OJO: aquí puse base_datos porque es como lo tienes en tu carpeta
        self.ruta_archivo = ruta_archivo

    def _asegurar_directorio(self) -> None:
        """
        Si la carpeta donde va el JSON no existe, la crea.
        Ej: si ruta_archivo = 'base_datos/clientes.json',
        crea la carpeta 'base_datos' si no existe.
        """
        carpeta = os.path.dirname(self.ruta_archivo)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)

    def guardar(self, clientes: List[Cliente]) -> None:
        data = [c.a_dict() for c in clientes]

        # 1) aseguramos que exista la carpeta
        self._asegurar_directorio()

        # 2) guardamos el archivo
        try:
            with open(self.ruta_archivo, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            raise OSError(f"No se pudo guardar el archivo JSON: {e}") from e

    def cargar(self) -> List[Cliente]:
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            raise ValueError("El archivo JSON está dañado o tiene un formato inválido.")
        except OSError as e:
            raise OSError(f"No se pudo leer el archivo JSON: {e}") from e

        clientes: List[Cliente] = []
        for d in data:
            clientes.append(self._cliente_desde_dict(d))
        return clientes

    def _cliente_desde_dict(self, d: dict) -> Cliente:
        tipo = d.get("tipo")

        if tipo == "regular":
            return ClienteRegular(**d)
        if tipo == "premium":
            return ClientePremium(**d)
        if tipo == "corporativo":
            return ClienteCorporativo(**d)

        raise ValueError(f"Tipo de cliente desconocido en JSON: {tipo}")

