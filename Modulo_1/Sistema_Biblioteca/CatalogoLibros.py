from Libro import Libro

class catalogoLibros:
    """Clase catalogoLibros: Para crear un diccionario de libros y manejar consultas de libros
    Input: recibe objetos tipo libros
    outuput: 
            top_3_libros: Diccionario con los 3 libros mas prestados
            buscar_por_autor: Una lista de libros.
    Functions:
            __init__: Funcion de inicio. Recibe su propio objeto y un diccionario.
            agregar: Funcion para agregar objetos tipo libro al diccionario. Recibe su propio objeto y un objeto tipo usuario.
            mostrarDisponibilidad: Funcion que recorre el diccionario de libros para imprimir los parametros titulo y ejemplares del objeto libro, si el diccionario esta vacio imprima no hay libros registrados. Recibe su propio objeto.
            crearLibros: Funcion para crear un objeto libro y agregarlo al diccionario. Recibe su propio objeto.
            top_3_libros: Funcion que ordena el diccionario de mayor a menor en base a la cantidad de veces que se ha prestado el libro. Recibe su propio objeto.
            buscar_por_autor: Funcion que crea una lista con los libros encontrados segun el autor dado. Recibe su propio objeto y el autor a buscar.
            buscar_por_titulo: Funcion que crea una lista con los libros encontrados segun el titulo dado. Recibe su propio objeto y el titulo a buscar.
            libros_por_autor: Funcion que pide al usuario un autor para buscar libros, llama a funcion buscar_por_autor el cual devuelve una lista, imprime la lista de libros encontrados. Recibe su propio objeto.
            libros_por_titulo: Funcion que pide al usuario un titulo para buscar libros, llama a funcion buscar_por_titulo el cual devuelve una lista, imprime la lista de libros encontrados. Recibe su propio objeto.
    """

    def __init__(self,libros = {}):
        self.libros=libros
    
    def agregar(self,l):
        self.libros[l.isbn] = l #Diccionario libros, isbn: libro {TITULO, AUTOR, N_EJEMPLARES }


    def mostrarDisponibilidad(self):
        if len(self.libros)==0:
            print("No hay libros registrados")
        else:
            for libro in self.libros.values():
                print(f"Libro: {libro.titulo:<25} | Ejemplares disponibles: {libro.n_ejemplares:<15}")
    
    def crearLibros(self):
        while True:
            isbn = input("ISBN: ")
            if isbn.isdigit():
                break
            else:
                print("El ISBN esta compuesto solo de digitos")
        titulo = input("Titulo: ")
        autor = input("Autor: ")
        while True:
            n_ejemplares = input("Numero de ejemplares: ")
            if n_ejemplares.isdigit():
                break
            else:
                print("Solo se aceptan numeros")
        libro = Libro(isbn,titulo,autor,n_ejemplares)
        self.agregar(libro)

    def top_3_libros(self):
        libros_ordenados = sorted(self.libros.values(), key=lambda x: x.veces_prestado, reverse=True) #Ordena el diccionario de mayor a menor segun la cantidad de prestamos
        return libros_ordenados[:3] #Devuelve los primeros 3 
    
    def buscar_por_autor(self, autor):
        encontrados = [] #Lista con los libros encontrados
        for l in self.libros.values(): #Recorre el diccionario de libros
            if l.autor.lower() == autor.lower(): #Si el autor dado coincide con el parametro autor del libro
                encontrados.append(l) #Se agrega a la lista de encontrados
        return encontrados 
    
    def buscar_por_titulo(self, titulo):
        encontrados = [] 
        for l in self.libros.values():
            if l.titulo.lower() == titulo.lower(): #Si el titulo dado coincide con el parametro titudlo del libro
                encontrados.append(l)
        return encontrados

    def libros_por_autor(self):
        autor = input("\nEscriba el nombre del autor: ")
        resultados = self.buscar_por_autor(autor)
        if resultados:
            print("")
            for l in resultados: #lista de libros encontrados
                print(f"Título: {l.titulo: <30} | ISBN: {l.isbn: <15} | Disponibles: {l.n_ejemplares}")
        else:
            print("No se encontraron libros de ese autor.")

    def libros_por_titulo(self):
        titulo = input("\nEscriba el titulo del libro: ")
        resultados = self.buscar_por_titulo(titulo)
        if resultados:
            print("")
            for l in resultados:
                print(f"Título: {l.titulo: <30} | ISBN: {l.isbn: <15} | Disponibles: {l.n_ejemplares}")
        else:
            print("No se encontro el libro.")
