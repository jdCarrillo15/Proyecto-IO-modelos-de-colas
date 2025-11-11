/**
 * CONFIG MANAGER - Gestor de Configuración
 * 
 * Maneja la configuración de parámetros del modelo y validaciones
 */

export class ConfigManager {
    constructor() {
        this.currentModel = 'mm1';
        this.config = {
            lambda: 0.8,
            mu: 1.0,
            c: 1,
            k: 10,
            horizon: 1000,
            warmup: 200,
            compareWithTheory: false
        };
        
        this.modelDefinitions = {
            mm1: {
                name: 'M/M/1',
                description: 'Un servidor, capacidad infinita',
                parameters: ['lambda', 'mu', 'horizon', 'warmup', 'compareWithTheory'],
                supportsTheory: true
            },
            mmc: {
                name: 'M/M/c',
                description: 'c servidores, capacidad infinita',
                parameters: ['lambda', 'mu', 'c', 'horizon', 'warmup', 'compareWithTheory'],
                supportsTheory: true
            },
            mmk1: {
                name: 'M/M/k/1',
                description: 'Un servidor, capacidad máxima k',
                parameters: ['lambda', 'mu', 'k', 'horizon', 'warmup'],
                supportsTheory: false
            },
            mmkc: {
                name: 'M/M/k/c',
                description: 'c servidores, capacidad máxima k',
                parameters: ['lambda', 'mu', 'c', 'k', 'horizon', 'warmup'],
                supportsTheory: false
            }
        };
    }

    async init() {
        console.log('Inicializando ConfigManager...');
        this.renderParametersForm();
        this.attachEventListeners();
    }

    selectModel(modelType) {
        if (!this.modelDefinitions[modelType]) {
            console.error('Modelo desconocido:', modelType);
            return;
        }
        
        this.currentModel = modelType;
        
        // Actualizar UI de tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.model === modelType);
        });
        
        // Renderizar formulario de parámetros
        this.renderParametersForm();
        
        // Actualizar estabilidad
        this.updateStabilityIndicator();
    }

    renderParametersForm() {
        const container = document.getElementById('parametersForm');
        const model = this.modelDefinitions[this.currentModel];
        
        let html = '';
        
        // Lambda (λ)
        if (model.parameters.includes('lambda')) {
            html += this.createSliderControl(
                'lambda',
                'Tasa de Llegadas (λ)',
                this.config.lambda,
                0.1,
                10,
                0.1,
                '⬇️',
                'Número promedio de clientes que llegan por unidad de tiempo'
            );
        }
        
        // Mu (μ)
        if (model.parameters.includes('mu')) {
            html += this.createSliderControl(
                'mu',
                'Tasa de Servicio (μ)',
                this.config.mu,
                0.1,
                15,
                0.1,
                '⚡',
                'Número promedio de clientes que un servidor puede atender por unidad de tiempo'
            );
        }
        
        // c (servidores)
        if (model.parameters.includes('c')) {
            html += this.createSliderControl(
                'c',
                'Número de Servidores (c)',
                this.config.c,
                1,
                10,
                1,
                '💼',
                'Cantidad de servidores disponibles para atender clientes'
            );
        }
        
        // k (capacidad)
        if (model.parameters.includes('k')) {
            html += this.createSliderControl(
                'k',
                'Capacidad Máxima (k)',
                this.config.k,
                5,
                100,
                5,
                '📦',
                'Número máximo de clientes en el sistema (incluyendo los que están siendo atendidos)'
            );
        }
        
        // Horizonte de simulación
        if (model.parameters.includes('horizon')) {
            html += this.createSliderControl(
                'horizon',
                'Horizonte de Simulación',
                this.config.horizon,
                100,
                10000,
                100,
                '⏱️',
                'Tiempo total de la simulación'
            );
        }
        
        // Warmup
        if (model.parameters.includes('warmup')) {
            html += this.createSliderControl(
                'warmup',
                'Periodo de Warmup',
                this.config.warmup,
                0,
                2000,
                50,
                '🔥',
                'Tiempo inicial descartado para eliminar efectos transitorios'
            );
        }
        
        // Comparar con teoría
        if (model.parameters.includes('compareWithTheory') && model.supportsTheory) {
            html += this.createToggleControl(
                'compareWithTheory',
                'Comparar con Teoría',
                this.config.compareWithTheory,
                '📐',
                'Mostrar comparación entre resultados simulados y valores teóricos'
            );
        }
        
        container.innerHTML = html;
        
        // Re-attach event listeners
        this.attachParameterListeners();
    }

    createSliderControl(id, label, value, min, max, step, icon, tooltip) {
        return `
            <div class="form-group">
                <div class="slider-container">
                    <div class="slider-header">
                        <label class="form-label">
                            <span>${icon}</span>
                            ${label}
                            ${tooltip ? `<span class="tooltip-icon" title="${tooltip}">ℹ️</span>` : ''}
                        </label>
                        <span class="slider-value" id="${id}-value">${value}</span>
                    </div>
                    <input 
                        type="range" 
                        id="${id}" 
                        class="slider" 
                        min="${min}" 
                        max="${max}" 
                        step="${step}" 
                        value="${value}"
                    />
                </div>
            </div>
        `;
    }

    createToggleControl(id, label, checked, icon, tooltip) {
        return `
            <div class="form-group">
                <div class="toggle-container">
                    <label class="form-label">
                        <span>${icon}</span>
                        ${label}
                        ${tooltip ? `<span class="tooltip-icon" title="${tooltip}">ℹ️</span>` : ''}
                    </label>
                    <div class="toggle-switch">
                        <input type="checkbox" id="${id}" ${checked ? 'checked' : ''} />
                        <span class="toggle-slider"></span>
                    </div>
                </div>
            </div>
        `;
    }

    attachParameterListeners() {
        // Sliders
        const sliders = ['lambda', 'mu', 'c', 'k', 'horizon', 'warmup'];
        sliders.forEach(id => {
            const slider = document.getElementById(id);
            if (slider) {
                slider.addEventListener('input', (e) => {
                    const value = parseFloat(e.target.value);
                    this.config[id] = value;
                    document.getElementById(`${id}-value`).textContent = value;
                    this.updateStabilityIndicator();
                });
            }
        });
        
        // Toggle
        const toggle = document.getElementById('compareWithTheory');
        if (toggle) {
            toggle.addEventListener('change', (e) => {
                this.config.compareWithTheory = e.target.checked;
            });
        }
    }

    attachEventListeners() {
        // Los event listeners específicos se manejan en renderParametersForm
    }

    updateStabilityIndicator() {
        const rho = this.calculateRho();
        const indicator = document.getElementById('stabilityIndicator');
        
        if (!indicator) return;
        
        let status, statusClass, message;
        
        if (rho < 0.7) {
            status = 'Óptimo';
            statusClass = 'status-optimal';
            message = 'El sistema está operando en condiciones óptimas';
        } else if (rho < 0.9) {
            status = 'Aceptable';
            statusClass = 'status-acceptable';
            message = 'El sistema está aceptablemente cargado';
        } else if (rho < 1.0) {
            status = 'Crítico';
            statusClass = 'status-critical';
            message = 'El sistema está cerca de saturación';
        } else {
            status = 'Inestable';
            statusClass = 'status-critical';
            message = '⚠️ Sistema inestable: ρ ≥ 1. No alcanzará estado estacionario';
        }
        
        const percentage = Math.min(rho * 100, 100);
        
        indicator.innerHTML = `
            <div class="rho-display">
                <span class="rho-value" style="color: ${this.getRhoColor(rho)}">
                    ρ = ${rho.toFixed(3)}
                </span>
                <span class="rho-label">Utilización del Sistema</span>
            </div>
            
            <div class="gauge-container">
                <svg class="gauge" viewBox="0 0 200 120">
                    <!-- Background arc -->
                    <path d="M 20 100 A 80 80 0 0 1 180 100" 
                          fill="none" 
                          stroke="var(--bg-tertiary)" 
                          stroke-width="20" 
                          stroke-linecap="round"/>
                    
                    <!-- Value arc -->
                    <path d="M 20 100 A 80 80 0 0 1 180 100" 
                          fill="none" 
                          stroke="${this.getRhoColor(rho)}" 
                          stroke-width="20" 
                          stroke-linecap="round"
                          stroke-dasharray="${percentage * 2.51}, 251"
                          style="transition: stroke-dasharray 0.5s ease;"/>
                    
                    <!-- Center text -->
                    <text x="100" y="85" 
                          text-anchor="middle" 
                          font-size="24" 
                          font-weight="bold" 
                          fill="currentColor">
                        ${percentage.toFixed(0)}%
                    </text>
                </svg>
            </div>
            
            <div class="stability-status ${statusClass}">
                <strong>${status}</strong><br/>
                <small>${message}</small>
            </div>
        `;
    }

    calculateRho() {
        const { lambda, mu, c } = this.config;
        
        if (this.currentModel === 'mm1' || this.currentModel === 'mmk1') {
            return lambda / mu;
        } else {
            return lambda / (c * mu);
        }
    }

    getRhoColor(rho) {
        if (rho < 0.7) return '#10B981'; // Verde
        if (rho < 0.9) return '#F59E0B'; // Amarillo
        if (rho < 1.0) return '#F97316'; // Naranja
        return '#EF4444'; // Rojo
    }

    getCurrentConfig() {
        return {
            ...this.config,
            model: this.currentModel
        };
    }

    loadDefaultConfig() {
        this.selectModel('mm1');
        this.updateStabilityIndicator();
    }

    validate(config) {
        // Validaciones básicas
        if (config.lambda <= 0) {
            return { valid: false, message: 'λ debe ser mayor que 0' };
        }
        
        if (config.mu <= 0) {
            return { valid: false, message: 'μ debe ser mayor que 0' };
        }
        
        if (config.horizon <= 0) {
            return { valid: false, message: 'El horizonte debe ser mayor que 0' };
        }
        
        if (config.warmup < 0) {
            return { valid: false, message: 'El warmup no puede ser negativo' };
        }
        
        if (config.warmup >= config.horizon) {
            return { valid: false, message: 'El warmup debe ser menor que el horizonte' };
        }
        
        if ((config.model === 'mmc' || config.model === 'mmkc') && config.c <= 0) {
            return { valid: false, message: 'El número de servidores debe ser mayor que 0' };
        }
        
        if ((config.model === 'mmk1' || config.model === 'mmkc') && config.k <= 0) {
            return { valid: false, message: 'La capacidad debe ser mayor que 0' };
        }
        
        // Verificar estabilidad
        const rho = this.calculateRho();
        const unstable = rho >= 1.0;
        
        return { 
            valid: true, 
            unstable,
            rho
        };
    }

    calculateTheory(config) {
        const { lambda, mu, c, model } = config;
        
        if (model === 'mm1') {
            return this.calculateMM1Theory(lambda, mu);
        } else if (model === 'mmc') {
            return this.calculateMMcTheory(lambda, mu, c);
        }
        
        return null;
    }

    calculateMM1Theory(lambda, mu) {
        const rho = lambda / mu;
        
        if (rho >= 1.0) return null;
        
        const L = rho / (1 - rho);
        const Lq = (rho * rho) / (1 - rho);
        const W = 1 / (mu - lambda);
        const Wq = rho / (mu - lambda);
        
        return { rho, L, Lq, W, Wq };
    }

    calculateMMcTheory(lambda, mu, c) {
        const rho = lambda / (c * mu);
        const a = lambda / mu;
        
        if (rho >= 1.0) return null;
        
        // Calcular P0 usando fórmula de Erlang-C
        let sum = 0;
        for (let n = 0; n < c; n++) {
            sum += Math.pow(a, n) / this.factorial(n);
        }
        const lastTerm = (Math.pow(a, c) / this.factorial(c)) * (1 / (1 - rho));
        const P0 = 1 / (sum + lastTerm);
        
        // Probabilidad de espera (C de Erlang)
        const C = ((Math.pow(a, c) / this.factorial(c)) * (1 / (1 - rho))) * P0;
        
        // Métricas
        const Lq = C * rho / (1 - rho);
        const L = Lq + a;
        const Wq = Lq / lambda;
        const W = Wq + (1 / mu);
        
        return { rho, L, Lq, W, Wq, P0, C };
    }

    factorial(n) {
        if (n <= 1) return 1;
        let result = 1;
        for (let i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }
}
