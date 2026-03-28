class catalogoUsuarios:
    """Clase catalogoUsuarios: Para crear un diccionario de Usuarios
    Input: recibe id inicial y un diccionario.
    outuput:
            __len__: numero de elementos del diccionario
    Functions:
            __init__: Funcion de inicio. recibe su propio objeto, id inicial y un diccionario.
            agregar: Funcion para agregar objetos tipo usuario al diccionario, recibe su propio objeto y un objeto tipo usuario.
            __len__: Funcion que devuelve el numero de elementos del diccionario, recibe su propio objeto.
            mostrarUsuarios: Funcion que recorre el diccionario para imprimir los parametros id y nombre del objeto usuario, recibe su propio objeto.
    """
    
    def __init__(self,id,usuarios = {}):
        self.id = id
        self.usuarios = usuarios
    
    def agregar(self,u):
        self.usuarios[self.id]=u #Diccionario usuarios, id: usuario
        self.id+=1
        
    def __len__(self):
        return len(self.usuarios)
    
    def mostrarUsuarios(self):
        for usuario in self.usuarios.values():
            print(f"Id: {usuario.id:<15} | Nombre: {usuario.nombre:<20}")
