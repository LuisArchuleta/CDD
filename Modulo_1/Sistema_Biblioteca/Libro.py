class Libro:
    """Clase Libro: Para representar los datos de un libro.
    Input: recibe el ISBN, título, autor y el número inicial de ejemplares.
    Output: Ninguno.
    Functions:
            __init__: Función de inicio. Recibe el objeto, isbn, titulo, autor y n_ejemplares.
                      Inicializa el contador de veces_prestado en 0 para despues usarlo en el top 3 de libros.
    """
    def __init__(self,isbn,titulo,autor,n_ejemplares):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.n_ejemplares = int(n_ejemplares)
        self.veces_prestado = 0
        print("\nSe ha creado el libro",self.titulo)    
    
    