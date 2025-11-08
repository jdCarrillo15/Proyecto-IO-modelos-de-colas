import random
import math
import time

# ----------------------------------------
# Funciones auxiliares
# ----------------------------------------

def exp_random(rate):
    """Genera un valor aleatorio con distribución exponencial."""
    return -math.log(1 - random.random()) / rate

# ----------------------------------------
# Clase base para modelos de colas
# ----------------------------------------

class Cola:
    def __init__(self, lmbda, mu, servidores=1, capacidad=None, nombre=""):
        self.lmbda = lmbda          # tasa de llegada
        self.mu = mu                # tasa de servicio
        self.servidores = servidores
        self.capacidad = capacidad  # capacidad máxima (None = infinita)
        self.nombre = nombre

        # Estado del sistema
        self.tiempo = 0
        self.evento_llegada = exp_random(lmbda)
        self.evento_salida = float('inf')
        self.en_sistema = 0
        self.en_servicio = 0
        self.cola = 0
        self.atendidos = 0
        self.rechazados = 0

    def avanzar(self):
        """Avanza al siguiente evento (llegada o salida)."""
        if self.evento_llegada < self.evento_salida:
            self.tiempo = self.evento_llegada
            self.procesar_llegada()
        else:
            self.tiempo = self.evento_salida
            self.procesar_salida()

    def procesar_llegada(self):
        """Procesa evento de llegada de un cliente."""
        if self.capacidad and self.en_sistema >= self.capacidad:
            self.rechazados += 1  # sistema lleno
        else:
            self.en_sistema += 1
            if self.en_servicio < self.servidores:
                self.en_servicio += 1
                self.evento_salida = self.tiempo + exp_random(self.mu)
            else:
                self.cola += 1
        self.evento_llegada = self.tiempo + exp_random(self.lmbda)

    def procesar_salida(self):
        """Procesa evento de salida (fin de servicio)."""
        self.en_sistema -= 1
        self.atendidos += 1
        if self.cola > 0:
            self.cola -= 1
            self.evento_salida = self.tiempo + exp_random(self.mu)
        elif self.en_servicio > 1:
            self.en_servicio -= 1
            self.evento_salida = self.tiempo + exp_random(self.mu)
        elif self.en_servicio == 1 and self.en_sistema > 0:
            self.evento_salida = self.tiempo + exp_random(self.mu)
        else:
            self.en_servicio = max(0, self.en_servicio - 1)
            self.evento_salida = float('inf')

    def estado(self):
        """Retorna el estado actual del sistema."""
        return {
            "modelo": self.nombre,
            "t": round(self.tiempo, 2),
            "en_sistema": self.en_sistema,
            "cola": self.cola,
            "servidores": self.en_servicio,
            "atendidos": self.atendidos,
            "rechazados": self.rechazados
        }

# ----------------------------------------
# Simulación en paralelo
# ----------------------------------------

def simular_modelos(tiempo_total=30):
    # Definir parámetros base
    lmbda = 4     # tasa de llegada
    mu = 5        # tasa de servicio
    c = 3         # servidores
    k = 5         # capacidad máxima (para modelos con límite)

    # Crear los 4 modelos
    modelos = [
        Cola(lmbda, mu, 1, None, "M/M/1"),
        Cola(lmbda, mu, c, None, f"M/M/{c}"),
        Cola(lmbda, mu, 1, k, f"M/M/{k}/1"),
        Cola(lmbda, mu, c, k, f"M/M/{k}/{c}")
    ]

    print("\n🌀 SIMULACIÓN DE MODELOS DE COLAS EN PARALELO")
    print("---------------------------------------------------------")
    print(f"{'Modelo':<10} {'t':>4} {'Sistema':>9} {'Cola':>6} {'Serv':>6} {'Atend.':>8} {'Rech.':>6}")
    print("---------------------------------------------------------")

    # Simulación paso a paso
    pasos = 0
    while pasos < tiempo_total:
        pasos += 1
        for cola in modelos:
            cola.avanzar()
            estado = cola.estado()
            print(f"{estado['modelo']:<10} {estado['t']:>4.1f} {estado['en_sistema']:>9} {estado['cola']:>6} "
                  f"{estado['servidores']:>6} {estado['atendidos']:>8} {estado['rechazados']:>6}")
        print("-"*60)
        time.sleep(0.3)  # Pausa para efecto dinámico

    print("\n✅ Simulación finalizada.")

# ----------------------------------------
# MAIN
# ----------------------------------------

if __name__ == "__main__":
    simular_modelos(tiempo_total=30)
