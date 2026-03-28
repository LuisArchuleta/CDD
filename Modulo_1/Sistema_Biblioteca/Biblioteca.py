from CatalogoLibros import catalogoLibros 
from Libro import Libro
from Usuario import Usuario
from CatalogoUsuarios import catalogoUsuarios
from GestionPrestamos import GestionPrestamos
"""Biblioteca: Manejo de la biblioteca, menus y funciones para la gestion de libros y usuarios.
    Input: 
            libros: Diccionario que se mandara como parametro para la creacion del catalogo.
            catalogolibros: Objeto de la clase catalogoLibros, envia diccionario libros.
            usuarios: Diccionario que se mandara como parametro para la creacion del catalogo.
            catalogousuarios: Objeto de la clase catalogoUsuarios, envia diccionario libros.
    Functions:
            menu_principal: Funcion que muestra el menu principal de la libreria, llama a los metodos menuLibros, 
            menuUsuarios, menuPrestamosyDevoluciones, menuReportesyConsultas segun la opcion dada por el usuario.

            menuLibros: Funcion que muestra el menu para la gestion de libros llama a la funcion crearLibros, 
            mostrarDisponibilidad y menuBuscar segun la opcion dada por el usuario.

            menuBuscar: Funcion que muestra el menu para buscar por titulo o autor del libro, llama a la funcion libros_por_titulo
            y libros_por_autor segun la opcion del usuario.

            menuUsuarios: Funcion que muestra el menu para el manejo de usuarios, llama a la funcion registrarUsuario y mostrarUsuarios
            segun la opcion del usuario.

            registrarUsuario: Funcion que  hace la creacion del objeto usuario con el parametro nombre y lo agrega al catalogoUsuarios.

            menuPrestamosyDevoluciones: Funcion que muestra el menu para la gestion de prestamos y devoluciones, llama a la funcion 
            realizar_prstamo y devolver segun la opcion dada por el usuario.

            realizar_prestamo: Funcion para realizar el prestamo del libro, llama a la funcion realizar_prestamo
            mandando el isbn e id_usuario para hacer el prestamo. Imprime el resultado del prestamo (Exito o fallido)

            devolver: Funcion para hacer la devolucion de un libro, llama a la funcion devolver de gestionPrestamos mandndo el isbn y el id del usuario.
            Imprime el resultado (Exitoso o error)

            menuReportesyConsultas: Funcion que muestra el menu para la gestion de reportes y consultas, llama a la funcion top_3_libros, mostrar_prestamos_activos
            y libros_por_autor segun la opcion dada por el usuario.

            __name__:Llama la funcion principal: menu_principal.
    """
libros={}
catalogolibros=catalogoLibros(libros)

usuarios={}
catalogousuarios=catalogoUsuarios(1,usuarios)

gestionPrestamos = GestionPrestamos()

def menu_principal():
    while True:
        print("""
    SISTEMA BIBLIOTECARIO
----------------------------
1.-Alta y gestion de libros
2.-Registro de usuarios
3.-Prestamos y devoluciones
4.-Reportes y consultas
5.-Salir del programa
----------------------------
    """)
        
        opcion=int(input("Opcion: "))
        match opcion:
            case 1:
                menuLibros()
            case 2:
                menuUsuarios()
            case 3:
                menuPrestamosyDevoluciones()
            case 4: 
                menuReportesyConsultas()
            case 5:
                print("\nSaliste del programa\n")
                break
            case _:
                print("Opcion no valida")
                
def menuLibros():
    while True:
        print("""
Alta y gestion de libros
----------------------------
1.-Registrar libro
2.-Consultar disponibilidad
3.-Buscar libro
4.-Volver
----------------------------
        """)
        opcion=int(input("Opcion: "))
        match opcion:
            case 1:
                print("")
                catalogoLibros.crearLibros(catalogolibros)
            case 2:
                print("")
                catalogoLibros.mostrarDisponibilidad(catalogolibros)
            case 3:
                menuBuscar()
            case 4:
                break
            case _:
                print("Opcion no valida")
            

def menuBuscar():
    while True:
        print("""
Buscar libro
----------------------------
1.-Por titulo
2.-Por autor
3.-Volver
----------------------------
    """)
        opcion=int(input("Opcion: "))
        match opcion:
            case 1:
                catalogoLibros.libros_por_titulo(catalogolibros)
            case 2:
                catalogoLibros.libros_por_autor(catalogolibros)
            case 3:
                break
            case _:
                print("Opcion no valida")
            

def menuUsuarios():
    while True:
        print("""
Alta y gestion de usuarios
----------------------------
1.-Registrar usuario
2.-Consultar usuarios
3.-Volver
----------------------------
        """)
        opcion=int(input("Opcion: "))
        match opcion:
            case 1:
                registrarUsuario()
            case 2:
                print("")
                catalogoUsuarios.mostrarUsuarios(catalogousuarios)
            case 3:
                break
            case _:
                print("Opcion no valida")

def registrarUsuario():
  nombre = input("\nNombre: ")
  usuario = Usuario(catalogousuarios.id,nombre) #Se crea el objeto usuario, se manda el id actual en el que va el catalogoUsuarios y el nombre dado.
  catalogousuarios.agregar(usuario) 

def menuPrestamosyDevoluciones():
     while True:
        print("""
Prestamos y Devoluciones
----------------------------
1.-Realizar prestamo
2.-Realizar devolucion
3.-Volver
----------------------------
        """)
        opcion=int(input("Opcion: "))
        match opcion:
            case 1:
                realizar_prestamo()
            case 2:
                devolver()
            case 3:
                break
            case _:
                print("Opcion no valida")

def realizar_prestamo():
    print("\n--- Realizar Préstamo ---")
    while True:
        isbn = input("Ingrese el ISBN del libro: ")
        if isbn.isdigit():
            break
        else: print("El ISBN esta compuesto solo de digitos")
    while True:
        id_usuario = input("Ingrese el ID del usuario: ")    
        if id_usuario.isdigit():
            id_usuario = int(id_usuario)
            break
        else: print("El id solo admite digitos")
    resultado = gestionPrestamos.realizar_prestamo(isbn, id_usuario, catalogolibros, catalogousuarios)
    print(f"\n{resultado}")

def devolver():
    print("\n--- Realizar Devolución ---")
    isbn = input("Ingrese el ISBN del libro: ")
    id_usuario = input("Ingrese el ID del usuario: ")

    if id_usuario.isdigit():
        id_usuario = int(id_usuario)
        resultado = gestionPrestamos.devolver(isbn, id_usuario, catalogolibros)
        print(f"\n{resultado}")
    else:
        print("\nError: ID de usuario no válido.")

def menuReportesyConsultas():
     while True:
        print("""
Reportes y Consultas
----------------------------
1.-Top 3 de libros más prestados
2.-Listado de prestamos activos
3.-Consultas de libros por autor
4.-Volver
----------------------------
        """)
        opcion=int(input("Opcion: "))
        match opcion:
            case 1:
                tops = catalogoLibros.top_3_libros(catalogolibros)
                for i, libro in enumerate(tops, 1):
                   print(f"{i}. {libro.titulo} ({libro.veces_prestado} veces)")
            case 2:
                gestionPrestamos.mostrar_prestamos_activos()
            case 3: 
                catalogoLibros.libros_por_autor(catalogolibros)
            case 4:
                break
            case _:
                print("Opcion no valida")



if __name__ == "__main__":
    menu_principal()