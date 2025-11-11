/**
 * VISUALIZATION MANAGER - Gestor de Visualización Animada
 * 
 * Renderiza la red de colas con animaciones tipo Cisco Packet Tracer
 */

export class VisualizationManager {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.clients = [];
        this.nodes = {};
    }

    async init() {
        this.canvas = document.getElementById('networkCanvas');
        if (!this.canvas) {
            console.error('Canvas no encontrado');
            return;
        }
        
        this.ctx = this.canvas.getContext('2d');
        this.resizeCanvas();
        
        window.addEventListener('resize', () => this.resizeCanvas());
        
        this.setupNodes();
    }

    resizeCanvas() {
        const wrapper = this.canvas.parentElement;
        this.canvas.width = wrapper.clientWidth;
        this.canvas.height = Math.max(400, wrapper.clientHeight);
    }

    setupNodes() {
        const w = this.canvas.width;
        const h = this.canvas.height;
        
        this.nodes = {
            arrival: { x: w * 0.15, y: h * 0.5, radius: 40, color: '#3B82F6', label: 'Llegadas' },
            queue: { x: w * 0.5, y: h * 0.5, width: 150, height: 60, color: '#F59E0B', label: 'Cola' },
            servers: { x: w * 0.85, y: h * 0.5, radius: 35, color: '#10B981', label: 'Servidores' }
        };
    }

    reset() {
        this.clients = [];
        if (this.ctx) {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            this.draw({ queue: [], servers: [], time: 0 });
        }
    }

    update(simState) {
        this.updateClients(simState);
        this.draw(simState);
    }

    updateClients(simState) {
        // Limitar número de clientes visuales para mejor rendimiento
        const MAX_VISUAL_CLIENTS = 50;
        
        // Sincronizar clientes visuales con el estado de la simulación
        const queueIds = simState.queue.slice(0, MAX_VISUAL_CLIENTS).map(j => j.id);
        const serverIds = simState.servers.filter(s => s.busy).map(s => s.currentJob.id);
        const allIds = [...queueIds, ...serverIds];
        
        // Eliminar clientes que ya no existen
        this.clients = this.clients.filter(c => allIds.includes(c.id));
        
        // Agregar nuevos clientes (solo los primeros para evitar sobrecarga)
        queueIds.slice(0, 20).forEach((id, index) => {
            if (!this.clients.find(c => c.id === id)) {
                this.clients.push({
                    id,
                    x: this.nodes.arrival.x,
                    y: this.nodes.arrival.y,
                    targetX: this.nodes.queue.x - 50 + (index * 15),
                    targetY: this.nodes.queue.y,
                    state: 'queue',
                    progress: 0
                });
            }
        });
        
        simState.servers.forEach((server, index) => {
            if (server.busy) {
                const id = server.currentJob.id;
                let client = this.clients.find(c => c.id === id);
                
                if (!client) {
                    client = {
                        id,
                        x: this.nodes.queue.x,
                        y: this.nodes.queue.y,
                        targetX: this.nodes.servers.x,
                        targetY: this.nodes.servers.y + (index - 0.5) * 50,
                        state: 'service',
                        progress: 0
                    };
                    this.clients.push(client);
                } else if (client.state === 'queue') {
                    client.state = 'moving-to-service';
                    client.targetX = this.nodes.servers.x;
                    client.targetY = this.nodes.servers.y + (index - 0.5) * 50;
                    client.progress = 0;
                }
            }
        });
        
        // Animar movimiento
        this.clients.forEach(client => {
            if (client.x !== client.targetX || client.y !== client.targetY) {
                const dx = client.targetX - client.x;
                const dy = client.targetY - client.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                
                if (dist > 1) {
                    const speed = 3;
                    client.x += (dx / dist) * speed;
                    client.y += (dy / dist) * speed;
                    client.progress = Math.min(1, client.progress + 0.05);
                } else {
                    client.x = client.targetX;
                    client.y = client.targetY;
                    client.progress = 1;
                }
            }
        });
    }

    draw(simState) {
        const { ctx, canvas } = this;
        
        // Limpiar canvas
        ctx.fillStyle = '#1E293B';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Dibujar conexiones
        this.drawConnections();
        
        // Dibujar nodos
        this.drawArrivalNode();
        this.drawQueueNode(simState.queue);
        this.drawServerNodes(simState.servers);
        
        // Dibujar clientes
        this.drawClients();
    }

    drawConnections() {
        const { ctx } = this;
        
        ctx.strokeStyle = '#475569';
        ctx.lineWidth = 3;
        ctx.setLineDash([10, 5]);
        
        // Llegada -> Cola
        ctx.beginPath();
        ctx.moveTo(this.nodes.arrival.x + this.nodes.arrival.radius, this.nodes.arrival.y);
        ctx.lineTo(this.nodes.queue.x - this.nodes.queue.width / 2, this.nodes.queue.y);
        ctx.stroke();
        
        // Cola -> Servidores
        ctx.beginPath();
        ctx.moveTo(this.nodes.queue.x + this.nodes.queue.width / 2, this.nodes.queue.y);
        ctx.lineTo(this.nodes.servers.x - this.nodes.servers.radius, this.nodes.servers.y);
        ctx.stroke();
        
        ctx.setLineDash([]);
    }

    drawArrivalNode() {
        const { ctx } = this;
        const node = this.nodes.arrival;
        
        // Círculo
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
        ctx.fillStyle = node.color;
        ctx.fill();
        ctx.strokeStyle = '#60A5FA';
        ctx.lineWidth = 3;
        ctx.stroke();
        
        // Icono
        ctx.font = '24px sans-serif';
        ctx.fillStyle = 'white';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('🚶', node.x, node.y);
        
        // Label
        ctx.font = '14px Inter';
        ctx.fillText(node.label, node.x, node.y + node.radius + 20);
    }

    drawQueueNode(queue) {
        const { ctx } = this;
        const node = this.nodes.queue;
        
        // Rectángulo
        ctx.fillStyle = node.color;
        ctx.fillRect(
            node.x - node.width / 2,
            node.y - node.height / 2,
            node.width,
            node.height
        );
        ctx.strokeStyle = '#FBBF24';
        ctx.lineWidth = 3;
        ctx.strokeRect(
            node.x - node.width / 2,
            node.y - node.height / 2,
            node.width,
            node.height
        );
        
        // Label y contador
        ctx.fillStyle = 'white';
        ctx.font = 'bold 16px Inter';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(node.label, node.x, node.y - 15);
        
        ctx.font = 'bold 24px JetBrains Mono';
        ctx.fillText(queue.length, node.x, node.y + 10);
    }

    drawServerNodes(servers) {
        const { ctx } = this;
        const node = this.nodes.servers;
        const numServers = servers.length;
        
        // Calcular espaciado dinámico según número de servidores
        const maxSpacing = 80;
        const minSpacing = 50;
        const spacing = numServers > 5 ? minSpacing : maxSpacing;
        
        servers.forEach((server, i) => {
            const y = node.y + (i - (numServers - 1) / 2) * spacing;
            const isBusy = server.busy;
            
            // Círculo con efecto de pulsación si está ocupado
            ctx.beginPath();
            ctx.arc(node.x, y, node.radius, 0, Math.PI * 2);
            ctx.fillStyle = isBusy ? '#059669' : '#475569';
            ctx.fill();
            ctx.strokeStyle = isBusy ? '#34D399' : '#64748B';
            ctx.lineWidth = isBusy ? 4 : 3;
            ctx.stroke();
            
            // Glow effect para servidores ocupados
            if (isBusy) {
                ctx.shadowBlur = 15;
                ctx.shadowColor = '#10B981';
                ctx.beginPath();
                ctx.arc(node.x, y, node.radius, 0, Math.PI * 2);
                ctx.stroke();
                ctx.shadowBlur = 0;
            }
            
            // Icono
            ctx.font = '22px sans-serif';
            ctx.fillStyle = 'white';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(isBusy ? '⚙️' : '�', node.x, y);
            
            // Número de servidor
            ctx.font = 'bold 11px Inter';
            ctx.fillStyle = 'white';
            ctx.fillText(`S${i + 1}`, node.x, y - node.radius - 8);
            
            // Estado
            ctx.font = '11px Inter';
            ctx.fillStyle = isBusy ? '#10B981' : '#94A3B8';
            ctx.fillText(isBusy ? 'Ocupado' : 'Libre', node.x, y + node.radius + 12);
        });
        
        // Label general con contador
        const busyCount = servers.filter(s => s.busy).length;
        ctx.font = 'bold 14px Inter';
        ctx.fillStyle = 'white';
        ctx.textAlign = 'center';
        const labelY = node.y - ((numServers - 1) / 2) * spacing - 50;
        ctx.fillText(`${node.label} (${busyCount}/${numServers})`, node.x, labelY);
    }

    drawClients() {
        const { ctx } = this;
        
        this.clients.forEach(client => {
            const radius = 8;
            const hue = (client.id * 137.5) % 360;
            
            ctx.beginPath();
            ctx.arc(client.x, client.y, radius, 0, Math.PI * 2);
            ctx.fillStyle = `hsl(${hue}, 70%, 60%)`;
            ctx.fill();
            ctx.strokeStyle = `hsl(${hue}, 70%, 40%)`;
            ctx.lineWidth = 2;
            ctx.stroke();
        });
    }
}
