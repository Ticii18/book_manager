import sys

class ConsoleUI:
    """
    Clase principal que maneja la interfaz de consola del sistema.
    Recibe un diccionario con todos los servicios ya instanciados.
    """
    def __init__(self, servicios: dict) -> None:
        self.servicios = servicios

    def iniciar(self):
        """menú principal de la aplicación."""
        while True:
            print("\n" + "=" * 40)
            print("BOOK MANAGER")
            print("=" * 40)
            print("1. Gestionar Libros")
            print("2. Gestionar Géneros")
            print("3. Gestionar Editoriales")
            print("4. Gestionar Monedas")
            print("5. Gestionar Tipos de Cotización")
            print("6. Gestionar Cotización del Dólar")
            print("7. Gestionar Precios")
            print("8. Gestionar Stock")
            print("0. Salir")
            print("=" * 40)

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.menu_libros()
            elif opcion == '2':
                self.menu_generos()
            elif opcion == '3':
                self.menu_editoriales()
            elif opcion == '4':
                self.menu_monedas()
            elif opcion == '5':
                self.menu_tipos_cotizacion()
            elif opcion == '6':
                self.menu_cotizaciones()
            elif opcion == '7':
                self.menu_precios()
            elif opcion == '8':
                self.menu_stocks()
            elif opcion == '0':
                print("\n¡Gracias por usar Book Manager!")
                break
            else:
                print("\nOpción inválida. Intente de nuevo.")

    # MENÚS ESPECÍFICOS

    def menu_libros(self):
        while True:
            print("\n--- GESTIÓN DE LIBROS ---")
            print("1. Listar todos los libros")
            print("2. Agregar un nuevo libro")
            print("3. Modificar un libro")
            print("4. Eliminar un libro")
            print("0. Volver al menú principal")
            
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.listar_libros()
            elif opcion == '2':
                self.crear_libro()
            elif opcion == '3':
                self.modificar_libro()
            elif opcion == '4':
                self.eliminar_libro()
            elif opcion == '0':
                break
            else:
                print("\nOpción inválida.")

    def menu_generos(self):
        while True:
            print("\n--- GESTIÓN DE GÉNEROS ---")
            print("1. Listar todos los géneros")
            print("2. Agregar un nuevo género")
            print("3. Modificar un género")
            print("4. Eliminar un género")
            print("0. Volver al menú principal")
            
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.listar_generos()
            elif opcion == '2':
                self.crear_genero()
            elif opcion == '3':
                self.modificar_genero()
            elif opcion == '4':
                self.eliminar_genero()
            elif opcion == '0':
                break
            else:
                print("\nOpción inválida.")

    def menu_editoriales(self):
        while True:
            print("\n--- GESTIÓN DE EDITORIALES ---")
            print("1. Listar todas las editoriales")
            print("2. Agregar una nueva editorial")
            print("3. Modificar una editorial")
            print("4. Eliminar una editorial")
            print("0. Volver al menú principal")
            
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.listar_editoriales()
            elif opcion == '2':
                self.crear_editorial()
            elif opcion == '3':
                self.modificar_editorial()
            elif opcion == '4':
                self.eliminar_editorial()
            elif opcion == '0':
                break
            else:
                print("\nOpción inválida.")

    # CRUD (Lógica de Interfaz)

    def listar_libros(self):
        print("\nListado de Libros:")
        libros = self.servicios['libro'].obtener_todos()
        if not libros:
            print("No hay libros registrados.")
            return
        for l in libros:
            print(f"[{l.id}] {l.titulo} - Autor: {l.autor} - Precio: {l.precio.valor} {l.precio.moneda.simbolo}")

    def crear_libro(self):
        print("\nAgregar Nuevo Libro:")
        try:
            libros_actuales = self.servicios['libro'].obtener_todos()
            id_libro = max((l.id for l in libros_actuales), default=0) + 1
            
            isbn = input("Ingrese ISBN: ")
            titulo = input("Ingrese Título: ")
            autor = input("Ingrese Autor: ")
            
            print("\n--- Géneros Disponibles ---")
            for g in self.servicios['genero'].obtener_todos():
                print(f"[{g.id}] {g.nombre}")
            id_genero = int(input("Ingrese el ID del Género deseado: "))
            
            print("\n--- Editoriales Disponibles ---")
            for ed in self.servicios['editorial'].obtener_todos():
                print(f"[{ed.id}] {ed.nombre}")
            id_editorial = int(input("Ingrese el ID de la Editorial deseada: "))
            
            print("\n--- Configuración del Precio ---")
            valor_precio = float(input("Ingrese el valor numérico del precio (ej: 1500.50): "))
            
            print("\n--- Monedas Disponibles ---")
            for m in self.servicios['moneda'].obtener_todos():
                print(f"[{m.id}] {m.nombre} ({m.simbolo})")
            id_moneda = int(input("Ingrese el ID de la Moneda: "))
            
            print("\n--- Tipos de Cotización Disponibles ---")
            print("(Si es en Pesos ARS, elegí 'Oficial' por defecto)")
            for t in self.servicios['tipo_cotizacion'].obtener_todos():
                print(f"[{t.id}] {t.nombre}")
            id_tipo_cotizacion = int(input("Ingrese el ID del Tipo de Cotización: "))
            
            precios_actuales = self.servicios['precio'].obtener_todos()
            nuevo_id_precio = max((p.id for p in precios_actuales), default=0) + 1
            
            self.servicios['precio'].crear(
                id_precio=nuevo_id_precio, 
                valor=valor_precio, 
                id_moneda=id_moneda, 
                id_tipo_cotizacion=id_tipo_cotizacion
            )

            nuevo_libro = self.servicios['libro'].crear(
                id_libro=id_libro,
                isbn=isbn,
                titulo=titulo,
                autor=autor,
                id_genero=id_genero,
                id_editorial=id_editorial,
                id_precio=nuevo_id_precio
            )
            print(f"\nLibro '{nuevo_libro.titulo}' creado exitosamente!")
        except ValueError as e:
            print(f"\nError de validación: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")

    def listar_generos(self):
        print("\nListado de Géneros:")
        generos = self.servicios['genero'].obtener_todos()
        if not generos:
            print("No hay géneros registrados.")
            return
        for g in generos:
            print(f"[{g.id}] {g.nombre}")

    def crear_genero(self):
        print("\nAgregar Nuevo Género:")
        try:
            generos_actuales = self.servicios['genero'].obtener_todos()
            id_genero = max((g.id for g in generos_actuales), default=0) + 1
            
            nombre = input("Ingrese el Nombre del género: ")
            
            self.servicios['genero'].crear(id_genero, nombre)
            print(f"\nGénero '{nombre}' creado exitosamente!")
        except ValueError as e:
            print(f"\nError: {e}")

    def listar_editoriales(self):
        print("\nListado de Editoriales:")
        editoriales = self.servicios['editorial'].obtener_todos()
        if not editoriales:
            print("No hay editoriales registradas.")
            return
        for ed in editoriales:
            print(f"[{ed.id}] {ed.nombre}")

    def crear_editorial(self):
        print("\nAgregar Nueva Editorial:")
        try:
            editoriales_actuales = self.servicios['editorial'].obtener_todos()
            id_editorial = max((ed.id for ed in editoriales_actuales), default=0) + 1
            
            nombre = input("Ingrese el Nombre de la editorial: ")
            
            self.servicios['editorial'].crear(id_editorial, nombre)
            print(f"\nEditorial '{nombre}' creada exitosamente!")
        except ValueError as e:
            print(f"\nError: {e}")

    def modificar_libro(self):
        print("\nModificar Libro:")
        try:
            id_libro = int(input("Ingrese el ID del libro a modificar: "))
            libro = self.servicios['libro'].obtener_por_id(id_libro)
            if not libro:
                print("El libro no existe.")
                return
                
            isbn = input(f"Ingrese nuevo ISBN (actual: {libro.isbn}): ")
            titulo = input(f"Ingrese nuevo Título (actual: {libro.titulo}): ")
            autor = input(f"Ingrese nuevo Autor (actual: {libro.autor}): ")
            
            print("\n--- Géneros Disponibles ---")
            for g in self.servicios['genero'].obtener_todos():
                print(f"[{g.id}] {g.nombre}")
            id_genero = int(input(f"Ingrese el ID del nuevo Género (actual: {libro.genero.id}): "))
            
            print("\n--- Editoriales Disponibles ---")
            for ed in self.servicios['editorial'].obtener_todos():
                print(f"[{ed.id}] {ed.nombre}")
            id_editorial = int(input(f"Ingrese el ID de la nueva Editorial (actual: {libro.editorial.id}): "))
            
            id_precio = libro.precio.id
            
            libro_mod = self.servicios['libro'].actualizar(
                id_libro=id_libro, isbn=isbn, titulo=titulo, autor=autor, 
                id_genero=id_genero, id_editorial=id_editorial, id_precio=id_precio
            )
            print(f"\nLibro '{libro_mod.titulo}' modificado exitosamente!")
        except ValueError as e:
            print(f"\nError de validación: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")

    def eliminar_libro(self):
        print("\nEliminar Libro:")
        try:
            id_libro = int(input("Ingrese el ID del libro a eliminar: "))
            if self.servicios['libro'].eliminar(id_libro):
                print("\nLibro eliminado exitosamente!")
            else:
                print("\nEl libro no existe o no se pudo eliminar.")
        except ValueError:
            print("\nError: ID inválido.")

    def modificar_genero(self):
        print("\nModificar Género:")
        try:
            id_genero = int(input("Ingrese el ID del género a modificar: "))
            nombre = input("Ingrese el nuevo Nombre del género: ")
            self.servicios['genero'].actualizar(id_genero, nombre)
            print(f"\nGénero modificado exitosamente!")
        except ValueError as e:
            print(f"\nError: {e}")

    def eliminar_genero(self):
        print("\nEliminar Género:")
        try:
            id_genero = int(input("Ingrese el ID del género a eliminar: "))
            if self.servicios['genero'].eliminar(id_genero):
                print("\nGénero eliminado exitosamente!")
            else:
                print("\nEl género no existe.")
        except ValueError:
            print("\nError: ID inválido.")

    def modificar_editorial(self):
        print("\nModificar Editorial:")
        try:
            id_editorial = int(input("Ingrese el ID de la editorial a modificar: "))
            nombre = input("Ingrese el nuevo Nombre de la editorial: ")
            self.servicios['editorial'].actualizar(id_editorial, nombre)
            print(f"\nEditorial modificada exitosamente!")
        except ValueError as e:
            print(f"\nError: {e}")

    def eliminar_editorial(self):
        print("\nEliminar Editorial:")
        try:
            id_editorial = int(input("Ingrese el ID de la editorial a eliminar: "))
            if self.servicios['editorial'].eliminar(id_editorial):
                print("\nEditorial eliminada exitosamente!")
            else:
                print("\nLa editorial no existe.")
        except ValueError:
            print("\nError: ID inválido.")

    # --- CRUD MONEDAS ---
    def menu_monedas(self):
        while True:
            print("\n--- GESTIÓN DE MONEDAS ---")
            print("1. Listar todas")
            print("2. Agregar")
            print("3. Modificar")
            print("4. Eliminar")
            print("0. Volver")
            op = input("Seleccione una opción: ")
            if op == '1': self.listar_monedas()
            elif op == '2': self.crear_moneda()
            elif op == '3': self.modificar_moneda()
            elif op == '4': self.eliminar_moneda()
            elif op == '0': break
            else: print("Opción inválida.")

    def listar_monedas(self):
        elementos = self.servicios['moneda'].obtener_todos()
        if not elementos:
            print("No hay monedas registradas.")
            return
        for e in elementos: print(f"[{e.id}] {e.nombre} ({e.simbolo})")

    def crear_moneda(self):
        print("\nAgregar Nueva Moneda:")
        try:
            elementos = self.servicios['moneda'].obtener_todos()
            nuevo_id = max((e.id for e in elementos), default=0) + 1
            nombre = input("Ingrese el Nombre: ")
            simbolo = input("Ingrese el Símbolo: ")
            self.servicios['moneda'].crear(nuevo_id, nombre, simbolo)
            print("Creado exitosamente!")
        except Exception as e:
            print(f"Error: {e}")

    def modificar_moneda(self):
        try:
            id_val = int(input("Ingrese ID a modificar: "))
            nombre = input("Ingrese nuevo Nombre: ")
            simbolo = input("Ingrese nuevo Símbolo: ")
            self.servicios['moneda'].actualizar(id_val, nombre, simbolo)
            print("Modificado exitosamente!")
        except Exception as e:
            print(f"Error: {e}")

    def eliminar_moneda(self):
        try:
            id_val = int(input("Ingrese ID a eliminar: "))
            if self.servicios['moneda'].eliminar(id_val): print("Eliminado exitosamente!")
            else: print("No existe o error al eliminar.")
        except Exception as e:
            print(f"Error: {e}")

    # --- CRUD TIPOS DE COTIZACIÓN ---
    def menu_tipos_cotizacion(self):
        while True:
            print("\n--- GESTIÓN DE TIPOS DE COTIZACIÓN ---")
            print("1. Listar")
            print("2. Agregar")
            print("3. Modificar")
            print("4. Eliminar")
            print("0. Volver")
            op = input("Seleccione una opción: ")
            if op == '1': self.listar_tipos_cotizacion()
            elif op == '2': self.crear_tipo_cotizacion()
            elif op == '3': self.modificar_tipo_cotizacion()
            elif op == '4': self.eliminar_tipo_cotizacion()
            elif op == '0': break
            else: print("Opción inválida.")

    def listar_tipos_cotizacion(self):
        elementos = self.servicios['tipo_cotizacion'].obtener_todos()
        if not elementos:
            print("No hay tipos registrados.")
            return
        for e in elementos: print(f"[{e.id}] {e.nombre}")

    def crear_tipo_cotizacion(self):
        try:
            elementos = self.servicios['tipo_cotizacion'].obtener_todos()
            nuevo_id = max((e.id for e in elementos), default=0) + 1
            nombre = input("Ingrese el Nombre: ")
            self.servicios['tipo_cotizacion'].crear(nuevo_id, nombre)
            print("Creado exitosamente!")
        except Exception as e: print(f"Error: {e}")

    def modificar_tipo_cotizacion(self):
        try:
            id_val = int(input("Ingrese ID a modificar: "))
            nombre = input("Ingrese nuevo Nombre: ")
            self.servicios['tipo_cotizacion'].actualizar(id_val, nombre)
            print("Modificado exitosamente!")
        except Exception as e: print(f"Error: {e}")

    def eliminar_tipo_cotizacion(self):
        try:
            id_val = int(input("Ingrese ID a eliminar: "))
            if self.servicios['tipo_cotizacion'].eliminar(id_val): print("Eliminado exitosamente!")
            else: print("No existe o error.")
        except Exception as e: print(f"Error: {e}")

    # --- CRUD COTIZACION DOLAR ---
    def menu_cotizaciones(self):
        while True:
            print("\n--- GESTIÓN DE COTIZACIÓN DEL DÓLAR ---")
            print("1. Listar")
            print("2. Agregar")
            print("3. Modificar")
            print("4. Eliminar")
            print("0. Volver")
            op = input("Seleccione una opción: ")
            if op == '1': self.listar_cotizaciones()
            elif op == '2': self.crear_cotizacion()
            elif op == '3': self.modificar_cotizacion()
            elif op == '4': self.eliminar_cotizacion()
            elif op == '0': break
            else: print("Opción inválida.")

    def listar_cotizaciones(self):
        elementos = self.servicios['cotizacion'].obtener_todos()
        if not elementos:
            print("No hay cotizaciones registradas.")
            return
        for e in elementos: print(f"[Tipo {e.tipo_cotizacion.id}] {e.fecha}: {e.valor}")

    def crear_cotizacion(self):
        from datetime import date
        try:
            self.listar_tipos_cotizacion()
            id_tipo = int(input("ID Tipo: "))
            valor = float(input("Valor numérico: "))
            self.servicios['cotizacion'].crear(valor, date.today(), id_tipo)
            print("Creado exitosamente!")
        except Exception as e: print(f"Error: {e}")

    def modificar_cotizacion(self):
        from datetime import date
        try:
            id_tipo = int(input("ID Tipo: "))
            valor = float(input("Nuevo valor: "))
            self.servicios['cotizacion'].actualizar(valor, date.today(), id_tipo)
            print("Modificado exitosamente!")
        except Exception as e: print(f"Error: {e}")

    def eliminar_cotizacion(self):
        from datetime import date
        try:
            id_tipo = int(input("ID Tipo a eliminar: "))
            if self.servicios['cotizacion'].eliminar(id_tipo, date.today()): print("Eliminado!")
            else: print("No se encontró.")
        except Exception as e: print(f"Error: {e}")

    # --- CRUD PRECIOS ---
    def menu_precios(self):
        while True:
            print("\n--- GESTIÓN DE PRECIOS ---")
            print("1. Listar")
            print("2. Agregar")
            print("3. Modificar")
            print("4. Eliminar")
            print("0. Volver")
            op = input("Seleccione una opción: ")
            if op == '1': self.listar_precios()
            elif op == '2': self.crear_precio()
            elif op == '3': self.modificar_precio()
            elif op == '4': self.eliminar_precio()
            elif op == '0': break
            else: print("Opción inválida.")

    def listar_precios(self):
        elementos = self.servicios['precio'].obtener_todos()
        if not elementos:
            print("No hay precios registrados.")
            return
        for e in elementos: print(f"[{e.id}] {e.valor} {e.moneda.simbolo} (Tipo {e.tipo_cotizacion.id if e.tipo_cotizacion else 'N/A'})")

    def crear_precio(self):
        try:
            elementos = self.servicios['precio'].obtener_todos()
            nuevo_id = max((e.id for e in elementos), default=0) + 1
            valor = float(input("Valor numérico: "))
            self.listar_monedas()
            id_moneda = int(input("ID Moneda: "))
            self.listar_tipos_cotizacion()
            id_tipo = int(input("ID Tipo Cotización (0 para nulo): "))
            id_tipo = None if id_tipo == 0 else id_tipo
            self.servicios['precio'].crear(nuevo_id, valor, id_moneda, id_tipo)
            print("Creado exitosamente!")
        except Exception as e: print(f"Error: {e}")

    def modificar_precio(self):
        try:
            id_val = int(input("ID a modificar: "))
            valor = float(input("Nuevo valor: "))
            id_moneda = int(input("ID Moneda: "))
            id_tipo = int(input("ID Tipo Cotización (0 para nulo): "))
            id_tipo = None if id_tipo == 0 else id_tipo
            self.servicios['precio'].actualizar(id_val, valor, id_moneda, id_tipo)
            print("Modificado exitosamente!")
        except Exception as e: print(f"Error: {e}")

    def eliminar_precio(self):
        try:
            id_val = int(input("ID a eliminar: "))
            if self.servicios['precio'].eliminar(id_val): print("Eliminado!")
            else: print("No encontrado.")
        except Exception as e: print(f"Error: {e}")

    # --- CRUD STOCKS ---
    def menu_stocks(self):
        while True:
            print("\n--- GESTIÓN DE STOCK ---")
            print("1. Listar")
            print("2. Agregar")
            print("3. Modificar")
            print("4. Eliminar")
            print("0. Volver")
            op = input("Seleccione una opción: ")
            if op == '1': self.listar_stocks()
            elif op == '2': self.crear_stock()
            elif op == '3': self.modificar_stock()
            elif op == '4': self.eliminar_stock()
            elif op == '0': break
            else: print("Opción inválida.")

    def listar_stocks(self):
        elementos = self.servicios['stock'].obtener_todos()
        if not elementos:
            print("No hay stocks registrados.")
            return
        for e in elementos: print(f"[{e.id}] Libro {e.libro.titulo}: {e.cantidad} unidades")

    def crear_stock(self):
        try:
            elementos = self.servicios['stock'].obtener_todos()
            nuevo_id = max((e.id for e in elementos), default=0) + 1
            self.listar_libros()
            id_libro = int(input("ID Libro: "))
            cantidad = int(input("Cantidad: "))
            self.servicios['stock'].crear(nuevo_id, cantidad, id_libro)
            print("Creado exitosamente!")
        except Exception as e: print(f"Error: {e}")

    def modificar_stock(self):
        try:
            id_val = int(input("ID de Stock a modificar: "))
            id_libro = int(input("ID Libro: "))
            cantidad = int(input("Nueva Cantidad: "))
            self.servicios['stock'].actualizar(id_val, cantidad, id_libro)
            print("Modificado exitosamente!")
        except Exception as e: print(f"Error: {e}")

    def eliminar_stock(self):
        try:
            id_val = int(input("ID a eliminar: "))
            if self.servicios['stock'].eliminar(id_val): print("Eliminado!")
            else: print("No encontrado.")
        except Exception as e: print(f"Error: {e}")
