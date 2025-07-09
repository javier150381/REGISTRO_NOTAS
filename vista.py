import gradio as gr
from controlador import NotasController

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
