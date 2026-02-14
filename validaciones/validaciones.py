import re


def email_es_valido(email: str) -> bool:
    patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(patron, email) is not None


def telefono_chile_es_valido(telefono: str) -> bool:
    t = telefono.strip().replace(" ", "")
    return t.isdigit() and len(t) == 9 and t.startswith("9")
