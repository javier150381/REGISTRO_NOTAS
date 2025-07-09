from pymongo import MongoClient

class NotasMongo:
    """Modelo que almacena las notas en MongoDB"""

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["registro_notas"]
        self.collection = self.db["notas"]

    def insertar_nota(self, nota_id, nombre, nota):
        self.collection.insert_one({
            "id": nota_id,
            "nombre": nombre,
            "nota": nota
        })

    def obtener_notas(self):
        return [
            (doc["id"], doc["nombre"], doc["nota"]) for doc in self.collection.find()
        ]

    def obtener_nota(self, nota_id):
        doc = self.collection.find_one({"id": nota_id})
        return (doc["id"], doc["nombre"], doc["nota"]) if doc else None

    def actualizar_nota(self, nota_id, nombre, nota):
        self.collection.update_one(
            {"id": nota_id},
            {"$set": {"nombre": nombre, "nota": nota}}
        )

    def eliminar_nota(self, nota_id):
        self.collection.delete_one({"id": nota_id})
