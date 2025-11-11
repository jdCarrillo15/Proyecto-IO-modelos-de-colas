/**
 * SISTEMA DE SIMULACIÓN DE COLAS - MÓDULO PRINCIPAL
 * 
 * Punto de entrada de la aplicación web interactiva
 */

import { ConfigManager } from './modules/config.js';
import { SimulationEngine } from './modules/simulation-engine.js';
import { VisualizationManager } from './modules/visualization.js';
import { MetricsManager } from './modules/metrics.js';
import { ChartManager } from './modules/charts.js';
import { UIManager } from './modules/ui.js';
import { ExportManager } from './modules/export.js';
import { TutorialManager } from './modules/tutorial.js';

class QueueSimulationApp {
    constructor() {
        this.config = new ConfigManager();
        this.simulation = new SimulationEngine();
        this.visualization = new VisualizationManager();
        this.metrics = new MetricsManager();
        this.charts = new ChartManager();
        this.ui = new UIManager();
        this.export = new ExportManager();
        this.tutorial = new TutorialManager();
        
        this.isRunning = false;
        this.isPaused = false;
        this.animationFrameId = null;
    }

    async init() {
        console.log('🚀 Iniciando Sistema de Simulación de Colas...');
        
        try {
            // Inicializar módulos
            await this.config.init();
            await this.visualization.init();
            await this.metrics.init();
            await this.charts.init();
            await this.ui.init();
            
            // Configurar event listeners
            this.setupEventListeners();
            
            // Cargar configuración por defecto
            this.config.loadDefaultConfig();
            
            console.log('✅ Aplicación iniciada correctamente');
            this.ui.showToast('Aplicación cargada correctamente', 'success');
            
        } catch (error) {
            console.error('❌ Error al iniciar aplicación:', error);
            this.ui.showToast('Error al iniciar la aplicación', 'error');
        }
    }

    setupEventListeners() {
        // Botones de acción
        document.getElementById('runSimulation')?.addEventListener('click', () => this.runSimulation());
        document.getElementById('pauseSimulation')?.addEventListener('click', () => this.togglePause());
        document.getElementById('resetSimulation')?.addEventListener('click', () => this.resetSimulation());
        document.getElementById('exportResults')?.addEventListener('click', () => this.exportResults());
        
        // Controles de tema y ayuda
        document.getElementById('toggleTheme')?.addEventListener('click', () => this.ui.toggleTheme());
        document.getElementById('toggleTutorial')?.addEventListener('click', () => this.tutorial.show());
        document.getElementById('showHelp')?.addEventListener('click', () => this.showHelp());
        
        // Velocidad de animación
        document.getElementById('animationSpeed')?.addEventListener('change', (e) => {
            this.simulation.setSpeed(parseFloat(e.target.value));
        });
        
        // Cambio de modelo
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const model = e.target.dataset.model;
                this.config.selectModel(model);
                this.updateUI();
            });
        });
        
        // Tabs de gráficos
        document.querySelectorAll('.chart-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                const chartType = e.target.dataset.chart;
                this.charts.showChart(chartType);
            });
        });
    }

    async runSimulation() {
        if (this.isRunning) {
            this.ui.showToast('Ya hay una simulación en ejecución', 'warning');
            return;
        }

        // Obtener configuración actual
        const config = this.config.getCurrentConfig();
        
        // Validar configuración
        const validation = this.config.validate(config);
        if (!validation.valid) {
            this.ui.showToast(validation.message, 'error');
            return;
        }

        // Advertencia si el sistema es inestable
        if (validation.unstable) {
            const proceed = await this.ui.showConfirm(
                '⚠️ Sistema Inestable',
                'El sistema tiene ρ ≥ 1 y puede no alcanzar estado estacionario. ¿Deseas continuar?'
            );
            if (!proceed) return;
        }

        try {
            this.isRunning = true;
            this.isPaused = false;
            
            // Actualizar UI
            this.ui.setSimulationRunning(true);
            this.ui.showLoading('Iniciando simulación...');
            
            // Inicializar simulación
            await this.simulation.initialize(config);
            
            // Reiniciar visualización y métricas
            this.visualization.reset();
            this.metrics.reset();
            this.charts.reset();
            
            this.ui.hideLoading();
            
            // Iniciar loop de animación
            this.startAnimationLoop();
            
            this.ui.showToast('Simulación iniciada', 'success');
            
        } catch (error) {
            console.error('Error al ejecutar simulación:', error);
            this.ui.showToast(`Error: ${error.message}`, 'error');
            this.isRunning = false;
            this.ui.setSimulationRunning(false);
            this.ui.hideLoading();
        }
    }

    startAnimationLoop() {
        const animate = (timestamp) => {
            if (!this.isRunning) return;
            
            if (!this.isPaused) {
                // Ejecutar paso de simulación
                const simState = this.simulation.step();
                
                // Actualizar visualización
                this.visualization.update(simState);
                
                // Actualizar métricas
                this.metrics.update(simState);
                
                // Actualizar gráficos
                this.charts.update(simState);
                
                // Actualizar progreso
                const progress = (simState.time / simState.config.horizon) * 100;
                this.ui.updateProgress(progress, simState.time, simState.config.horizon);
                
                // Verificar si la simulación terminó
                if (simState.finished) {
                    this.finishSimulation(simState);
                    return;
                }
            }
            
            this.animationFrameId = requestAnimationFrame(animate);
        };
        
        this.animationFrameId = requestAnimationFrame(animate);
    }

    togglePause() {
        this.isPaused = !this.isPaused;
        const btn = document.getElementById('pauseSimulation');
        if (this.isPaused) {
            btn.innerHTML = '<span class="btn-icon">⏯</span> Reanudar';
            this.ui.showToast('Simulación pausada', 'info');
        } else {
            btn.innerHTML = '<span class="btn-icon">⏸</span> Pausar';
            this.ui.showToast('Simulación reanudada', 'info');
        }
    }

    resetSimulation() {
        // Cancelar animación
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
        }
        
        this.isRunning = false;
        this.isPaused = false;
        
        // Reiniciar módulos
        this.simulation.reset();
        this.visualization.reset();
        this.metrics.reset();
        this.charts.reset();
        
        // Actualizar UI
        this.ui.setSimulationRunning(false);
        this.ui.updateProgress(0, 0, 0);
        
        this.ui.showToast('Simulación reiniciada', 'info');
    }

    async finishSimulation(finalState) {
        this.isRunning = false;
        this.ui.setSimulationRunning(false);
        
        console.log('✅ Simulación completada');
        
        // Guardar resultados
        this.lastResults = finalState;
        
        // Habilitar exportación
        document.getElementById('exportResults').disabled = false;
        
        // Mostrar modal de resultados
        await this.showResults(finalState);
        
        this.ui.showToast('Simulación completada exitosamente', 'success');
    }

    async showResults(results) {
        const modal = document.getElementById('resultsModal');
        const content = document.getElementById('resultsContent');
        
        // Generar contenido de resultados
        content.innerHTML = this.generateResultsHTML(results);
        
        // Generar gráficos finales
        await this.charts.generateFinalCharts(results);
        
        // Mostrar modal
        modal.classList.add('show');
        
        // Event listeners para modal
        const closeBtn = modal.querySelector('.modal-close');
        const overlay = modal.querySelector('.modal-overlay');
        
        const closeModal = () => modal.classList.remove('show');
        
        closeBtn.onclick = closeModal;
        overlay.onclick = closeModal;
        
        // Botones de acción
        document.getElementById('downloadJSON').onclick = () => this.export.downloadJSON(results);
        document.getElementById('generateReport').onclick = () => this.export.generateReport(results);
        document.getElementById('newSimulation').onclick = () => {
            closeModal();
            this.resetSimulation();
        };
    }

    generateResultsHTML(results) {
        const metrics = results.metrics;
        const config = results.config;
        
        return `
            <div class="results-summary">
                <h3>📊 Métricas Finales</h3>
                <div class="results-grid">
                    <div class="result-card">
                        <div class="result-label">Utilización (ρ)</div>
                        <div class="result-value">${metrics.rho.toFixed(4)}</div>
                    </div>
                    <div class="result-card">
                        <div class="result-label">Clientes en Sistema (L)</div>
                        <div class="result-value">${metrics.L.toFixed(3)}</div>
                    </div>
                    <div class="result-card">
                        <div class="result-label">Clientes en Cola (Lq)</div>
                        <div class="result-value">${metrics.Lq.toFixed(3)}</div>
                    </div>
                    <div class="result-card">
                        <div class="result-label">Tiempo en Sistema (W)</div>
                        <div class="result-value">${metrics.W.toFixed(3)}</div>
                    </div>
                    <div class="result-card">
                        <div class="result-label">Tiempo en Cola (Wq)</div>
                        <div class="result-value">${metrics.Wq.toFixed(3)}</div>
                    </div>
                    <div class="result-card">
                        <div class="result-label">Clientes Atendidos</div>
                        <div class="result-value">${results.totalServed}</div>
                    </div>
                </div>
                
                ${this.generateTheoryComparison(metrics, config)}
                
                <h3>📈 Gráficos de Resultados</h3>
                <div class="final-charts">
                    <canvas id="finalTimeseriesChart"></canvas>
                    <canvas id="finalDistributionChart"></canvas>
                </div>
            </div>
        `;
    }

    generateTheoryComparison(simMetrics, config) {
        if (!config.compareWithTheory) return '';
        if (config.model !== 'mm1' && config.model !== 'mmc') return '';
        
        const theory = this.config.calculateTheory(config);
        if (!theory) return '';
        
        const calcError = (sim, theo) => Math.abs((sim - theo) / theo * 100);
        
        return `
            <div class="theory-comparison-section">
                <h3>📐 Comparación: Simulación vs Teoría</h3>
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Métrica</th>
                            <th>Simulación</th>
                            <th>Teoría</th>
                            <th>Error (%)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>L</td>
                            <td>${simMetrics.L.toFixed(4)}</td>
                            <td>${theory.L.toFixed(4)}</td>
                            <td>${calcError(simMetrics.L, theory.L).toFixed(2)}%</td>
                        </tr>
                        <tr>
                            <td>Lq</td>
                            <td>${simMetrics.Lq.toFixed(4)}</td>
                            <td>${theory.Lq.toFixed(4)}</td>
                            <td>${calcError(simMetrics.Lq, theory.Lq).toFixed(2)}%</td>
                        </tr>
                        <tr>
                            <td>W</td>
                            <td>${simMetrics.W.toFixed(4)}</td>
                            <td>${theory.W.toFixed(4)}</td>
                            <td>${calcError(simMetrics.W, theory.W).toFixed(2)}%</td>
                        </tr>
                        <tr>
                            <td>Wq</td>
                            <td>${simMetrics.Wq.toFixed(4)}</td>
                            <td>${theory.Wq.toFixed(4)}</td>
                            <td>${calcError(simMetrics.Wq, theory.Wq).toFixed(2)}%</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `;
    }

    exportResults() {
        if (!this.lastResults) {
            this.ui.showToast('No hay resultados para exportar', 'warning');
            return;
        }
        
        this.export.downloadJSON(this.lastResults);
    }

    showHelp() {
        const helpContent = `
            <h3>📚 Ayuda del Sistema</h3>
            <div class="help-section">
                <h4>Modelos Disponibles</h4>
                <ul>
                    <li><strong>M/M/1:</strong> Un servidor, capacidad infinita</li>
                    <li><strong>M/M/c:</strong> c servidores, capacidad infinita</li>
                    <li><strong>M/M/k/1:</strong> Un servidor, capacidad máxima k</li>
                    <li><strong>M/M/k/c:</strong> c servidores, capacidad máxima k</li>
                </ul>
                
                <h4>Parámetros</h4>
                <ul>
                    <li><strong>λ (Lambda):</strong> Tasa de llegadas por unidad de tiempo</li>
                    <li><strong>μ (Mu):</strong> Tasa de servicio por servidor</li>
                    <li><strong>c:</strong> Número de servidores</li>
                    <li><strong>k:</strong> Capacidad máxima del sistema</li>
                </ul>
                
                <h4>Métricas</h4>
                <ul>
                    <li><strong>ρ (Rho):</strong> Utilización del sistema</li>
                    <li><strong>L:</strong> Número promedio de clientes en el sistema</li>
                    <li><strong>Lq:</strong> Número promedio de clientes en la cola</li>
                    <li><strong>W:</strong> Tiempo promedio en el sistema</li>
                    <li><strong>Wq:</strong> Tiempo promedio en la cola</li>
                </ul>
            </div>
        `;
        
        this.ui.showModal('Ayuda', helpContent);
    }

    updateUI() {
        const config = this.config.getCurrentConfig();
        
        // Actualizar indicador de estabilidad
        this.ui.updateStabilityIndicator(config);
        
        // Mostrar/ocultar comparación con teoría
        const theoryCard = document.getElementById('theoryComparisonCard');
        if (config.compareWithTheory && (config.model === 'mm1' || config.model === 'mmc')) {
            theoryCard.style.display = 'block';
        } else {
            theoryCard.style.display = 'none';
        }
        
        // Mostrar/ocultar panel de servidores
        const serverCard = document.getElementById('serverStatusCard');
        if (config.model === 'mmc' || config.model === 'mmkc') {
            serverCard.style.display = 'block';
        } else {
            serverCard.style.display = 'none';
        }
    }
}

// Inicializar aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.app = new QueueSimulationApp();
    window.app.init();
});

// Exportar para uso global
export default QueueSimulationApp;
