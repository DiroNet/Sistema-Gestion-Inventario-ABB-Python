class Producto:
    def __init__(self, codigo, nombre, categoria, cantidad, fecha_vencimiento=None):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.cantidad = cantidad
        self.fecha_vencimiento = fecha_vencimiento

class Nodo:
    def __init__(self, producto):
        self.producto = producto
        self.izquierdo = None
        self.derecho = None

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def agregar(self, producto):
        if not self.raiz:
            self.raiz = Nodo(producto)
        else:
            self._agregar_recursivo(self.raiz, producto)

    def _agregar_recursivo(self, nodo, producto):
        if producto.codigo < nodo.producto.codigo:
            if nodo.izquierdo:
                self._agregar_recursivo(nodo.izquierdo, producto)
            else:
                nodo.izquierdo = Nodo(producto)
        elif producto.codigo > nodo.producto.codigo:
            if nodo.derecho:
                self._agregar_recursivo(nodo.derecho, producto)
            else:
                nodo.derecho = Nodo(producto)

    def buscar(self, codigo):
        return self._buscar_recursivo(self.raiz, codigo)

    def _buscar_recursivo(self, nodo, codigo):
        if not nodo:
            return None
        if codigo == nodo.producto.codigo:
            return nodo.producto
        elif codigo < nodo.producto.codigo:
            return self._buscar_recursivo(nodo.izquierdo, codigo)
        else:
            return self._buscar_recursivo(nodo.derecho, codigo)

    def eliminar(self, codigo):
        self.raiz = self._eliminar_recursivo(self.raiz, codigo)

    def _eliminar_recursivo(self, nodo, codigo):
        if not nodo:
            return None
        if codigo < nodo.producto.codigo:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, codigo)
        elif codigo > nodo.producto.codigo:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, codigo)
        else:
            if not nodo.izquierdo:
                return nodo.derecho
            if not nodo.derecho:
                return nodo.izquierdo

            sucesor = self._minimo(nodo.derecho)
            nodo.producto = sucesor.producto
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, sucesor.producto.codigo)
        return nodo

    def _minimo(self, nodo):
        while nodo.izquierdo:
            nodo = nodo.izquierdo
        return nodo

    def mostrar(self):
        productos = []
        self._inorden(self.raiz, productos)
        return productos

    def _inorden(self, nodo, productos):
        if nodo:
            self._inorden(nodo.izquierdo, productos)
            productos.append(nodo.producto)
            self._inorden(nodo.derecho, productos)

class SistemaInventario:
    def __init__(self):
        self.arbol = ArbolBinarioBusqueda()
        self.categorias = {}

    def agregar_producto(self, codigo, nombre, categoria, cantidad, fecha_vencimiento=None):
        producto_existente = self.arbol.buscar(codigo)
        
        if producto_existente:
            if producto_existente.nombre == nombre and producto_existente.categoria == categoria:
                producto_existente.cantidad += cantidad
                print(f"\n>>> Producto existente actualizado: {producto_existente.nombre} ahora tiene {producto_existente.cantidad} unidades.")
            else:
                print(f"\n>>> Error: Ya existe un producto con el código {codigo}, pero tiene un nombre o categoría diferente.")
        else:
            nuevo_producto = Producto(codigo, nombre, categoria, cantidad, fecha_vencimiento)
            self.arbol.agregar(nuevo_producto)
            if categoria not in self.categorias:
                self.categorias[categoria] = []
            self.categorias[categoria].append(nuevo_producto)
            print("\n>>> Producto agregado con éxito!")

    def buscar_producto(self, codigo):
        return self.arbol.buscar(codigo)

    def listar_por_categoria(self, categoria):
        return self.categorias.get(categoria, [])

    def eliminar_producto(self, codigo):
        producto = self.buscar_producto(codigo)
        if producto:
            self.arbol.eliminar(codigo)
            self.categorias[producto.categoria].remove(producto)

    def mostrar_inventario(self):
        return self.arbol.mostrar()

# Interfaz de consola
if __name__ == "__main__":
    sistema = SistemaInventario()

    while True:
        print("\n//=== Sistema de Gestión de Inventario ===//")
        print("1. Agregar producto")
        print("2. Buscar producto por código")
        print("3. Listar productos por categoría")
        print("4. Eliminar producto")
        print("5. Mostrar inventario completo")
        print("6. Salir")
        print("//=======================================//")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\n//--- Agregar Producto ---//")
            codigo = input("Código del producto: ")
            nombre = input("Nombre del producto: ")
            categoria = input("Categoría del producto: ")
            cantidad = int(input("Cantidad del producto: "))
            fecha_vencimiento = input("Fecha de vencimiento (opcional): ") or None
            sistema.agregar_producto(codigo, nombre, categoria, cantidad, fecha_vencimiento)

        elif opcion == "2":
            print("\n//--- Buscar Producto ---//")
            codigo = input("Ingrese el código del producto: ")
            producto = sistema.buscar_producto(codigo)
            if producto:
                print(f"\n>>> Producto encontrado: {producto.nombre}, Categoría: {producto.categoria}, Cantidad: {producto.cantidad}, Fecha de vencimiento: {producto.fecha_vencimiento}")
            else:
                print("\n>>> Producto no encontrado.")

        elif opcion == "3":
            print("\n//--- Listar por Categoría ---//")
            categoria = input("Ingrese la categoría: ")
            productos = sistema.listar_por_categoria(categoria)
            if productos:
                print(f"\n>>> Productos en la categoría '{categoria}':")
                for p in productos:
                    print(f"- {p.nombre} (Código: {p.codigo}, Cantidad: {p.cantidad}, Fecha de vencimiento: {p.fecha_vencimiento})")
            else:
                print("\n>>> No hay productos en esta categoría.")

        elif opcion == "4":
            print("\n//--- Eliminar Producto ---//")
            codigo = input("Ingrese el código del producto a eliminar: ")
            sistema.eliminar_producto(codigo)
            print("\n>>> Producto eliminado con éxito.")

        elif opcion == "5":
            print("\n//--- Inventario Completo ---//")
            productos = sistema.mostrar_inventario()
            if productos:
                for p in productos:
                    print(f"- {p.nombre} (Código: {p.codigo}, Categoría: {p.categoria}, Cantidad: {p.cantidad}, Fecha de vencimiento: {p.fecha_vencimiento})")
            else:
                print("\n>>> El inventario está vacío.")

        elif opcion == "6":
            print("\n>>> Saliendo del sistema. ¡Hasta luego!")
            break

        else:
            print("\n>>> Opción no válida. Por favor, intente de nuevo.")
