/**
 * METRICS MANAGER - Gestor de Métricas en Tiempo Real
 */

export class MetricsManager {
    constructor() {
        this.currentMetrics = null;
    }

    async init() {
        console.log('Inicializando MetricsManager...');
    }

    reset() {
        this.currentMetrics = null;
        this.updateDisplay({ rho: 0, L: 0, Lq: 0, W: 0, Wq: 0 });
    }

    update(simState) {
        this.currentMetrics = simState.metrics;
        this.updateDisplay(simState.metrics);
        this.updateLiveOverlay(simState);
        this.updateAccumulatedStats(simState);
    }

    updateDisplay(metrics) {
        const container = document.getElementById('instantMetrics');
        if (!container) return;
        
        container.innerHTML = `
            ${this.createMetricItem('ρ', 'Utilización', metrics.rho, 4)}
            ${this.createMetricItem('L', 'En Sistema', metrics.L, 3)}
            ${this.createMetricItem('Lq', 'En Cola', metrics.Lq, 3)}
            ${this.createMetricItem('W', 'Tiempo Sistema', metrics.W, 3)}
            ${this.createMetricItem('Wq', 'Tiempo Cola', metrics.Wq, 3)}
        `;
    }

    createMetricItem(symbol, label, value, decimals) {
        return `
            <div class="metric-item">
                <div>
                    <span class="metric-label">${symbol} - ${label}</span>
                </div>
                <span class="metric-value">${value.toFixed(decimals)}</span>
            </div>
        `;
    }

    updateLiveOverlay(simState) {
        const overlay = document.getElementById('liveMetricsOverlay');
        if (!overlay) return;
        
        const nSystem = simState.queue.length + simState.servers.filter(s => s.busy).length;
        const nQueue = simState.queue.length;
        
        overlay.innerHTML = `
            <div class="overlay-metric">
                <span>Tiempo:</span>
                <strong>${simState.time.toFixed(1)}</strong>
            </div>
            <div class="overlay-metric">
                <span>En Sistema:</span>
                <strong>${nSystem}</strong>
            </div>
            <div class="overlay-metric">
                <span>En Cola:</span>
                <strong>${nQueue}</strong>
            </div>
            <div class="overlay-metric">
                <span>ρ Actual:</span>
                <strong>${simState.metrics.rho.toFixed(3)}</strong>
            </div>
        `;
    }

    updateAccumulatedStats(simState) {
        const container = document.getElementById('accumulatedStats');
        if (!container) return;
        
        container.innerHTML = `
            <div class="stat-item">
                <span class="stat-value">${simState.totalServed}</span>
                <span class="stat-label">Atendidos</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">${simState.totalRejected}</span>
                <span class="stat-label">Rechazados</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">${simState.time.toFixed(1)}</span>
                <span class="stat-label">Tiempo Sim.</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">${(simState.time - simState.config.warmup).toFixed(1)}</span>
                <span class="stat-label">Tiempo Efectivo</span>
            </div>
        `;
    }
}
