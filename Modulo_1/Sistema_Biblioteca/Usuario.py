class Usuario:
    """Clase Usuario: Para representar a un miembno de la biblioteca.
    Input: recibe el id único del usuario y su nombre.
    Output:
            __str__: Una cadena con el formato "Id: [id] Nombre: [nombre]".
    Functions:
            __init__: Función de inicio. Recibe su propio objeto, el id y el nombre.
            __str__: Función para representar el objeto como una cadena. Recibe su propio objeto y devuelve una cadena con formato.
    """
    def __init__(self,id,nombre):
        self.id=id;
        self.nombre=nombre;
    
    def __str__(self):
        return f"Id: {self.id} Nombre: {self.nombre}"
