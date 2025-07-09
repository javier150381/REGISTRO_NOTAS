import sqlite3

class NotasDB:
    """Maneja todas las operaciones de la base de datos SQLite"""

    def __init__(self, db_name: str = "notas.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.crear_tabla()

    def crear_tabla(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS notas (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    nota REAL NOT NULL
                )"""
        )
        self.conn.commit()

    def insertar_nota(self, nota_id: int, nombre: str, nota: float) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO notas (id, nombre, nota) VALUES (?, ?, ?)",
            (nota_id, nombre, nota),
        )
        self.conn.commit()

    def obtener_notas(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nombre, nota FROM notas")
        return cursor.fetchall()

    def obtener_nota(self, nota_id: int):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, nombre, nota FROM notas WHERE id = ?",
            (nota_id,),
        )
        return cursor.fetchone()

    def actualizar_nota(self, nota_id: int, nombre: str, nota: float) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE notas SET nombre = ?, nota = ? WHERE id = ?",
            (nombre, nota, nota_id),
        )
        self.conn.commit()

    def eliminar_nota(self, nota_id: int) -> None:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM notas WHERE id = ?", (nota_id,))
        self.conn.commit()
