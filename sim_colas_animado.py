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
        # Acumuladores para tiempo de espera en cola (Wq) y en sistema (W)
        self.total_wait_q: float = 0.0
        self.count_wait_q: int = 0
        self.total_wait_sys: float = 0.0
        self.count_wait_sys: int = 0
        # Acumuladores para área bajo la curva (para L y Lq)
        self.area_in_system: float = 0.0
        self.area_in_queue: float = 0.0
        self.last_event_time: float = 0.0
        self.last_n_system: int = 0
        self.last_n_queue: int = 0
        # Series temporales para gráficos
        self.time_series: List[float] = []
        self.system_series: List[int] = []
        self.queue_series: List[int] = []
        # Series para tiempos de espera individuales
        self.wait_times: List[float] = []
        self.wait_times_q: List[float] = []
        self.departure_times: List[float] = []

    def step(self):
        raise NotImplementedError
    
    def _update_areas(self):
        """Actualizar áreas para calcular L y Lq"""
        dt = self.time - self.last_event_time
        if dt > 0:
            self.area_in_system += self.last_n_system * dt
            self.area_in_queue += self.last_n_queue * dt
        self.last_event_time = self.time
    
    def _record_state(self):
        """Registrar estado actual para series temporales"""
        st = self.state()
        self.time_series.append(self.time)
        self.system_series.append(st['in_system'])
        self.queue_series.append(st['in_queue'])

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
            'w_avg': (self.total_wait_sys / self.count_wait_sys) if self.count_wait_sys > 0 else 0.0,
            'lq_avg': (self.area_in_queue / self.time) if self.time > 0 else 0.0,
            'l_avg': (self.area_in_system / self.time) if self.time > 0 else 0.0,
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
        # Actualizar áreas antes del evento
        self.last_n_system = len(self.queue) + (1 if self.server.current_job else 0)
        self.last_n_queue = len(self.queue)
        self._update_areas()
        self._record_state()
        
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
                # Acumular tiempo en sistema
                wait_sys = job.t_departure - job.t_arrival
                wait_q = job.t_service_start - job.t_arrival if job.t_service_start else 0.0
                self.total_wait_sys += wait_sys
                self.count_wait_sys += 1
                # Registrar para gráficos
                self.departure_times.append(self.time)
                self.wait_times.append(wait_sys)
                self.wait_times_q.append(wait_q)
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
            'w_avg': (self.total_wait_sys / self.count_wait_sys) if self.count_wait_sys > 0 else 0.0,
            'lq_avg': (self.area_in_queue / self.time) if self.time > 0 else 0.0,
            'l_avg': (self.area_in_system / self.time) if self.time > 0 else 0.0,
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
        # Actualizar áreas
        busy = sum(1 for s in self.servers if s.current_job)
        self.last_n_system = len(self.queue) + busy
        self.last_n_queue = len(self.queue)
        self._update_areas()
        self._record_state()
        
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
                wait_sys = job.t_departure - job.t_arrival
                wait_q = job.t_service_start - job.t_arrival if job.t_service_start else 0.0
                self.total_wait_sys += wait_sys
                self.count_wait_sys += 1
                # Registrar para gráficos
                self.departure_times.append(self.time)
                self.wait_times.append(wait_sys)
                self.wait_times_q.append(wait_q)
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
            'w_avg': (self.total_wait_sys / self.count_wait_sys) if self.count_wait_sys > 0 else 0.0,
            'lq_avg': (self.area_in_queue / self.time) if self.time > 0 else 0.0,
            'l_avg': (self.area_in_system / self.time) if self.time > 0 else 0.0,
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
        # Actualizar áreas
        busy = sum(1 for s in self.servers if s.current_job)
        n_queue = sum(len(q) for q in self.queues)
        self.last_n_system = n_queue + busy
        self.last_n_queue = n_queue
        self._update_areas()
        self._record_state()
        
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
                wait_sys = job.t_departure - job.t_arrival
                wait_q = job.t_service_start - job.t_arrival if job.t_service_start else 0.0
                self.total_wait_sys += wait_sys
                self.count_wait_sys += 1
                # Registrar para gráficos
                self.departure_times.append(self.time)
                self.wait_times.append(wait_sys)
                self.wait_times_q.append(wait_q)
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
            'w_avg': (self.total_wait_sys / self.count_wait_sys) if self.count_wait_sys > 0 else 0.0,
            'lq_avg': (self.area_in_queue / self.time) if self.time > 0 else 0.0,
            'l_avg': (self.area_in_system / self.time) if self.time > 0 else 0.0,
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
        # Actualizar áreas
        busy = sum(1 for col in self.servers for s in col if s.current_job)
        n_queue = sum(len(q) for q in self.queues)
        self.last_n_system = n_queue + busy
        self.last_n_queue = n_queue
        self._update_areas()
        self._record_state()
        
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
                wait_sys = job.t_departure - job.t_arrival
                wait_q = job.t_service_start - job.t_arrival if job.t_service_start else 0.0
                self.total_wait_sys += wait_sys
                self.count_wait_sys += 1
                # Registrar para gráficos
                self.departure_times.append(self.time)
                self.wait_times.append(wait_sys)
                self.wait_times_q.append(wait_q)
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
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_aspect('equal')
            txt = ax.text(0.02, 0.98, '', transform=ax.transAxes, va='top', fontsize=10,
                           bbox=dict(facecolor='white', alpha=0.8))
            self.texts.append(txt)

            # Topología tipo red: Nodo de llegada -> Cola -> Servidores
            # Nodo de llegada (izquierda)
            x_arrival = 1.5
            y_center = 5.0
            
            # Nodo de cola (centro)
            x_queue = 5.0
            
            # Servidores (derecha)
            x_servers = 8.5
            
            # Dibujar nodo de llegada (círculo grande)
            arrival_node = Circle((x_arrival, y_center), radius=0.4, 
                                 facecolor='lightblue', edgecolor='black', lw=2)
            ax.add_patch(arrival_node)
            ax.text(x_arrival, y_center-0.8, 'Llegadas', ha='center', fontsize=8)
            
            # Dibujar nodo de cola (rectángulo)
            from matplotlib.patches import Rectangle, FancyBboxPatch
            queue_node = FancyBboxPatch((x_queue-0.5, y_center-0.4), 1.0, 0.8,
                                       boxstyle="round,pad=0.1", 
                                       facecolor='lightyellow', edgecolor='black', lw=2)
            ax.add_patch(queue_node)
            ax.text(x_queue, y_center, 'Cola', ha='center', va='center', fontsize=8)
            
            # Línea de llegada a cola
            line1 = Line2D([x_arrival+0.4, x_queue-0.5], [y_center, y_center], 
                          color='black', lw=2, marker='>', markersize=8, markevery=[1])
            ax.add_line(line1)
            
            # Configurar servidores según modelo
            positions: List[Tuple[float, float]] = []
            if sp.kind == 'mm1':
                positions = [(x_servers, y_center)]
            elif sp.kind == 'mmc':
                c = sp.params['c']
                y_start = y_center - (c-1)*0.6
                positions = [(x_servers, y_start + i*1.2) for i in range(c)]
            elif sp.kind == 'mmk1':
                k = sp.params['k']
                y_start = y_center - (k-1)*0.6
                positions = [(x_servers, y_start + i*1.2) for i in range(k)]
            else:  # mmkc
                k = sp.params['k']
                c = sp.params['c']
                total = k * c
                y_start = y_center - (total-1)*0.4
                for idx in range(total):
                    positions.append((x_servers, y_start + idx*0.8))
            
            self.server_positions[i] = positions
            
            # Dibujar servidores como nodos con icono
            s_artists: List[Tuple[Circle, Line2D]] = []
            for idx, (sx, sy) in enumerate(positions):
                # Nodo servidor (círculo)
                server_circle = Circle((sx, sy), radius=0.35, 
                                      facecolor=self.colors[i], edgecolor='black', lw=2, alpha=0.7)
                ax.add_patch(server_circle)
                # Icono de servidor (rectángulo pequeño dentro)
                server_icon = Rectangle((sx-0.15, sy-0.1), 0.3, 0.2, 
                                       facecolor='white', edgecolor='black', lw=1)
                ax.add_patch(server_icon)
                ax.text(sx, sy-0.6, f'S{idx+1}', ha='center', fontsize=7)
                s_artists.append((server_circle, server_icon))
                
                # Línea de cola a servidor
                line_to_server = Line2D([x_queue+0.5, sx-0.35], [y_center, sy],
                                       color='gray', lw=1.5, linestyle='--', alpha=0.6)
                ax.add_line(line_to_server)
            
            self.server_artists[i] = s_artists
            self.arrival_nodes[i] = [arrival_node]

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
            sprite = self._ensure_client_sprite(idx, jid, x=1.5, y=5.0)
            # Movimiento suave hacia el objetivo (interpolación)
            cx, cy = sprite['x'], sprite['y']
            alpha = 0.25  # Velocidad de movimiento
            nx = cx + alpha*(tx - cx)
            ny = cy + alpha*(ty - cy)
            self._place_client_sprite(sprite, nx, ny)
        # Remover sprites de jobs completados
        self._remove_missing_client_sprites(idx, alive_ids)

    # Nuevas utilidades para representar estado detallado
    def _ensure_client_sprite(self, panel_idx: int, job_id: int, x: float, y: float):
        dct = self.client_sprites[panel_idx]
        if job_id not in dct:
            # Cliente como círculo pequeño (paquete/usuario)
            client_circle = Circle((x, y), radius=0.15, facecolor='red', 
                                  edgecolor='darkred', lw=1.5, alpha=0.9)
            ax = self.axes[panel_idx]
            ax.add_patch(client_circle)
            dct[job_id] = {'artist': client_circle, 'x': x, 'y': y}
        return dct[job_id]

    def _place_client_sprite(self, sprite: Dict, x: float, y: float):
        client_circle = sprite['artist']
        client_circle.center = (x, y)
        sprite['x'] = x
        sprite['y'] = y

    def _remove_missing_client_sprites(self, panel_idx: int, alive_ids: set):
        dct = self.client_sprites[panel_idx]
        remove_ids = [jid for jid in dct.keys() if jid not in alive_ids]
        for jid in remove_ids:
            client_circle = dct[jid]['artist']
            client_circle.remove()
            del dct[jid]

    def _layout_targets(self, idx: int) -> Dict[int, Tuple[float, float]]:
        sp = self.specs[idx]
        sim = self.sims[idx]
        targets: Dict[int, Tuple[float, float]] = {}
        
        # Posiciones de nodos en topología
        x_arrival = 1.5
        x_queue = 5.0
        y_center = 5.0
        
        # Posición en cola: apilados verticalmente cerca del nodo de cola
        queue_x_offset = 3.5
        queue_y_start = y_center + 1.0
        queue_y_step = 0.3
        
        if sp.kind == 'mm1':
            if isinstance(sim, MM1):
                # Clientes en cola
                for pos, job in enumerate(sim.queue):
                    targets[job.id] = (queue_x_offset, queue_y_start + pos*queue_y_step)
                # Cliente en servicio
                if sim.server.current_job:
                    job = sim.server.current_job
                    sx, sy = self.server_positions[idx][0]
                    targets[job.id] = (sx, sy)
        elif sp.kind == 'mmc':
            if isinstance(sim, MMC):
                # Clientes en cola
                for pos, job in enumerate(sim.queue):
                    targets[job.id] = (queue_x_offset, queue_y_start + pos*queue_y_step)
                # Clientes en servicio
                for si, s in enumerate(sim.servers):
                    if s.current_job:
                        sx, sy = self.server_positions[idx][si]
                        targets[s.current_job.id] = (sx, sy)
        elif sp.kind == 'mmk1':
            if isinstance(sim, MMK1):
                # Múltiples colas
                for qi, q in enumerate(sim.queues):
                    for pos, job in enumerate(q):
                        y_offset = queue_y_start + qi*1.5
                        targets[job.id] = (queue_x_offset, y_offset + pos*queue_y_step)
                # Clientes en servicio
                for si, s in enumerate(sim.servers):
                    if s.current_job:
                        sx, sy = self.server_positions[idx][si]
                        targets[s.current_job.id] = (sx, sy)
        else:  # mmkc
            if isinstance(sim, MMKC):
                k = sp.params['k']
                c = sp.params['c']
                # Múltiples colas
                for qi, q in enumerate(sim.queues):
                    for pos, job in enumerate(q):
                        y_offset = queue_y_start + qi*1.5
                        targets[job.id] = (queue_x_offset, y_offset + pos*queue_y_step)
                # Clientes en servicio
                for qi in range(k):
                    for si in range(c):
                        s = sim.servers[qi][si]
                        if s.current_job:
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
                client_circle = spr['artist']
                artists.append(client_circle)
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
        
        # Generar reporte post-simulación
        self._generate_report()
    
    def _generate_report(self):
        """Generar reporte de métricas post-simulación"""
        print("\n" + "="*80)
        print("REPORTE DE MÉTRICAS POST-SIMULACIÓN")
        print("="*80)
        print(f"Horizonte de simulación: {self.horizon:.2f} unidades de tiempo\n")
        
        # Tabla comparativa
        print(f"{'Modelo':<15} {'λ':<8} {'μ':<8} {'c/k':<8} {'ρ':<8} {'Wq':<10} {'W':<10} {'Lq':<10} {'L':<10} {'Atendidos':<12}")
        print("-"*110)
        
        for i, (spec, sim) in enumerate(zip(self.specs, self.sims)):
            # Completar simulación hasta el horizonte
            while sim.time < sim.horizon:
                sim.step()
            
            st = sim.state()
            p = spec.params
            
            # Formatear parámetros según modelo
            if spec.kind == 'mm1':
                ck_str = "-"
            elif spec.kind == 'mmc':
                ck_str = f"c={p['c']}"
            elif spec.kind == 'mmk1':
                ck_str = f"k={p['k']}"
            else:  # mmkc
                ck_str = f"k={p['k']},c={p['c']}"
            
            print(f"{spec.name:<15} {p['lam']:<8.2f} {p['mu']:<8.2f} {ck_str:<8} "
                  f"{st['rho']:<8.3f} {st['wq_avg']:<10.3f} {st['w_avg']:<10.3f} "
                  f"{st['lq_avg']:<10.3f} {st['l_avg']:<10.3f} {st['served']:<12}")
        
        print("\n" + "="*80)
        print("LEYENDA:")
        print("  λ  = Tasa de llegadas (clientes/tiempo)")
        print("  μ  = Tasa de servicio (clientes/tiempo)")
        print("  c  = Número de servidores")
        print("  k  = Número de colas")
        print("  ρ  = Utilización del sistema")
        print("  Wq = Tiempo promedio de espera en cola")
        print("  W  = Tiempo promedio en el sistema")
        print("  Lq = Número promedio de clientes en cola")
        print("  L  = Número promedio de clientes en el sistema")
        print("="*80 + "\n")
        
        # Generar gráfico de series temporales
        self._plot_time_series()
    
    def _plot_time_series(self):
        """Generar gráfico de tiempo en el sistema vs tiempo de simulación"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        axes = axes.flatten()
        
        for i, (spec, sim, ax) in enumerate(zip(self.specs, self.sims, axes)):
            p = spec.params
            
            if not sim.departure_times:
                # Si no hay datos, mostrar mensaje
                ax.text(0.5, 0.5, 'Sin datos suficientes', 
                       transform=ax.transAxes, ha='center', va='center')
                ax.set_title(f"{spec.name}", fontsize=13, fontweight='bold', pad=10)
                continue
            
            # Usar datos de tiempos de espera
            departure_times = sim.departure_times
            wait_times = sim.wait_times
            wait_times_q = sim.wait_times_q
            
            # Submuestrear si hay demasiados puntos
            sample_rate = max(1, len(departure_times) // 500)
            dep_times = departure_times[::sample_rate]
            w_times = wait_times[::sample_rate]
            wq_times = wait_times_q[::sample_rate]
            
            # Graficar tiempos de espera con líneas conectadas
            ax.plot(dep_times, w_times, 'b-', linewidth=2, alpha=0.7, 
                   label='Tiempo en sistema (W)', marker='o', markersize=4, markevery=max(1, len(dep_times)//50))
            ax.plot(dep_times, wq_times, 'r--', linewidth=2, alpha=0.7, 
                   label='Tiempo en cola (Wq)', marker='s', markersize=3, markevery=max(1, len(dep_times)//50))
            
            # Calcular límites dinámicos del eje Y
            max_val = max(max(w_times) if w_times else 1, 
                         max(wq_times) if wq_times else 1)
            ax.set_ylim(-0.05, max_val * 1.15)
            
            # Configurar ejes
            ax.set_xlabel('Tiempo de simulación (unidades)', fontsize=11, fontweight='bold')
            ax.set_ylabel('Tiempo de espera (unidades)', fontsize=11, fontweight='bold')
            ax.set_title(f"{spec.name}", fontsize=13, fontweight='bold', pad=10)
            ax.grid(True, alpha=0.4, linestyle='--', linewidth=0.5)
            ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
            
            # Agregar información de parámetros y métricas
            if spec.kind == 'mm1':
                param_text = f"λ={p['lam']:.1f}, μ={p['mu']:.1f}"
            elif spec.kind == 'mmc':
                param_text = f"λ={p['lam']:.1f}, μ={p['mu']:.1f}, c={p['c']}"
            elif spec.kind == 'mmk1':
                param_text = f"λ={p['lam']:.1f}, μ={p['mu']:.1f}, k={p['k']}"
            else:  # mmkc
                param_text = f"λ={p['lam']:.1f}, μ={p['mu']:.1f}, k={p['k']}, c={p['c']}"
            
            st = sim.state()
            stats_text = (f"{param_text}\n"
                         f"ρ={st['rho']:.3f}\n"
                         f"W̄={st['w_avg']:.3f}, W̄q={st['wq_avg']:.3f}\n"
                         f"L̄={st['l_avg']:.2f}, L̄q={st['lq_avg']:.2f}\n"
                         f"Clientes: {st['served']}")
            
            ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
                   fontsize=9, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='lightyellow', 
                            edgecolor='gray', alpha=0.9, pad=0.5),
                   family='monospace')
            
            # Añadir línea horizontal para promedio de tiempo en sistema
            ax.axhline(y=st['w_avg'], color='blue', linestyle=':', 
                      linewidth=2, alpha=0.6, label=f"W̄ promedio")
            # Añadir línea horizontal para promedio de tiempo en cola
            ax.axhline(y=st['wq_avg'], color='red', linestyle=':', 
                      linewidth=2, alpha=0.6, label=f"W̄q promedio")
        
        plt.suptitle('Evolución Temporal: Tiempo en Sistema por Cliente', 
                    fontsize=15, fontweight='bold', y=0.995)
        plt.tight_layout()
        plt.show()

# -----------------------------
# Punto de entrada
# -----------------------------

if __name__ == '__main__':
    # Parámetros por defecto (estables, con frecuencias reducidas para mejor observación)
    specs = [
        ModelSpec('M/M/1', 'mm1',  {'lam': 0.6, 'mu': 2.0}),
        ModelSpec('M/M/c', 'mmc',  {'lam': 0.7, 'mu': 2.5, 'c': 3}),
        ModelSpec('M/M/k/1', 'mmk1', {'lam': 0.8, 'mu': 2.5, 'k': 3}),
        ModelSpec('M/M/k/c', 'mmkc', {'lam': 0.9, 'mu': 2.5, 'k': 2, 'c': 2}),
    ]
    anim = AnimatedComparison(specs, horizon=120.0, seed=42)
    anim.run(dt=0.2, frames=500, interval_ms=100)
