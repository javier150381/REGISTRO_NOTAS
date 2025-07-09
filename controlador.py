from typing import Any

class NotasController:
    """Coordina las operaciones entre la vista y el modelo"""

    def __init__(self, modelo: Any):
        self.modelo = modelo

    def registrar(self, nota_id: int, nombre: str, nota: float) -> str:
        self.modelo.insertar_nota(nota_id, nombre, nota)
        return f"Nota para {nombre} registrada correctamente."

    def listar(self):
        return self.modelo.obtener_notas()

    def obtener(self, nota_id: int):
        return self.modelo.obtener_nota(nota_id)

    def actualizar(self, nota_id: int, nombre: str, nota: float) -> str:
        self.modelo.actualizar_nota(nota_id, nombre, nota)
        return "Nota actualizada correctamente."

    def eliminar(self, nota_id: int) -> str:
        self.modelo.eliminar_nota(nota_id)
        return "Nota eliminada correctamente."
