/**
 * UI MANAGER - Gestor de Interfaz de Usuario
 */

export class UIManager {
    constructor() {
        this.theme = 'dark';
    }

    async init() {
        console.log('Inicializando UIManager...');
        this.loadTheme();
    }

    toggleTheme() {
        this.theme = this.theme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', this.theme);
        localStorage.setItem('theme', this.theme);
        
        const icon = document.querySelector('.theme-icon');
        if (icon) {
            icon.textContent = this.theme === 'dark' ? '☀️' : '🌙';
        }
        
        this.showToast(`Tema ${this.theme === 'dark' ? 'oscuro' : 'claro'} activado`, 'info');
    }

    loadTheme() {
        const savedTheme = localStorage.getItem('theme') || 'dark';
        this.theme = savedTheme;
        document.documentElement.setAttribute('data-theme', savedTheme);
        
        const icon = document.querySelector('.theme-icon');
        if (icon) {
            icon.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
        }
    }

    setSimulationRunning(running) {
        const runBtn = document.getElementById('runSimulation');
        const pauseBtn = document.getElementById('pauseSimulation');
        const resetBtn = document.getElementById('resetSimulation');
        
        if (runBtn) runBtn.disabled = running;
        if (pauseBtn) pauseBtn.disabled = !running;
        if (resetBtn) resetBtn.disabled = false;
    }

    updateProgress(percent, currentTime, totalTime) {
        const fill = document.getElementById('progressFill');
        const label = document.getElementById('progressLabel');
        const percentLabel = document.getElementById('progressPercent');
        
        if (fill) fill.style.width = `${percent}%`;
        if (label) label.textContent = `Tiempo: ${currentTime.toFixed(1)} / ${totalTime.toFixed(0)}`;
        if (percentLabel) percentLabel.textContent = `${percent.toFixed(0)}%`;
    }

    showLoading(message = 'Cargando...') {
        const spinner = document.getElementById('loadingSpinner');
        if (spinner) {
            spinner.style.display = 'flex';
            const text = spinner.querySelector('p');
            if (text) text.textContent = message;
        }
    }

    hideLoading() {
        const spinner = document.getElementById('loadingSpinner');
        if (spinner) {
            spinner.style.display = 'none';
        }
    }

    showToast(message, type = 'info') {
        const container = document.getElementById('toastContainer');
        if (!container) return;
        
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        
        toast.innerHTML = `
            <span class="toast-icon">${icons[type] || icons.info}</span>
            <div class="toast-content">
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close">×</button>
        `;
        
        container.appendChild(toast);
        
        // Auto-close
        const autoClose = setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
        
        // Manual close
        toast.querySelector('.toast-close').addEventListener('click', () => {
            clearTimeout(autoClose);
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        });
    }

    async showConfirm(title, message) {
        return new Promise((resolve) => {
            const modal = document.createElement('div');
            modal.className = 'modal show';
            modal.innerHTML = `
                <div class="modal-overlay"></div>
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>${title}</h2>
                    </div>
                    <div class="modal-body">
                        <p>${message}</p>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" id="cancelBtn">Cancelar</button>
                        <button class="btn btn-primary" id="confirmBtn">Continuar</button>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            modal.querySelector('#confirmBtn').onclick = () => {
                modal.remove();
                resolve(true);
            };
            
            modal.querySelector('#cancelBtn').onclick = () => {
                modal.remove();
                resolve(false);
            };
            
            modal.querySelector('.modal-overlay').onclick = () => {
                modal.remove();
                resolve(false);
            };
        });
    }

    showModal(title, content) {
        const modal = document.createElement('div');
        modal.className = 'modal show';
        modal.innerHTML = `
            <div class="modal-overlay"></div>
            <div class="modal-content">
                <div class="modal-header">
                    <h2>${title}</h2>
                    <button class="modal-close">×</button>
                </div>
                <div class="modal-body">
                    ${content}
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        const close = () => modal.remove();
        modal.querySelector('.modal-close').onclick = close;
        modal.querySelector('.modal-overlay').onclick = close;
    }

    updateStabilityIndicator(config) {
        // Implementado en config.js
    }
}
