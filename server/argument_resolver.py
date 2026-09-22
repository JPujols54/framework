import inspect
from typing import get_type_hints, Any
from .request import HTTPRequest

class ConversorTipo:
    """Clase base / interfaz para castear valores de cadena a tipos nativos."""
    def convertir(self, val: Any) -> Any:
        raise NotImplementedError

class ConversorBooleano(ConversorTipo):
    def convertir(self, val: Any) -> bool:
        if isinstance(val, str):
            return val.lower() in ("true", "1", "yes", "on")
        return bool(val)

class ConversorLista(ConversorTipo):
    def convertir(self, val: Any) -> list:
        return val if isinstance(val, list) else [val]

class ConversorGenerico(ConversorTipo):
    def __init__(self, target_type: type):
        self.target_type = target_type

    def convertir(self, val: Any) -> Any:
        try:
            return self.target_type(val)
        except (ValueError, TypeError):
            return val

class ArgumentResolver:
    """Extrae, combina y convierte argumentos de Path + Query según la firma del Handler."""

    _CONVERSORES_ESPECIALES = {
        bool: ConversorBooleano(),
        list: ConversorLista(),
    }

    @classmethod
    def _castear_valor(cls, val: Any, expected_type: type) -> Any:
        if expected_type is inspect.Parameter.empty or expected_type == str:
            return val

        conversor = cls._CONVERSORES_ESPECIALES.get(
            expected_type, ConversorGenerico(expected_type)
        )
        return conversor.convertir(val)

    @classmethod
    def resolve_kwargs(cls, handler, req: HTTPRequest) -> dict:
        """
        Extrae path_params y query_params del request, los cruza con la firma
        del handler y los convierte según los Type Hints.
        """
        path_params = getattr(req, "params", {}) or {}
        query_params = getattr(req, "query_params", {}) or {}

        combined_args = {**query_params, **path_params}

        sig = inspect.signature(handler)
        type_hints = get_type_hints(handler)

        valid_kwargs = {}
        has_kwargs = any(
            p.kind == inspect.Parameter.VAR_KEYWORD
            for p in sig.parameters.values()
        )

        for key, val in combined_args.items():
            if key in sig.parameters or has_kwargs:
                expected_type = type_hints.get(key, str)

                # Si el Query String devolvió una lista pero la función espera un tipo escalar (int, str, bool)
                if isinstance(val, list) and expected_type not in (list, inspect.Parameter.empty):
                    val = val[0]

                valid_kwargs[key] = cls._castear_valor(val, expected_type)

        return valid_kwargs