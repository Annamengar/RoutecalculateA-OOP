import heapq

class Mapa:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.mapa = [[0 for _ in range(ancho)] for _ in range(alto)]
        self.inicio = None
        self.fin = None

    def agregar_obstaculo(self, x, y, tipo):
        if 0 <= x < self.ancho and 0 <= y < self.alto:
            self.mapa[y][x] = tipo

    def quitar_obstaculo(self, x, y):
        if 0 <= x < self.ancho and 0 <= y < self.alto:
            self.mapa[y][x] = 0

    def es_accesible(self, x, y):
        return 0 <= x < self.ancho and 0 <= y < self.alto and self.mapa[y][x] == 0

    def mostrar(self, ruta=[]):
        for y in range(self.alto):
            for x in range(self.ancho):
                if (x, y) == self.inicio:
                    print("I", end=" ")
                elif (x, y) == self.fin:
                    print("F", end=" ")
                elif (x, y) in ruta:
                    print("*", end=" ")
                elif self.mapa[y][x] == 0:
                    print(".", end=" ")
                elif self.mapa[y][x] == 1:
                    print("X", end=" ")
                elif self.mapa[y][x] == 2:
                    print("A", end=" ")
                elif self.mapa[y][x] == 3:
                    print("B", end=" ")
            print()
        print()

class CalculadoraRutas:
    def __init__(self, mapa):
        self.mapa = mapa

    def heuristica(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def encontrar_ruta(self):
        inicio = self.mapa.inicio
        fin = self.mapa.fin
        open_set = []
        heapq.heappush(open_set, (0, inicio))
        came_from = {}
        g_score = {inicio: 0}
        f_score = {inicio: self.heuristica(inicio, fin)}

        while open_set:
            _, actual = heapq.heappop(open_set)

            if actual == fin:
                camino = []
                while actual in came_from:
                    camino.append(actual)
                    actual = came_from[actual]
                camino.append(inicio)
                return camino[::-1]

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                vecino = (actual[0] + dx, actual[1] + dy)
                if self.mapa.es_accesible(vecino[0], vecino[1]):
                    tentativo_g_score = g_score[actual] + 1

                    if vecino not in g_score or tentativo_g_score < g_score[vecino]:
                        came_from[vecino] = actual
                        g_score[vecino] = tentativo_g_score
                        f_score[vecino] = tentativo_g_score + self.heuristica(vecino, fin)
                        heapq.heappush(open_set, (f_score[vecino], vecino))

        return []

def obtener_coordenadas(mensaje, ancho, alto):
    while True:
        try:
            x, y = map(int, input(mensaje).split())
            if 0 <= x < ancho and 0 <= y < alto:
                return x, y
            else:
                print(f"Coordenadas fuera de rango. Deben estar entre 0 y {ancho-1} para x y entre 0 y {alto-1} para y.")
        except ValueError:
            print("Entrada inválida. Ingrese dos números enteros separados por un espacio.")

def main():
    ancho, alto = 10, 10
    mapa = Mapa(ancho, alto)

    print("Configuración del mapa:")
    while True:
        try:
            x, y = obtener_coordenadas("Ingrese las coordenadas del obstáculo (x y) o 'q' para terminar: ", ancho, alto)
            tipo = int(input("Ingrese el tipo de obstáculo (1: Edificio, 2: Agua, 3: Bloqueo temporal): "))
            if tipo in [1, 2, 3]:
                mapa.agregar_obstaculo(x, y, tipo)
            else:
                print("Tipo de obstáculo inválido.")
            continuar = input("¿Desea agregar otro obstáculo? (s/n): ")
            if continuar.lower() != 's':
                break
        except ValueError:
            print("Entrada inválida.")

    print("Mapa después de agregar obstáculos:")
    mapa.mostrar()

    while True:
        accion = input("¿Desea remover algún obstáculo? (s/n): ").lower()
        if accion == 'n':
            break
        try:
            x, y = obtener_coordenadas("Ingrese las coordenadas del obstáculo a remover (x y): ", ancho, alto)
            mapa.quitar_obstaculo(x, y)
        except ValueError:
            print("Entrada inválida.")

    print("Mapa después de remover obstáculos:")
    mapa.mostrar()

    x_inicio, y_inicio = obtener_coordenadas("Ingrese las coordenadas de inicio (x y): ", ancho, alto)
    x_fin, y_fin = obtener_coordenadas("Ingrese las coordenadas de fin (x y): ", ancho, alto)
    
    mapa.inicio = (x_inicio, y_inicio)
    mapa.fin = (x_fin, y_fin)

    if not mapa.es_accesible(x_inicio, y_inicio) or not mapa.es_accesible(x_fin, y_fin):
        print("Las coordenadas de inicio o fin no pueden ser obstáculos.")
        return

    print("Mapa antes de ejecutar A*:")
    mapa.mostrar()

    calculadora = CalculadoraRutas(mapa)
    ruta = calculadora.encontrar_ruta()

    if not ruta:
        print("No se encontró una ruta.")
    else:
        print("Mapa con la ruta encontrada:")
        mapa.mostrar(ruta)

    input("Presione Enter para salir.")

if __name__ == "__main__":
    main()
