import datetime

class GestionPrestamos:
    """Clase GestionPrestamos: Para administrar el proceso de los préstamos de libros.
    Input: recibe una lista de préstamos.
    Output:
            realizar_prestamo: mensaje de éxito o error.
            devolver: mensaje de confirmación o error.
    Functions:
            __init__: Función de inicio. Recibe su propio objeto y una lista de préstamos. Si no recibe lista, inicializa una vacía.
            realizar_prestamo: Función para registrar un nuevo préstamo. Recibe el objeto, ISBN del libro, 
                               ID del usuario y los objetos de catálogo de libros y usuarios. 
                               Valida existencia, disponibilidad, límite de 3 libros y duplicados.
            devolver: Función para registrar la devolución de un libro. Recibe el objeto, ISBN, ID de usuario 
                      y el catálogo de libros. Elimina el registro de la lista y restaura el stock.
            mostrar_prestamos_activos: Función que recorre la lista de tuplas para imprimir el ISBN, ID de usuario 
                                       y fecha del préstamo.
    """

    def __init__(self, prestamos = None):
        # Si no se proporciona una lista al crear la clase, se inicializa vacía.
        # Para evitar errores al intentar iterar.
        if prestamos is None:
            self.prestamos = []
        else:
            self.prestamos = prestamos

    def realizar_prestamo(self, isbn, id_usuario, catalogo_l, catalogo_u):
        # Se buscan los objetos en los diccionarios de los catalogos.
        libro = catalogo_l.libros.get(isbn)
        usuario = catalogo_u.usuarios.get(id_usuario)

        # Validar que tanto el libro como el usuario existan en el sistema.
        if not libro or not usuario:
            return "Error: Datos no encontrados."
        
        # Validar que el libro tenga unidades en stock.
        if int(libro.n_ejemplares) <= 0:
            return "No hay ejemplares disponibles."

        # Contar préstamos actuales del usuario
        # Se usa el '_' para ignorar el ISBN y la Fecha, ya que solo necesitamos el ID.
        prestamos_del_usuario = 0
        for _, id_u_p, _ in self.prestamos:
            if id_u_p == id_usuario:
                prestamos_del_usuario += 1

        # Si el usuario ya tiene 3 libros prestados, se rechaza la operación.
        if prestamos_del_usuario >= 3:
            return f"El usuario {usuario.nombre} ya tiene el máximo de 3 libros."

        # Evitar que el usuario pida prestado dos veces el mismo libro.
        for isbn_p, id_u_p, _ in self.prestamos:
            if isbn_p == isbn and id_u_p == id_usuario:
                return "El usuariop ya cuenta con este libro en préstamo."

        # Se crea una tupla con la información.
        fecha = str(datetime.date.today())
        registro = (isbn, id_usuario, fecha)
        self.prestamos.append(registro) # Se guarda la tupla en la lista
        
        # Se actualiza los datos
        libro.n_ejemplares = int(libro.n_ejemplares) - 1
        libro.veces_prestado += 1

        return f"Se realizo el prestamo del libro {libro.titulo} a {usuario.nombre}"

    def devolver(self, isbn, id_usuario, catalogo_l):
        # enumerate nos da el índice (i) necesario para eliminar el registro con .pop()
        for i, (isbn_p, id_u_p, fecha_p) in enumerate(self.prestamos):
            # Comparamos si el ISBN y el ID coinciden con un préstamo registrado.
            if isbn_p == isbn and id_u_p == id_usuario:
                self.prestamos.pop(i)   # Se elimina el prestamo de la lista
                libro = catalogo_l.libros.get(isbn) # Se busca el libro en el catálogo para devolver la unidad al stock.
                if libro:
                    libro.n_ejemplares = int(libro.n_ejemplares) + 1
                return "Devolución exitosa."
        return "No se encontró un préstamo activo con estos datos."
    
    def mostrar_prestamos_activos(self):
        # Verificamos si la lista tiene elementos.
        if not self.prestamos:
            print("No hay préstamos activos en este momento.")
        else:
            print("\n--- Listado de Préstamos Activos ---")
            for isbn, id_u, fecha in self.prestamos:                # Se recorren cada una de las tuplas para imprimirlas
                print(f"ISBN: {isbn:<15} | Usuario ID: {id_u:<10} | Fecha: {fecha:<12}")