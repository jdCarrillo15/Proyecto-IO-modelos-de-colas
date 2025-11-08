import math
import random
import itertools
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

# -----------------------------
# Utilidades de distribución
# -----------------------------

def expovariate(rate: float) -> float:
    if rate <= 0:
        return float('inf')
    u = random.random()
    while u <= 0.0:
        u = random.random()
    return -math.log(u) / rate

# -----------------------------
# Entidades de simulación
# -----------------------------

@dataclass
class Job:
    id: int
    t_arrival: float
    service_time: float
    t_service_start: Optional[float] = None
    t_departure: Optional[float] = None

@dataclass
class Server:
    busy_until: float = 0.0
    current_job: Optional[Job] = None

# -----------------------------
# Base de simulación por eventos
# -----------------------------

class EventSim:
    def __init__(self, lam: float, mu: float, horizon: float):
        self.lam = lam
        self.mu = mu
        self.horizon = horizon
        self.time = 0.0
        self.next_arrival = expovariate(self.lam)
        self.jobs_created = 0
        self.jobs: List[Job] = []
        self.completed: List[Job] = []
        # Acumuladores para tiempo de espera en cola (Wq)
        self.total_wait_q: float = 0.0
        self.count_wait_q: int = 0

    def step(self):
        raise NotImplementedError

    def _new_job(self) -> Job:
        self.jobs_created += 1
        return Job(
            id=self.jobs_created,
            t_arrival=self.time,
            service_time=expovariate(self.mu),
        )

# -----------------------------
# Modelos concretos
# -----------------------------

class MM1(EventSim):
    def __init__(self, lam: float, mu: float, horizon: float):
        super().__init__(lam, mu, horizon)
        self.server = Server()
        self.queue: List[Job] = []

    def utilization(self) -> float:
        return min(1.0, self.lam / self.mu) if self.mu > 0 else 0.0

    def state(self) -> Dict:
        n_system = len(self.queue) + (1 if self.server.current_job else 0)
        n_queue = len(self.queue)
        return {
            't': self.time,
            'in_system': n_system,
            'in_queue': n_queue,
            'served': len(self.completed),
            'rejected': 0,
            'rho': self.utilization(),
            'wq_avg': (self.total_wait_q / self.count_wait_q) if self.count_wait_q > 0 else 0.0,
        }

    def _maybe_start_service(self):
        if (self.server.current_job is None) and self.queue:
            job = self.queue.pop(0)
            job.t_service_start = self.time
            # Acumular espera en cola
            self.total_wait_q += (job.t_service_start - job.t_arrival)
            self.count_wait_q += 1
            self.server.current_job = job
            self.server.busy_until = self.time + job.service_time

    def step(self):
        # Próximo evento: llegada o salida
        t_depart = self.server.busy_until if self.server.current_job else float('inf')
        if self.next_arrival <= t_depart and self.next_arrival <= self.horizon:
            # Llegada
            self.time = self.next_arrival
            job = self._new_job()
            self.queue.append(job)
            self.next_arrival = self.time + expovariate(self.lam)
            self._maybe_start_service()
        else:
            # Salida (si existe)
            if t_depart == float('inf'):
                # No más eventos
                self.time = self.horizon
                return
            self.time = t_depart
            job = self.server.current_job
            if job:
                job.t_departure = self.time
                self.completed.append(job)
            self.server.current_job = None
            self._maybe_start_service()

class MMC(EventSim):
    def __init__(self, lam: float, mu: float, c: int, horizon: float):
        super().__init__(lam, mu, horizon)
        self.servers: List[Server] = [Server() for _ in range(c)]
        self.queue: List[Job] = []

    def utilization(self) -> float:
        c = len(self.servers)
        return min(1.0, self.lam / (self.mu * c)) if self.mu > 0 and c > 0 else 0.0

    def state(self) -> Dict:
        busy = sum(1 for s in self.servers if s.current_job)
        n_system = len(self.queue) + busy
        return {
            't': self.time,
            'in_system': n_system,
            'in_queue': len(self.queue),
            'served': len(self.completed),
            'rejected': 0,
            'rho': self.utilization(),
            'wq_avg': (self.total_wait_q / self.count_wait_q) if self.count_wait_q > 0 else 0.0,
        }

    def _maybe_start_service(self):
        for s in self.servers:
            if not self.queue:
                break
            if s.current_job is None:
                job = self.queue.pop(0)
                job.t_service_start = self.time
                self.total_wait_q += (job.t_service_start - job.t_arrival)
                self.count_wait_q += 1
                s.current_job = job
                s.busy_until = self.time + job.service_time

    def step(self):
        # Calcular próxima salida
        next_depart = float('inf')
        depart_server_idx = None
        for i, s in enumerate(self.servers):
            if s.current_job and s.busy_until < next_depart:
                next_depart = s.busy_until
                depart_server_idx = i
        # Elegir mínimo entre llegada y salida
        t_next = min(self.next_arrival, next_depart, self.horizon)
        if t_next == self.horizon and self.horizon < float('inf'):
            self.time = self.horizon
            return
        if self.next_arrival <= next_depart:
            # Llegada
            self.time = self.next_arrival
            job = self._new_job()
            self.queue.append(job)
            self.next_arrival = self.time + expovariate(self.lam)
            self._maybe_start_service()
        else:
            # Salida
            if depart_server_idx is None:
                self.time = t_next
                return
            self.time = next_depart
            s = self.servers[depart_server_idx]
            job = s.current_job
            if job:
                job.t_departure = self.time
                self.completed.append(job)
            s.current_job = None
            self._maybe_start_service()

class MMK1(EventSim):
    """
    k colas paralelas, 1 servidor por cola, asignación por cola más corta.
    """
    def __init__(self, lam: float, mu: float, k: int, horizon: float):
        super().__init__(lam, mu, horizon)
        self.k = k
        self.servers: List[Server] = [Server() for _ in range(k)]
        self.queues: List[List[Job]] = [[] for _ in range(k)]

    def utilization(self) -> float:
        # Carga promedio por servidor
        return min(1.0, (self.lam / self.k) / self.mu) if self.k > 0 and self.mu > 0 else 0.0

    def state(self) -> Dict:
        busy = sum(1 for s in self.servers if s.current_job)
        n_queue = sum(len(q) for q in self.queues)
        return {
            't': self.time,
            'in_system': n_queue + busy,
            'in_queue': n_queue,
            'served': len(self.completed),
            'rejected': 0,
            'rho': self.utilization(),
            'wq_avg': (self.total_wait_q / self.count_wait_q) if self.count_wait_q > 0 else 0.0,
        }

    def _maybe_start_service(self, idx: int):
        s = self.servers[idx]
        q = self.queues[idx]
        if s.current_job is None and q:
            job = q.pop(0)
            job.t_service_start = self.time
            self.total_wait_q += (job.t_service_start - job.t_arrival)
            self.count_wait_q += 1
            s.current_job = job
            s.busy_until = self.time + job.service_time

    def step(self):
        # Próxima salida por cola
        next_depart = float('inf')
        idx_dep = None
        for i, s in enumerate(self.servers):
            if s.current_job and s.busy_until < next_depart:
                next_depart = s.busy_until
                idx_dep = i
        t_next = min(self.next_arrival, next_depart, self.horizon)
        if t_next == self.horizon and self.horizon < float('inf'):
            self.time = self.horizon
            return
        if self.next_arrival <= next_depart:
            self.time = self.next_arrival
            job = self._new_job()
            # Asignar a la cola más corta (empates al azar)
            lengths = [len(q) + (1 if s.current_job else 0) for q, s in zip(self.queues, self.servers)]
            m = min(lengths)
            candidates = [i for i, L in enumerate(lengths) if L == m]
            idx = random.choice(candidates)
            self.queues[idx].append(job)
            self.next_arrival = self.time + expovariate(self.lam)
            self._maybe_start_service(idx)
        else:
            # Salida
            if idx_dep is None:
                self.time = t_next
                return
            self.time = next_depart
            s = self.servers[idx_dep]
            job = s.current_job
            if job:
                job.t_departure = self.time
                self.completed.append(job)
            s.current_job = None
            self._maybe_start_service(idx_dep)

class MMKC(EventSim):
    """
    k colas, c servidores por cola (servicio por cola), asignación a cola más corta.
    """
    def __init__(self, lam: float, mu: float, k: int, c: int, horizon: float):
        super().__init__(lam, mu, horizon)
        self.k = k
        self.c = c
        self.servers: List[List[Server]] = [[Server() for _ in range(c)] for _ in range(k)]
        self.queues: List[List[Job]] = [[] for _ in range(k)]

    def utilization(self) -> float:
        total_servers = self.k * self.c
        return min(1.0, self.lam / (self.mu * total_servers)) if total_servers > 0 and self.mu > 0 else 0.0

    def state(self) -> Dict:
        busy = sum(1 for col in self.servers for s in col if s.current_job)
        n_queue = sum(len(q) for q in self.queues)
        return {
            't': self.time,
            'in_system': n_queue + busy,
            'in_queue': n_queue,
            'served': len(self.completed),
            'rejected': 0,
            'rho': self.utilization(),
            'wq_avg': (self.total_wait_q / self.count_wait_q) if self.count_wait_q > 0 else 0.0,
        }

    def _maybe_start_service(self, qi: int):
        q = self.queues[qi]
        if not q:
            return
        for s in self.servers[qi]:
            if s.current_job is None and q:
                job = q.pop(0)
                job.t_service_start = self.time
                self.total_wait_q += (job.t_service_start - job.t_arrival)
                self.count_wait_q += 1
                s.current_job = job
                s.busy_until = self.time + job.service_time

    def step(self):
        # Próxima salida global
        next_depart = float('inf')
        dep_qi, dep_si = None, None
        for qi, col in enumerate(self.servers):
            for si, s in enumerate(col):
                if s.current_job and s.busy_until < next_depart:
                    next_depart = s.busy_until
                    dep_qi, dep_si = qi, si
        t_next = min(self.next_arrival, next_depart, self.horizon)
        if t_next == self.horizon and self.horizon < float('inf'):
            self.time = self.horizon
            return
        if self.next_arrival <= next_depart:
            self.time = self.next_arrival
            job = self._new_job()
            # Elegir cola más corta (considerando servidores ocupados)
            lengths = [len(q) + sum(1 for s in col if s.current_job) for q, col in zip(self.queues, self.servers)]
            m = min(lengths)
            cands = [i for i, L in enumerate(lengths) if L == m]
            qi = random.choice(cands)
            self.queues[qi].append(job)
            self.next_arrival = self.time + expovariate(self.lam)
            self._maybe_start_service(qi)
        else:
            # Salida
            if dep_qi is None:
                self.time = t_next
                return
            self.time = next_depart
            s = self.servers[dep_qi][dep_si]
            job = s.current_job
            if job:
                job.t_departure = self.time
                self.completed.append(job)
            s.current_job = None
            self._maybe_start_service(dep_qi)

# -----------------------------
# Capa de animación (2x2)
# -----------------------------

@dataclass
class ModelSpec:
    name: str
    kind: str  # 'mm1' | 'mmc' | 'mmk1' | 'mmkc'
    params: Dict

@dataclass
class LiveSeries:
    t: List[float] = field(default_factory=list)
    in_system: List[int] = field(default_factory=list)
    in_queue: List[int] = field(default_factory=list)

class AnimatedComparison:
    def __init__(self, specs: List[ModelSpec], horizon: float = 60.0, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
        self.horizon = horizon
        self.specs = specs
        # Construir simuladores
        self.sims = []
        for sp in specs:
            if sp.kind == 'mm1':
                sim = MM1(sp.params['lam'], sp.params['mu'], horizon)
            elif sp.kind == 'mmc':
                sim = MMC(sp.params['lam'], sp.params['mu'], sp.params['c'], horizon)
            elif sp.kind == 'mmk1':
                sim = MMK1(sp.params['lam'], sp.params['mu'], sp.params['k'], horizon)
            elif sp.kind == 'mmkc':
                sim = MMKC(sp.params['lam'], sp.params['mu'], sp.params['k'], sp.params['c'], horizon)
            else:
                raise ValueError('Modelo no soportado')
            self.sims.append(sim)
        # Figura
        self.fig, axs = plt.subplots(2, 2, figsize=(12, 8))
        self.axes = axs.flatten()
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        self.texts = []
        # Elementos "muñequitos"
        # Clientes por panel: dict id-> sprite
        self.client_sprites: List[Dict[int, Dict]] = [dict() for _ in specs]
        # Servidores: posiciones y artistas por panel
        self.server_positions: List[List[Tuple[float, float]]] = [[] for _ in specs]
        self.server_artists: List[List[Tuple[Circle, Line2D]]] = [[] for _ in specs]
        # Nodos de llegada por panel
        self.arrival_nodes: List[List[Circle]] = [[] for _ in specs]

        for i, (ax, sp) in enumerate(zip(self.axes, self.specs)):
            # Título con parámetros por modelo
            p = sp.params
            parts = [f"λ={p.get('lam')}", f"μ={p.get('mu')}"]
            if 'c' in p:
                parts.append(f"c={p['c']}")
            if 'k' in p:
                parts.append(f"k={p['k']}")
            ax.set_title(f"{sp.name} (" + ", ".join(parts) + ")")
            ax.set_xlim(0, 100)
            ax.set_ylim(-2, 8)
            ax.set_xticks([])
            ax.set_yticks([])
            txt = ax.text(0.02, 0.95, '', transform=ax.transAxes, va='top', fontsize=9,
                           bbox=dict(facecolor='white', alpha=0.7))
            self.texts.append(txt)
            # Sin leyenda ni curvas, solo animación de nodos

            # Servidores como muñequitos (stick figures) en posiciones fijas
            x0 = 70.0
            dx = 5.0
            y_base = 2.0
            positions: List[Tuple[float, float]] = []
            if sp.kind == 'mm1':
                positions = [(x0, y_base)]
            elif sp.kind == 'mmc':
                c = sp.params['c']
                positions = [(x0 + cc*dx, y_base) for cc in range(c)]
            elif sp.kind == 'mmk1':
                k = sp.params['k']
                positions = [(x0, y_base + r*1.2) for r in range(k)]
            else:  # mmkc
                k = sp.params['k']
                c = sp.params['c']
                for r in range(k):
                    for cc in range(c):
                        positions.append((x0 + cc*dx, y_base + r*1.2))
            self.server_positions[i] = positions
            # Dibujar muñequitos de servidores
            s_artists: List[Tuple[Circle, Line2D]] = []
            for (sx, sy) in positions:
                head = Circle((sx, sy), radius=0.25, facecolor=self.colors[i], edgecolor='k', lw=0.8)
                body = Line2D([sx, sx], [sy-0.25, sy-0.9], color='k', lw=1.2)
                ax.add_patch(head)
                ax.add_line(body)
                s_artists.append((head, body))
            self.server_artists[i] = s_artists

            # Nodos de llegada (círculos) al inicio de la cola
            arrivals: List[Circle] = []
            x_arr = 15.0
            if sp.kind in ('mm1', 'mmc'):
                y_arrs = [y_base]
            elif sp.kind == 'mmk1':
                k = sp.params['k']
                y_arrs = [y_base + r*1.2 for r in range(k)]
            else:  # mmkc
                k = sp.params['k']
                y_arrs = [y_base + r*1.2 for r in range(k)]
            for ya in y_arrs:
                dot = Circle((x_arr, ya), radius=0.12, facecolor='black', alpha=0.6)
                ax.add_patch(dot)
                arrivals.append(dot)
            self.arrival_nodes[i] = arrivals

        self.anim = None

    def _spawn_client_artist(self, ax, color) -> Tuple[Circle, Line2D]:
        head = Circle((0, 0), radius=0.2, facecolor=color, edgecolor='k', lw=0.5)
        body = Line2D([0, 0], [-0.2, -0.8], color='k', lw=1)
        ax.add_patch(head)
        ax.add_line(body)
        return head, body

    def _place_client(self, artist: Tuple[Circle, Line2D], x: float, y: float):
        head, body = artist
        head.center = (x, y)
        body.set_data([x, x], [y-0.2, y-0.8])

    def _collect_clients_snapshot(self, sim: EventSim) -> List[Tuple[float, float]]:
        # Coordenadas para clientes: llegada->cola->servidor->salida
        coords: List[Tuple[float, float]] = []
        # Para representación simple: todos en una sola fila animada hacia la derecha
        # La cantidad de puntos representará en sistema
        state = getattr(sim, 'state')()
        n = state['in_system']
        for i in range(n):
            x = min(60, 5 + i * 1.0)
            y = 2.0
            coords.append((x, y))
        return coords

    def _advance_sims_until(self, t_target: float):
        for sim in self.sims:
            while sim.time < t_target and sim.time < sim.horizon:
                sim.step()

    def _update_panel(self, idx: int, frame_t: float):
        ax = self.axes[idx]
        sim = self.sims[idx]

        # Avanzar simulación hasta frame_t
        self._advance_sims_until(frame_t)

        st = sim.state()
        sp = self.specs[idx]
        p = sp.params
        # No hay gráfica temporal; límites fijos ya establecidos

        # Texto: solo tiempo de espera promedio en cola (Wq)
        self.texts[idx].set_text(
            f"Wq prom: {st.get('wq_avg', 0.0):.2f}"
        )
        
        # Actualizar muñequitos de clientes según estado real (colas y servicio)
        targets = self._layout_targets(idx)
        alive_ids = set(targets.keys())
        # Crear/actualizar sprites
        for jid, (tx, ty) in targets.items():
            sprite = self._ensure_client_sprite(idx, jid, x=0.0, y=ty)
            # Movimiento simple hacia el objetivo (interpolación)
            cx, cy = sprite['x'], sprite['y']
            alpha = 0.35
            nx = cx + alpha*(tx - cx)
            ny = cy + alpha*(ty - cy)
            self._place_client_sprite(sprite, nx, ny)
        # Remover sprites de jobs completados
        self._remove_missing_client_sprites(idx, alive_ids)

    # Nuevas utilidades para representar estado detallado
    def _ensure_client_sprite(self, panel_idx: int, job_id: int, x: float, y: float):
        dct = self.client_sprites[panel_idx]
        if job_id not in dct:
            head = Circle((x, y), radius=0.2, facecolor=self.colors[panel_idx], edgecolor='k', lw=0.5)
            body = Line2D([x, x], [y-0.2, y-0.8], color='k', lw=1)
            ax = self.axes[panel_idx]
            ax.add_patch(head)
            ax.add_line(body)
            dct[job_id] = {'artist': (head, body), 'x': x, 'y': y}
        return dct[job_id]

    def _place_client_sprite(self, sprite: Dict, x: float, y: float):
        head, body = sprite['artist']
        head.center = (x, y)
        body.set_data([x, x], [y-0.2, y-0.8])
        sprite['x'] = x
        sprite['y'] = y

    def _remove_missing_client_sprites(self, panel_idx: int, alive_ids: set):
        dct = self.client_sprites[panel_idx]
        remove_ids = [jid for jid in dct.keys() if jid not in alive_ids]
        for jid in remove_ids:
            head, body = dct[jid]['artist']
            head.remove(); body.remove()
            del dct[jid]

    def _layout_targets(self, idx: int) -> Dict[int, Tuple[float, float]]:
        sp = self.specs[idx]
        sim = self.sims[idx]
        targets: Dict[int, Tuple[float, float]] = {}
        # Colas y servidores por modelo
        x_queue_start = 20.0
        x_queue_step = 1.2
        if sp.kind == 'mm1':
            # Cola única
            yq = 2.0
            # En cola
            if isinstance(sim, MM1):
                for pos, job in enumerate(sim.queue):
                    targets[job.id] = (x_queue_start + pos*x_queue_step, yq)
                # En servicio
                if sim.server.current_job:
                    job = sim.server.current_job
                    sx, sy = self.server_positions[idx][0]
                    targets[job.id] = (sx, sy)
        elif sp.kind == 'mmc':
            yq = 2.0
            if isinstance(sim, MMC):
                for pos, job in enumerate(sim.queue):
                    targets[job.id] = (x_queue_start + pos*x_queue_step, yq)
                for si, s in enumerate(sim.servers):
                    if s.current_job:
                        sx, sy = self.server_positions[idx][si]
                        targets[s.current_job.id] = (sx, sy)
        elif sp.kind == 'mmk1':
            if isinstance(sim, MMK1):
                for qi, q in enumerate(sim.queues):
                    yq = 2.0 + qi*1.2
                    for pos, job in enumerate(q):
                        targets[job.id] = (x_queue_start + pos*x_queue_step, yq)
                for si, s in enumerate(sim.servers):
                    if s.current_job:
                        sx, sy = self.server_positions[idx][si]
                        targets[s.current_job.id] = (sx, sy)
        else:  # mmkc
            if isinstance(sim, MMKC):
                k = sp.params['k']
                c = sp.params['c']
                for qi, q in enumerate(sim.queues):
                    yq = 2.0 + qi*1.2
                    for pos, job in enumerate(q):
                        targets[job.id] = (x_queue_start + pos*x_queue_step, yq)
                for qi in range(k):
                    for si in range(c):
                        s = sim.servers[qi][si]
                        if s.current_job:
                            # Mapeo de posición en lista linearizada
                            idx_lin = qi*c + si
                            sx, sy = self.server_positions[idx][idx_lin]
                            targets[s.current_job.id] = (sx, sy)
        return targets

    def _init_anim(self):
        return self.texts

    def _update_anim(self, frame_idx: int):
        frame_t = frame_idx * self.dt
        for i in range(len(self.sims)):
            self._update_panel(i, frame_t)
        artists = []
        # Incluir sprites de clientes
        for sprite_map in self.client_sprites:
            for spr in sprite_map.values():
                head, body = spr['artist']
                artists.append(head)
                artists.append(body)
        # También podemos devolver artistas de servidores (opcional)
        for s_list in self.server_artists:
            for head, body in s_list:
                artists.append(head)
                artists.append(body)
        # Nodos de llegada
        for arr_list in self.arrival_nodes:
            for dot in arr_list:
                artists.append(dot)
        return self.texts + artists

    def run(self, dt: float = 0.2, frames: int = 400, interval_ms: int = 100):
        self.dt = dt
        self.anim = animation.FuncAnimation(
            self.fig,
            self._update_anim,
            init_func=self._init_anim,
            frames=frames,
            interval=interval_ms,
            blit=False,
            repeat=False,
        )
        plt.tight_layout()
        plt.show()

# -----------------------------
# Punto de entrada
# -----------------------------

if __name__ == '__main__':
    # Parámetros por defecto (estables)
    specs = [
        ModelSpec('M/M/1', 'mm1',  {'lam': 2.0, 'mu': 3.0}),
        ModelSpec('M/M/c', 'mmc',  {'lam': 5.0, 'mu': 3.0, 'c': 3}),
        ModelSpec('M/M/k/1', 'mmk1', {'lam': 6.0, 'mu': 4.0, 'k': 3}),
        ModelSpec('M/M/k/c', 'mmkc', {'lam': 8.0, 'mu': 4.0, 'k': 2, 'c': 2}),
    ]
    anim = AnimatedComparison(specs, horizon=120.0, seed=42)
    anim.run(dt=0.2, frames=500, interval_ms=100)
