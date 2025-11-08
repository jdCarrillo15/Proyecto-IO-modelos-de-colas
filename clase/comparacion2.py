import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# -------------------------------
# CONFIGURACIÓN DE MODELOS
# -------------------------------

models_config = {
    "M/M/1":  {"λ": 2.0, "μ": 3.0, "c": 1, "k": 1},
    "M/M/c":  {"λ": 4.0, "μ": 3.0, "c": 3, "k": 1},
    "M/M/k/1": {"λ": 6.0, "μ": 3.5, "c": 1, "k": 3},
    "M/M/k/c": {"λ": 8.0, "μ": 4.0, "c": 2, "k": 3},
}

SIM_TIME = 200

# -------------------------------
# DEFINICIÓN DE MODELOS
# -------------------------------

def simulate_mm1(cfg):
    n = 0
    queue = []
    for t in range(SIM_TIME):
        if random.random() < cfg["λ"] / 10:
            queue.append(1)
        if n > 0 and random.random() < cfg["μ"] / 10:
            n -= 1
        n = len(queue)
        if n > 0 and random.random() < cfg["μ"] / 10:
            queue.pop(0)
        yield n

def simulate_mmc(cfg):
    queue = []
    for t in range(SIM_TIME):
        if random.random() < cfg["λ"] / 10:
            queue.append(1)
        service = min(cfg["c"], len(queue))
        for _ in range(service):
            if random.random() < cfg["μ"] / 10:
                queue.pop(0)
        yield len(queue)

def simulate_mmk1(cfg):
    queues = [[] for _ in range(cfg["k"])]
    for t in range(SIM_TIME):
        if random.random() < cfg["λ"] / 10:
            random.choice(queues).append(1)
        for q in queues:
            if len(q) > 0 and random.random() < cfg["μ"] / 10:
                q.pop(0)
        yield sum(len(q) for q in queues)

def simulate_mmkc(cfg):
    queues = [[] for _ in range(cfg["k"])]
    for t in range(SIM_TIME):
        if random.random() < cfg["λ"] / 10:
            random.choice(queues).append(1)
        for q in queues:
            service = min(cfg["c"], len(q))
            for _ in range(service):
                if random.random() < cfg["μ"] / 10:
                    q.pop(0)
        yield sum(len(q) for q in queues)

# Asignar modelos
models = {
    "M/M/1": simulate_mm1,
    "M/M/c": simulate_mmc,
    "M/M/k/1": simulate_mmk1,
    "M/M/k/c": simulate_mmkc
}

# -------------------------------
# VISUALIZACIÓN EN TIEMPO REAL
# -------------------------------

fig, axs = plt.subplots(2, 2, figsize=(12, 8))
axes = axs.flatten()

lines = {}
texts = {}
data = {key: [] for key in models}
time = []

# Inicializar gráficos
for ax, key in zip(axes, models.keys()):
    cfg = models_config[key]
    ax.set_title(key)
    ax.set_xlim(0, SIM_TIME)
    ax.set_ylim(0, 40)
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Clientes en sistema")
    lines[key], = ax.plot([], [], lw=2, label="Clientes")
    ax.legend(loc="upper left")

    # Mostrar parámetros dinámicos
    texts[key] = ax.text(
        0.02, 0.85, "", transform=ax.transAxes,
        fontsize=9, verticalalignment="top",
        bbox=dict(facecolor="white", alpha=0.6)
    )

# Generadores por modelo
gens = {key: models[key](models_config[key]) for key in models.keys()}

def update(frame):
    time.append(frame)
    for key, gen in gens.items():
        cfg = models_config[key]
        try:
            n = next(gen)
            data[key].append(n)
            lines[key].set_data(time, data[key])

            # cálculo de utilización ρ = λ / (μ * c)
            rho = round(cfg["λ"] / (cfg["μ"] * cfg["c"]), 3)

            # texto dinámico con parámetros
            text = (
                f"λ = {cfg['λ']}\n"
                f"μ = {cfg['μ']}\n"
                f"c = {cfg['c']}\n"
                f"k = {cfg['k']}\n"
                f"ρ = {rho}\n"
                f"Clientes actuales: {n}"
            )
            texts[key].set_text(text)
        except StopIteration:
            pass
    return list(lines.values()) + list(texts.values())

ani = animation.FuncAnimation(
    fig, update, frames=range(SIM_TIME),
    blit=False, interval=200, repeat=False
)

plt.tight_layout()
plt.show()
