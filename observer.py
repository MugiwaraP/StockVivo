class Observador:
    def actualizar(self, producto):
        raise NotImplementedError

class AlertaStockBajo(Observador):
    def actualizar(self, producto):
        if producto.cantidad <= producto.stock_minimo:
            print(f"⚠️ ALERTA: El producto '{producto.nombre}' tiene stock bajo. Cantidad actual: {producto.cantidad}, Mínimo: {producto.stock_minimo}")
            return {
                'alerta': True,
                'mensaje': f"Stock bajo en '{producto.nombre}': {producto.cantidad} unidades (mínimo {producto.stock_minimo})"
            }
        return {'alerta': False}

class GestorInventario:
    def __init__(self):
        self._observadores = []

    def agregar_observador(self, observador):
        self._observadores.append(observador)

    def notificar(self, producto):
        alertas = []
        for observador in self._observadores:
            resultado = observador.actualizar(producto)
            if resultado and resultado.get('alerta'):
                alertas.append(resultado['mensaje'])
        return alertas

# Instancia global del gestor con la alerta registrada
gestor = GestorInventario()
gestor.agregar_observador(AlertaStockBajo())