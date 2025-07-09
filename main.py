import sqlite3
import gradio as gr

# Modelo
class NotasDB:
    def __init__(self, db_name="notas.db"):
        self.conn = sqlite3.connect(db_name)
        self.crear_tabla()

    def crear_tabla(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS notas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    nota REAL NOT NULL
                )"""
        )
        self.conn.commit()

    def insertar_nota(self, nombre, nota):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO notas (nombre, nota) VALUES (?, ?)", (nombre, nota))
        self.conn.commit()


# Controlador
class NotasController:
    def __init__(self, modelo: NotasDB):
        self.modelo = modelo

    def registrar(self, nombre: str, nota: float) -> str:
        self.modelo.insertar_nota(nombre, nota)
        return f"Nota para {nombre} registrada correctamente."


# Vista
class NotasView:
    def __init__(self, controlador: NotasController):
        self.controlador = controlador

    def interfaz(self):
        with gr.Blocks() as demo:
            nombre = gr.Textbox(label="Nombre del Estudiante")
            nota = gr.Number(label="Nota Final")
            salida = gr.Textbox(label="Mensaje", interactive=False)

            def manejar(nombre, nota):
                return self.controlador.registrar(nombre, nota)

            boton = gr.Button("Guardar Nota")
            boton.click(manejar, inputs=[nombre, nota], outputs=salida)
        return demo


if __name__ == "__main__":
    modelo = NotasDB()
    controlador = NotasController(modelo)
    vista = NotasView(controlador)
    app = vista.interfaz()
    app.launch()
