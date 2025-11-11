/**
 * SIMULATION ENGINE - Motor de Simulación de Colas
 * 
 * Implementa la lógica de simulación por eventos discretos
 */

export class SimulationEngine {
    constructor() {
        this.reset();
        this.speed = 1.0;
    }

    reset() {
        this.config = null;
        this.time = 0;
        this.nextArrival = 0;
        this.queue = [];
        this.servers = [];
        this.events = [];
        this.completedJobs = [];
        this.rejectedCount = 0;
        this.jobIdCounter = 0;
        
        // Métricas acumuladas
        this.totalWaitTime = 0;
        this.totalSystemTime = 0;
        this.areaInSystem = 0;
        this.areaInQueue = 0;
        this.lastEventTime = 0;
        
        // Series temporales
        this.timeSeries = [];
        this.systemSeries = [];
        this.queueSeries = [];
        
        this.warmupPassed = false;
        this.finished = false;
    }

    async initialize(config) {
        this.reset();
        this.config = config;
        
        // Inicializar servidores
        const numServers = config.model === 'mm1' || config.model === 'mmk1' ? 1 : config.c;
        this.servers = Array(numServers).fill().map(() => ({
            busy: false,
            busyUntil: 0,
            currentJob: null
        }));
        
        // Programar primera llegada
        this.nextArrival = this.exponential(config.lambda);
        this.scheduleEvent('arrival', this.nextArrival);
        
        console.log('Simulación inicializada:', {
            model: config.model,
            lambda: config.lambda,
            mu: config.mu,
            servers: this.servers.length,
            horizon: config.horizon
        });
    }

    step() {
        if (this.finished) {
            return this.getState();
        }
        
        // Avanzar tiempo basado en velocidad
        const dt = 0.016 * this.speed; // ~60 FPS base
        
        // Procesar eventos hasta el tiempo actual
        while (this.events.length > 0 && this.events[0].time <= this.time + dt) {
            const event = this.events.shift();
            this.processEvent(event);
        }
        
        this.time += dt;
        
        // Verificar si pasamos el warmup
        if (!this.warmupPassed && this.time >= this.config.warmup) {
            this.warmupPassed = true;
            this.resetMetrics();
        }
        
        // Registrar métricas
        if (this.warmupPassed && this.timeSeries.length < 1000) {
            this.recordMetrics();
        }
        
        // Verificar fin de simulación
        if (this.time >= this.config.horizon) {
            this.finished = true;
            this.finalizeMetrics();
        }
        
        return this.getState();
    }

    processEvent(event) {
        if (event.type === 'arrival') {
            this.handleArrival();
        } else if (event.type === 'departure') {
            this.handleDeparture(event.job);
        }
    }

    handleArrival() {
        // Crear nuevo trabajo
        const job = {
            id: this.jobIdCounter++,
            arrivalTime: this.time,
            serviceTime: this.exponential(this.config.mu),
            startTime: null,
            departureTime: null
        };
        
        // Verificar capacidad (para modelos con límite)
        const totalInSystem = this.queue.length + this.servers.filter(s => s.busy).length;
        const hasCapacityLimit = this.config.model === 'mmk1' || this.config.model === 'mmkc';
        const maxCapacity = this.config.k || Infinity;
        
        if (hasCapacityLimit && totalInSystem >= maxCapacity) {
            // Rechazar cliente
            this.rejectedCount++;
        } else {
            // Intentar asignar a un servidor libre
            const freeServer = this.servers.find(s => !s.busy);
            
            if (freeServer) {
                // Atender inmediatamente
                this.startService(job, freeServer);
            } else {
                // Agregar a la cola
                this.queue.push(job);
            }
        }
        
        // Programar siguiente llegada
        if (this.time < this.config.horizon) {
            this.nextArrival = this.time + this.exponential(this.config.lambda);
            this.scheduleEvent('arrival', this.nextArrival);
        }
    }

    handleDeparture(job) {
        // Liberar servidor
        const server = this.servers.find(s => s.currentJob?.id === job.id);
        if (server) {
            server.busy = false;
            server.currentJob = null;
            
            // Si hay clientes en cola, atender al siguiente
            if (this.queue.length > 0) {
                const nextJob = this.queue.shift();
                this.startService(nextJob, server);
            }
        }
        
        // Registrar trabajo completado
        job.departureTime = this.time;
        this.completedJobs.push(job);
        
        // Actualizar métricas (solo después del warmup)
        if (this.warmupPassed) {
            const waitTime = job.startTime - job.arrivalTime;
            const systemTime = job.departureTime - job.arrivalTime;
            
            this.totalWaitTime += waitTime;
            this.totalSystemTime += systemTime;
        }
    }

    startService(job, server) {
        job.startTime = this.time;
        server.busy = true;
        server.currentJob = job;
        
        const departureTime = this.time + job.serviceTime;
        server.busyUntil = departureTime;
        
        this.scheduleEvent('departure', departureTime, job);
    }

    scheduleEvent(type, time, job = null) {
        const event = { type, time, job };
        
        // Insertar evento en orden cronológico
        const index = this.events.findIndex(e => e.time > time);
        if (index === -1) {
            this.events.push(event);
        } else {
            this.events.splice(index, 0, event);
        }
    }

    exponential(rate) {
        const u = Math.random();
        return -Math.log(1 - u) / rate;
    }

    resetMetrics() {
        // Reiniciar acumuladores después del warmup
        this.totalWaitTime = 0;
        this.totalSystemTime = 0;
        this.areaInSystem = 0;
        this.areaInQueue = 0;
        this.lastEventTime = this.time;
        
        // Limpiar trabajos completados del warmup
        this.completedJobs = [];
        
        console.log('Periodo de warmup completado, métricas reiniciadas');
    }

    recordMetrics() {
        const nSystem = this.queue.length + this.servers.filter(s => s.busy).length;
        const nQueue = this.queue.length;
        
        // Actualizar áreas
        const dt = this.time - this.lastEventTime;
        this.areaInSystem += nSystem * dt;
        this.areaInQueue += nQueue * dt;
        this.lastEventTime = this.time;
        
        // Guardar en series temporales (submuestreo para evitar demasiados puntos)
        if (this.timeSeries.length === 0 || this.time - this.timeSeries[this.timeSeries.length - 1] > 1) {
            this.timeSeries.push(this.time);
            this.systemSeries.push(nSystem);
            this.queueSeries.push(nQueue);
        }
    }

    finalizeMetrics() {
        console.log('Simulación finalizada');
        console.log('Total de trabajos completados:', this.completedJobs.length);
        console.log('Total de trabajos rechazados:', this.rejectedCount);
    }

    calculateMetrics() {
        const effectiveTime = this.time - this.config.warmup;
        const jobsCompleted = this.completedJobs.length;
        
        if (effectiveTime <= 0 || jobsCompleted === 0) {
            return {
                rho: 0,
                L: 0,
                Lq: 0,
                W: 0,
                Wq: 0
            };
        }
        
        // Utilización
        const busyTime = this.servers.reduce((sum, s) => {
            return sum + (s.busy ? (this.time - this.config.warmup) : 0);
        }, 0);
        const rho = busyTime / (effectiveTime * this.servers.length);
        
        // Número promedio en sistema y cola
        const L = this.areaInSystem / effectiveTime;
        const Lq = this.areaInQueue / effectiveTime;
        
        // Tiempo promedio en sistema y cola
        const W = this.totalSystemTime / jobsCompleted;
        const Wq = this.totalWaitTime / jobsCompleted;
        
        return { rho, L, Lq, W, Wq };
    }

    getState() {
        return {
            time: this.time,
            config: this.config,
            queue: [...this.queue],
            servers: this.servers.map(s => ({ ...s })),
            metrics: this.calculateMetrics(),
            timeSeries: [...this.timeSeries],
            systemSeries: [...this.systemSeries],
            queueSeries: [...this.queueSeries],
            totalServed: this.completedJobs.length,
            totalRejected: this.rejectedCount,
            warmupPassed: this.warmupPassed,
            finished: this.finished,
            completedJobs: [...this.completedJobs]
        };
    }

    setSpeed(speed) {
        this.speed = speed;
        console.log('Velocidad de simulación cambiada a:', speed);
    }
}
