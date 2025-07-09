import sqlite3
import gradio as gr

# Aplicación sencilla para gestionar notas de estudiantes usando SQLite y Gradio

# Modelo
class NotasDB:
    """Maneja todas las operaciones de la base de datos"""

    def __init__(self, db_name="notas.db"):
        # Permite que la conexión sea usada desde los hilos de trabajo de Gradio
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.crear_tabla()

    def crear_tabla(self):
        """Crea la tabla inicial si no existe"""
        cursor = self.conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS notas (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    nota REAL NOT NULL
                )"""
        )
        self.conn.commit()

    def insertar_nota(self, nota_id, nombre, nota):
        """Inserta una nota nueva en la base de datos"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO notas (id, nombre, nota) VALUES (?, ?, ?)",
            (nota_id, nombre, nota),
        )
        self.conn.commit()

    def obtener_notas(self):
        """Devuelve todas las notas almacenadas"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nombre, nota FROM notas")
        return cursor.fetchall()

    def obtener_nota(self, nota_id):
        """Devuelve una nota concreta por id o None si no existe"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, nombre, nota FROM notas WHERE id = ?",
            (nota_id,),
        )
        return cursor.fetchone()

    def actualizar_nota(self, nota_id, nombre, nota):
        """Actualiza una nota existente"""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE notas SET nombre = ?, nota = ? WHERE id = ?",
            (nombre, nota, nota_id),
        )
        self.conn.commit()

    def eliminar_nota(self, nota_id):
        """Elimina una nota por id"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM notas WHERE id = ?", (nota_id,))
        self.conn.commit()


# Controlador
class NotasController:
    """Coordina las operaciones entre la vista y el modelo"""

    def __init__(self, modelo: NotasDB):
        self.modelo = modelo

    def registrar(self, nota_id: int, nombre: str, nota: float) -> str:
        """Registra una nueva nota"""
        self.modelo.insertar_nota(nota_id, nombre, nota)
        return f"Nota para {nombre} registrada correctamente."

    def listar(self):
        """Lista todas las notas"""
        return self.modelo.obtener_notas()

    def obtener(self, nota_id: int):
        """Obtiene una nota individual por id"""
        return self.modelo.obtener_nota(nota_id)

    def actualizar(self, nota_id: int, nombre: str, nota: float) -> str:
        """Actualiza una nota existente"""
        self.modelo.actualizar_nota(nota_id, nombre, nota)
        return "Nota actualizada correctamente."

    def eliminar(self, nota_id: int) -> str:
        """Elimina una nota por id"""
        self.modelo.eliminar_nota(nota_id)
        return "Nota eliminada correctamente."


# Vista
class NotasView:
    """Define la interfaz de usuario con Gradio"""

    def __init__(self, controlador: NotasController):
        self.controlador = controlador

    def interfaz(self):
        """Construye y devuelve la interfaz de Gradio"""
        with gr.Blocks() as demo:
            gr.Markdown("## Gestión de Notas de Estudiantes")
            with gr.Tabs():
                with gr.Tab("Crear"):
                    nota_id_c = gr.Number(label="ID del Estudiante", precision=0)
                    nombre = gr.Textbox(label="Nombre del Estudiante")
                    nota = gr.Number(label="Nota Final")
                    salida = gr.Textbox(label="Mensaje", interactive=False)

                    def manejar(nota_id_c, nombre, nota):
                        return self.controlador.registrar(int(nota_id_c), nombre, nota)

                    boton = gr.Button("Guardar Nota")
                    boton.click(manejar, inputs=[nota_id_c, nombre, nota], outputs=salida)

                with gr.Tab("Leer"):
                    tabla = gr.Dataframe(
                        headers=["ID", "Nombre", "Nota"],
                        interactive=False,
                    )

                    def cargar():
                        return self.controlador.listar()

                    boton_cargar = gr.Button("Cargar Notas")
                    boton_cargar.click(cargar, outputs=tabla)

                with gr.Tab("Actualizar"):
                    with gr.Row():
                        nota_id = gr.Number(label="ID", precision=0)
                        boton_buscar = gr.Button("Buscar")

                    nombre_u = gr.Textbox(label="Nombre")
                    nota_u = gr.Number(label="Nota")
                    salida_u = gr.Textbox(label="Mensaje", interactive=False)

                    def buscar_datos(nota_id):
                        datos = self.controlador.obtener(int(nota_id))
                        if datos:
                            _, nombre, nota = datos
                            return nombre, nota, ""
                        return "", None, "ID no encontrado"

                    boton_buscar.click(
                        buscar_datos,
                        inputs=nota_id,
                        outputs=[nombre_u, nota_u, salida_u],
                    )

                    def manejar_actualizar(nota_id, nombre_u, nota_u):
                        return self.controlador.actualizar(int(nota_id), nombre_u, nota_u)

                    boton_u = gr.Button("Actualizar Nota")
                    boton_u.click(
                        manejar_actualizar,
                        inputs=[nota_id, nombre_u, nota_u],
                        outputs=salida_u,
                    )

                with gr.Tab("Eliminar"):
                    nota_id_e = gr.Number(label="ID", precision=0)
                    salida_e = gr.Textbox(label="Mensaje", interactive=False)

                    def manejar_eliminar(nota_id_e):
                        return self.controlador.eliminar(int(nota_id_e))

                    boton_e = gr.Button("Eliminar Nota")
                    boton_e.click(manejar_eliminar, inputs=nota_id_e, outputs=salida_e)
        return demo


if __name__ == "__main__":
    # Punto de entrada de la aplicación
    modelo = NotasDB()
    controlador = NotasController(modelo)
    vista = NotasView(controlador)
    app = vista.interfaz()
    app.launch()
