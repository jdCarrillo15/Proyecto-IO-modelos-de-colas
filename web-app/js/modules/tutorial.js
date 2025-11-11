/**
 * TUTORIAL MANAGER - Gestor de Tutorial Interactivo
 */

export class TutorialManager {
    constructor() {
        this.steps = [
            {
                title: '¡Bienvenido! 👋',
                content: 'Este es un sistema interactivo para simular modelos de colas. Te guiaré por las funcionalidades principales.'
            },
            {
                title: 'Modelos de Cola 📋',
                content: `
                    <ul>
                        <li><strong>M/M/1:</strong> Un servidor, capacidad infinita</li>
                        <li><strong>M/M/c:</strong> Múltiples servidores, capacidad infinita</li>
                        <li><strong>M/M/k/1:</strong> Un servidor, capacidad limitada</li>
                        <li><strong>M/M/k/c:</strong> Múltiples servidores, capacidad limitada</li>
                    </ul>
                `
            },
            {
                title: 'Parámetros del Sistema ⚙️',
                content: `
                    <ul>
                        <li><strong>λ (Lambda):</strong> Tasa de llegadas de clientes</li>
                        <li><strong>μ (Mu):</strong> Tasa de servicio</li>
                        <li><strong>c:</strong> Número de servidores</li>
                        <li><strong>k:</strong> Capacidad máxima del sistema</li>
                    </ul>
                `
            },
            {
                title: 'Estabilidad del Sistema 📊',
                content: 'La utilización ρ = λ/(c·μ) indica la carga del sistema. Para que sea estable, debe ser ρ < 1.'
            },
            {
                title: 'Ejecutar Simulación ▶️',
                content: 'Ajusta los parámetros y haz clic en "Ejecutar Simulación". Verás la animación en tiempo real y las métricas actualizándose.'
            },
            {
                title: 'Resultados y Exportación 💾',
                content: 'Al finalizar, podrás ver un resumen completo y exportar los resultados en formato JSON o generar un reporte HTML.'
            }
        ];
        this.currentStep = 0;
    }

    show() {
        const modal = document.getElementById('tutorialModal');
        const content = document.getElementById('tutorialContent');
        
        if (!modal || !content) return;
        
        this.currentStep = 0;
        this.renderStep();
        modal.classList.add('show');
        
        // Event listeners
        const closeBtn = modal.querySelector('.modal-close');
        const overlay = modal.querySelector('.modal-overlay');
        
        const close = () => modal.classList.remove('show');
        
        if (closeBtn) closeBtn.onclick = close;
        if (overlay) overlay.onclick = close;
    }

    renderStep() {
        const content = document.getElementById('tutorialContent');
        if (!content) return;
        
        const step = this.steps[this.currentStep];
        const isFirst = this.currentStep === 0;
        const isLast = this.currentStep === this.steps.length - 1;
        
        content.innerHTML = `
            <div class="tutorial-step">
                <h3>${step.title}</h3>
                <div class="tutorial-content">${step.content}</div>
                <div class="tutorial-progress">
                    ${this.currentStep + 1} / ${this.steps.length}
                </div>
                <div class="tutorial-navigation">
                    <button class="btn btn-secondary" id="prevStep" ${isFirst ? 'disabled' : ''}>
                        ← Anterior
                    </button>
                    <button class="btn btn-primary" id="nextStep">
                        ${isLast ? 'Finalizar ✓' : 'Siguiente →'}
                    </button>
                </div>
            </div>
        `;
        
        // Event listeners para navegación
        const prevBtn = document.getElementById('prevStep');
        const nextBtn = document.getElementById('nextStep');
        
        if (prevBtn) {
            prevBtn.onclick = () => {
                if (this.currentStep > 0) {
                    this.currentStep--;
                    this.renderStep();
                }
            };
        }
        
        if (nextBtn) {
            nextBtn.onclick = () => {
                if (this.currentStep < this.steps.length - 1) {
                    this.currentStep++;
                    this.renderStep();
                } else {
                    document.getElementById('tutorialModal').classList.remove('show');
                }
            };
        }
    }
}
