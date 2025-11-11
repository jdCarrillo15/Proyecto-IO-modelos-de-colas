/**
 * CHART MANAGER - Gestor de Gráficos Interactivos
 */

export class ChartManager {
    constructor() {
        this.charts = {};
        this.currentTab = 'timeseries';
    }

    async init() {
        console.log('Inicializando ChartManager...');
        this.initializeCharts();
    }

    initializeCharts() {
        // Time Series Chart
        const tsCtx = document.getElementById('timeseriesChart');
        if (tsCtx) {
            this.charts.timeseries = new Chart(tsCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [
                        {
                            label: 'L (Sistema)',
                            data: [],
                            borderColor: '#3B82F6',
                            backgroundColor: 'rgba(59, 130, 246, 0.1)',
                            tension: 0.4
                        },
                        {
                            label: 'Lq (Cola)',
                            data: [],
                            borderColor: '#10B981',
                            backgroundColor: 'rgba(16, 185, 129, 0.1)',
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: true, position: 'top' },
                        title: { display: true, text: 'Evolución Temporal' }
                    },
                    scales: {
                        x: { title: { display: true, text: 'Tiempo' } },
                        y: { title: { display: true, text: 'Clientes' }, beginAtZero: true }
                    }
                }
            });
        }

        // Distribution Chart
        const distCtx = document.getElementById('distributionsChart');
        if (distCtx) {
            this.charts.distributions = new Chart(distCtx, {
                type: 'bar',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Frecuencia',
                        data: [],
                        backgroundColor: '#F59E0B'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        title: { display: true, text: 'Distribución de Tiempos de Espera' }
                    },
                    scales: {
                        x: { title: { display: true, text: 'Tiempo de Espera' } },
                        y: { title: { display: true, text: 'Frecuencia' }, beginAtZero: true }
                    }
                }
            });
        }
    }

    reset() {
        if (this.charts.timeseries) {
            this.charts.timeseries.data.labels = [];
            this.charts.timeseries.data.datasets.forEach(ds => ds.data = []);
            this.charts.timeseries.update();
        }
        
        if (this.charts.distributions) {
            this.charts.distributions.data.labels = [];
            this.charts.distributions.data.datasets[0].data = [];
            this.charts.distributions.update();
        }
    }

    update(simState) {
        this.updateTimeseriesChart(simState);
    }

    updateTimeseriesChart(simState) {
        const chart = this.charts.timeseries;
        if (!chart || !simState.warmupPassed) return;
        
        // Limitar a últimos 100 puntos para rendimiento
        const maxPoints = 100;
        const times = simState.timeSeries.slice(-maxPoints);
        const system = simState.systemSeries.slice(-maxPoints);
        const queue = simState.queueSeries.slice(-maxPoints);
        
        chart.data.labels = times;
        chart.data.datasets[0].data = system;
        chart.data.datasets[1].data = queue;
        chart.update('none'); // Sin animación para mejor rendimiento
    }

    showChart(chartType) {
        // Actualizar tabs
        document.querySelectorAll('.chart-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.chart === chartType);
        });
        
        // Mostrar panel correcto
        document.querySelectorAll('.chart-panel').forEach(panel => {
            panel.classList.toggle('active', panel.id === `chart${chartType.charAt(0).toUpperCase() + chartType.slice(1)}`);
        });
        
        this.currentTab = chartType;
    }

    async generateFinalCharts(results) {
        // Implementar generación de gráficos finales
        console.log('Generando gráficos finales...');
    }
}
