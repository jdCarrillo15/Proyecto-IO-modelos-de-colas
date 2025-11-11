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
        // Configuración común para mejorar legibilidad
        const commonFontConfig = {
            size: 14,
            weight: '500',
            family: "'Inter', sans-serif"
        };

        const titleFontConfig = {
            size: 16,
            weight: '600',
            family: "'Inter', sans-serif"
        };

        // Time Series Chart
        const tsCtx = document.getElementById('timeseriesChart');
        if (tsCtx) {
            this.charts.timeseries = new Chart(tsCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [
                        {
                            label: 'L (Clientes en Sistema)',
                            data: [],
                            borderColor: '#3B82F6',
                            backgroundColor: 'rgba(59, 130, 246, 0.15)',
                            borderWidth: 3,
                            tension: 0.4,
                            pointRadius: 0,
                            pointHoverRadius: 5
                        },
                        {
                            label: 'Lq (Clientes en Cola)',
                            data: [],
                            borderColor: '#10B981',
                            backgroundColor: 'rgba(16, 185, 129, 0.15)',
                            borderWidth: 3,
                            tension: 0.4,
                            pointRadius: 0,
                            pointHoverRadius: 5
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {
                        mode: 'index',
                        intersect: false
                    },
                    plugins: {
                        legend: { 
                            display: true, 
                            position: 'top',
                            labels: {
                                font: commonFontConfig,
                                padding: 15,
                                usePointStyle: true,
                                pointStyle: 'circle'
                            }
                        },
                        title: { 
                            display: true, 
                            text: '📈 Evolución Temporal del Sistema',
                            font: titleFontConfig,
                            padding: 20
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleFont: commonFontConfig,
                            bodyFont: commonFontConfig,
                            padding: 12,
                            cornerRadius: 8
                        }
                    },
                    scales: {
                        x: { 
                            title: { 
                                display: true, 
                                text: 'Tiempo (unidades)',
                                font: commonFontConfig,
                                padding: 10
                            },
                            ticks: {
                                font: commonFontConfig
                            },
                            grid: {
                                color: 'rgba(100, 116, 139, 0.2)'
                            }
                        },
                        y: { 
                            title: { 
                                display: true, 
                                text: 'Número de Clientes',
                                font: commonFontConfig,
                                padding: 10
                            },
                            beginAtZero: true,
                            ticks: {
                                font: commonFontConfig,
                                precision: 0
                            },
                            grid: {
                                color: 'rgba(100, 116, 139, 0.2)'
                            }
                        }
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
                        backgroundColor: '#F59E0B',
                        borderColor: '#D97706',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { 
                            display: true,
                            labels: {
                                font: commonFontConfig
                            }
                        },
                        title: { 
                            display: true, 
                            text: '📊 Distribución de Tiempos de Espera',
                            font: titleFontConfig,
                            padding: 20
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleFont: commonFontConfig,
                            bodyFont: commonFontConfig,
                            padding: 12,
                            cornerRadius: 8
                        }
                    },
                    scales: {
                        x: { 
                            title: { 
                                display: true, 
                                text: 'Intervalo de Tiempo',
                                font: commonFontConfig,
                                padding: 10
                            },
                            ticks: {
                                font: commonFontConfig
                            },
                            grid: {
                                display: false
                            }
                        },
                        y: { 
                            title: { 
                                display: true, 
                                text: 'Frecuencia',
                                font: commonFontConfig,
                                padding: 10
                            },
                            beginAtZero: true,
                            ticks: {
                                font: commonFontConfig,
                                precision: 0
                            },
                            grid: {
                                color: 'rgba(100, 116, 139, 0.2)'
                            }
                        }
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
        this.updateDistributionChart(simState);
    }
    
    updateDistributionChart(simState) {
        const chart = this.charts.distributions;
        if (!chart || !simState.warmupPassed) return;
        
        // Actualizar solo cada 30 frames
        if (!this.distUpdateCounter) this.distUpdateCounter = 0;
        this.distUpdateCounter++;
        
        if (this.distUpdateCounter % 30 !== 0) return;
        
        // Calcular distribución de tiempos de espera
        if (simState.completedJobs && simState.completedJobs.length > 10) {
            const waitTimes = simState.completedJobs
                .map(job => job.startTime - job.arrivalTime)
                .filter(t => t >= 0);
            
            if (waitTimes.length > 0) {
                const numBins = 8;
                const maxTime = Math.max(...waitTimes);
                const binSize = maxTime / numBins;
                const bins = Array(numBins).fill(0);
                const binLabels = [];
                
                for (let i = 0; i < numBins; i++) {
                    binLabels.push(`${(i * binSize).toFixed(1)}`);
                }
                
                waitTimes.forEach(time => {
                    const binIndex = Math.min(Math.floor(time / binSize), numBins - 1);
                    bins[binIndex]++;
                });
                
                chart.data.labels = binLabels;
                chart.data.datasets[0].data = bins;
                chart.update('none');
            }
        }
    }

    updateTimeseriesChart(simState) {
        const chart = this.charts.timeseries;
        if (!chart || !simState.warmupPassed) return;
        
        // Actualizar solo cada 10 frames para mejor rendimiento
        if (!this.updateCounter) this.updateCounter = 0;
        this.updateCounter++;
        
        if (this.updateCounter % 10 !== 0) return;
        
        // Limitar a últimos 100 puntos para rendimiento
        const maxPoints = 100;
        const times = simState.timeSeries.slice(-maxPoints);
        const system = simState.systemSeries.slice(-maxPoints);
        const queue = simState.queueSeries.slice(-maxPoints);
        
        chart.data.labels = times.map(t => t.toFixed(1));
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
        console.log('Generando gráficos finales...');
        
        // Esperar a que el DOM se actualice
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // Gráfica de series temporales
        const tsCanvas = document.getElementById('finalTimeseriesChart');
        if (tsCanvas && results.timeSeries && results.timeSeries.length > 0) {
            const tsChart = new Chart(tsCanvas, {
                type: 'line',
                data: {
                    labels: results.timeSeries.map(t => t.toFixed(1)),
                    datasets: [
                        {
                            label: 'Clientes en Sistema (L)',
                            data: results.systemSeries,
                            borderColor: '#3B82F6',
                            backgroundColor: 'rgba(59, 130, 246, 0.1)',
                            borderWidth: 2,
                            tension: 0.4
                        },
                        {
                            label: 'Clientes en Cola (Lq)',
                            data: results.queueSeries,
                            borderColor: '#10B981',
                            backgroundColor: 'rgba(16, 185, 129, 0.1)',
                            borderWidth: 2,
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    aspectRatio: 2,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: { font: { size: 12 } }
                        },
                        title: {
                            display: true,
                            text: 'Evolución Temporal del Sistema',
                            font: { size: 14, weight: 'bold' }
                        }
                    },
                    scales: {
                        x: {
                            title: { display: true, text: 'Tiempo' },
                            ticks: { maxTicksLimit: 10 }
                        },
                        y: {
                            title: { display: true, text: 'Clientes' },
                            beginAtZero: true
                        }
                    }
                }
            });
        }
        
        // Gráfica de distribución de tiempos de espera
        const distCanvas = document.getElementById('finalDistributionChart');
        if (distCanvas && results.completedJobs && results.completedJobs.length > 0) {
            // Calcular distribución de tiempos de espera
            const waitTimes = results.completedJobs.map(job => 
                job.startTime - job.arrivalTime
            ).filter(t => t >= 0);
            
            // Crear histograma
            const numBins = 10;
            const maxTime = Math.max(...waitTimes);
            const binSize = maxTime / numBins;
            const bins = Array(numBins).fill(0);
            const binLabels = [];
            
            for (let i = 0; i < numBins; i++) {
                binLabels.push(`${(i * binSize).toFixed(1)}-${((i + 1) * binSize).toFixed(1)}`);
            }
            
            waitTimes.forEach(time => {
                const binIndex = Math.min(Math.floor(time / binSize), numBins - 1);
                bins[binIndex]++;
            });
            
            const distChart = new Chart(distCanvas, {
                type: 'bar',
                data: {
                    labels: binLabels,
                    datasets: [{
                        label: 'Frecuencia',
                        data: bins,
                        backgroundColor: '#F59E0B',
                        borderColor: '#D97706',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    aspectRatio: 2,
                    plugins: {
                        legend: { display: false },
                        title: {
                            display: true,
                            text: 'Distribución de Tiempos de Espera',
                            font: { size: 14, weight: 'bold' }
                        }
                    },
                    scales: {
                        x: {
                            title: { display: true, text: 'Intervalo de Tiempo de Espera' }
                        },
                        y: {
                            title: { display: true, text: 'Frecuencia' },
                            beginAtZero: true,
                            ticks: { precision: 0 }
                        }
                    }
                }
            });
        }
    }
}
