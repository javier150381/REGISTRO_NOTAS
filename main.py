# from modelo_sqlite import NotasDB
from modelo_mongo import NotasMongo
from controlador import NotasController
from vista import NotasView

if __name__ == "__main__":
    modelo = NotasMongo()  # en lugar de NotasDB()
    controlador = NotasController(modelo)
    vista = NotasView(controlador)
    app = vista.interfaz()
    app.launch()
