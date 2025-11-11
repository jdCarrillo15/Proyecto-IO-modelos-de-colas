"""
COMPARACIÓN ANIMADA DE MODELOS DE COLA
========================================

Este script muestra una comparación visual animada de los 4 modelos de cola
implementados en el proyecto, simulando el flujo de clientes a través del sistema.

Modelos:
- M/M/1: Un servidor, capacidad infinita
- M/M/c: Múltiples servidores, capacidad infinita
- M/M/k/1: Un servidor, múltiples colas (capacidad limitada)
- M/M/k/c: Múltiples servidores, múltiples colas (capacidad limitada)

Uso:
    python animacion-comparacion.py

Autor: Proyecto IO - UPTC
"""

import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# -------------------------
# CONFIGURACIÓN DE LOS MODELOS
# -------------------------
MODELOS = {
    "M/M/1":  {"λ": 0.4, "μ": 0.8, "c": 1, "k": 1},
    "M/M/c":  {"λ": 0.8, "μ": 1.0, "c": 3, "k": 1},
    "M/M/k/1": {"λ": 1.0, "μ": 0.9, "c": 1, "k": 3},
    "M/M/k/c": {"λ": 1.2, "μ": 1.0, "c": 2, "k": 3},
}

NUM_CLIENTES = 15
SIM_TIME = 100

# -------------------------
# GENERAR CLIENTES
# -------------------------
def generar_clientes(lmbd, mu):
    clientes = []
    tiempo = 0
    for i in range(NUM_CLIENTES):
        llegada = random.expovariate(lmbd)
        servicio = random.expovariate(mu)
        tiempo += llegada
        clientes.append({
            "id": f"U{i+1}",
            "llegada": tiempo,
            "servicio": servicio
        })
    return clientes

BASE = generar_clientes(0.6, 1.0)

# -------------------------
# SIMULAR MODELOS DE COLA
# -------------------------
def simular_MM1(clientes, cfg):
    eventos = []
    libre = 0
    for u in clientes:
        inicio = max(u["llegada"], libre)
        fin = inicio + u["servicio"]
        libre = fin
        eventos.append((u["id"], u["llegada"], inicio, fin))
    return eventos

def simular_MMc(clientes, cfg):
    servidores = [0]*cfg["c"]
    eventos = []
    for u in clientes:
        i = servidores.index(min(servidores))
        inicio = max(u["llegada"], servidores[i])
        fin = inicio + u["servicio"]
        servidores[i] = fin
        eventos.append((u["id"], u["llegada"], inicio, fin))
    return eventos

def simular_MMk1(clientes, cfg):
    servidores = [0]*cfg["k"]
    eventos = []
    for u in clientes:
        q = random.randint(0, cfg["k"]-1)
        inicio = max(u["llegada"], servidores[q])
        fin = inicio + u["servicio"]
        servidores[q] = fin
        eventos.append((u["id"], u["llegada"], inicio, fin, q))
    return eventos

def simular_MMkC(clientes, cfg):
    colas = [[0]*cfg["c"] for _ in range(cfg["k"])]
    eventos = []
    for u in clientes:
        q = random.randint(0, cfg["k"]-1)
        s = colas[q].index(min(colas[q]))
        inicio = max(u["llegada"], colas[q][s])
        fin = inicio + u["servicio"]
        colas[q][s] = fin
        eventos.append((u["id"], u["llegada"], inicio, fin, q, s))
    return eventos

SIMS = {
    "M/M/1": simular_MM1(BASE, MODELOS["M/M/1"]),
    "M/M/c": simular_MMc(BASE, MODELOS["M/M/c"]),
    "M/M/k/1": simular_MMk1(BASE, MODELOS["M/M/k/1"]),
    "M/M/k/c": simular_MMkC(BASE, MODELOS["M/M/k/c"]),
}

# -------------------------
# ANIMACIÓN VISUAL TIPO PACKET TRACER
# -------------------------
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
axes = axs.flatten()
colores = ["#4CAF50", "#2196F3", "#FF9800", "#E91E63"]

circulos = {}
textos = {}

for ax, (modelo, color) in zip(axes, zip(SIMS.keys(), colores)):
    ax.set_title(modelo)
    ax.set_xlim(0, 100)
    ax.set_ylim(-1, 6)
    ax.set_xticks([])
    ax.set_yticks([])

    # Dibujar servidores (como cajas)
    cfg = MODELOS[modelo]
    if cfg["k"] == 1:
        for s in range(cfg["c"]):
            ax.add_patch(plt.Rectangle((60+s*5, 2), 3, 2, color=color, alpha=0.4))
    else:
        for k in range(cfg["k"]):
            for s in range(cfg["c"]):
                ax.add_patch(plt.Rectangle((60+s*5, 1.5+k*1.2), 3, 0.8, color=color, alpha=0.4))

    # Circulos (usuarios)
    clientes = SIMS[modelo]
    circulos[modelo] = [ax.plot([], [], 'o', color=color)[0] for _ in clientes]
    textos[modelo] = ax.text(1, 5.5, "", fontsize=8)

def update(frame):
    for modelo in SIMS.keys():
        clientes = SIMS[modelo]
        for i, ev in enumerate(clientes):
            llegada = ev[1]
            inicio = ev[2]
            fin = ev[3]
            if frame < llegada:
                x = 0
                y = 2
            elif llegada <= frame < inicio:
                x = (frame - llegada) * 5
                y = 2
            elif inicio <= frame < fin:
                x = 50 + (frame - inicio) * 2
                y = 2
            else:
                x = 80 + (frame - fin)
                y = 2
            circulos[modelo][i].set_data([x], [y])
        textos[modelo].set_text(f"Tiempo: {frame:.1f}s")
    return []

ani = animation.FuncAnimation(fig, update, frames=range(100), interval=100)
plt.tight_layout()
plt.show()
