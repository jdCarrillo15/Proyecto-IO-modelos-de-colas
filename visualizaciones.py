"""
Módulo de visualizaciones adicionales para análisis de colas

Este módulo proporciona herramientas de visualización avanzadas
para analizar resultados de simulación, incluyendo:
- Histogramas de tiempos de espera
- Gráficos de utilización por servidor
- Distribuciones de tiempos en sistema
- Comparaciones entre modelos
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from typing import List, Dict, Optional
from sim_colas_animado import EventSim, MM1, MMC, MMK1, MMKC
from teoria_colas import analytical_mm1, analytical_mmc, compare_simulation_vs_theory


class VisualizadorColas:
    """Clase para generar visualizaciones avanzadas de resultados de simulación"""
    
    def __init__(self, sim: EventSim, nombre_modelo: str = "Modelo"):
        """
        Inicializar visualizador
        
        Parámetros:
            sim: Instancia de simulación (MM1, MMC, etc.)
            nombre_modelo: Nombre descriptivo del modelo
        """
        self.sim = sim
        self.nombre_modelo = nombre_modelo
    
    def plot_histograma_tiempos_espera(self, bins: int = 30, figsize: tuple = (12, 5)):
        """
        Generar histogramas de tiempos de espera en cola y en sistema
        
        Parámetros:
            bins: Número de bins para el histograma
            figsize: Tamaño de la figura
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Histograma de tiempos en cola
        if self.sim.wait_times_q:
            ax1.hist(self.sim.wait_times_q, bins=bins, alpha=0.7, color='#FF6B6B', edgecolor='black')
            media_wq = np.mean(self.sim.wait_times_q)
            ax1.axvline(media_wq, color='darkred', linestyle='--', linewidth=2, label=f'Media: {media_wq:.2f}')
            ax1.set_xlabel('Tiempo en cola (Wq)', fontsize=11, fontweight='bold')
            ax1.set_ylabel('Frecuencia', fontsize=11, fontweight='bold')
            ax1.set_title(f'{self.nombre_modelo}: Distribución de Tiempos en Cola', fontsize=12, fontweight='bold')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
        else:
            ax1.text(0.5, 0.5, 'Sin datos', ha='center', va='center', transform=ax1.transAxes)
        
        # Histograma de tiempos en sistema
        if self.sim.wait_times:
            ax2.hist(self.sim.wait_times, bins=bins, alpha=0.7, color='#4ECDC4', edgecolor='black')
            media_w = np.mean(self.sim.wait_times)
            ax2.axvline(media_w, color='darkblue', linestyle='--', linewidth=2, label=f'Media: {media_w:.2f}')
            ax2.set_xlabel('Tiempo en sistema (W)', fontsize=11, fontweight='bold')
            ax2.set_ylabel('Frecuencia', fontsize=11, fontweight='bold')
            ax2.set_title(f'{self.nombre_modelo}: Distribución de Tiempos en Sistema', fontsize=12, fontweight='bold')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        else:
            ax2.text(0.5, 0.5, 'Sin datos', ha='center', va='center', transform=ax2.transAxes)
        
        plt.tight_layout()
        plt.show()
    
    def plot_serie_temporal_completa(self, figsize: tuple = (14, 8)):
        """
        Generar gráfico de series temporales completo (L, Lq, utilización)
        
        Parámetros:
            figsize: Tamaño de la figura
        """
        if not self.sim.time_series:
            print("⚠ No hay datos de series temporales")
            return
        
        fig = plt.figure(figsize=figsize)
        gs = gridspec.GridSpec(3, 1, height_ratios=[1, 1, 1], hspace=0.3)
        
        # Gráfico 1: Clientes en sistema (L)
        ax1 = plt.subplot(gs[0])
        ax1.plot(self.sim.time_series, self.sim.system_series, 'b-', linewidth=1.5, alpha=0.7)
        media_l = self.sim.state()['l_avg']
        ax1.axhline(media_l, color='red', linestyle='--', linewidth=2, label=f'L̄ = {media_l:.2f}')
        ax1.set_ylabel('Clientes en sistema (L)', fontsize=11, fontweight='bold')
        ax1.set_title(f'{self.nombre_modelo}: Evolución Temporal', fontsize=13, fontweight='bold')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        
        # Gráfico 2: Clientes en cola (Lq)
        ax2 = plt.subplot(gs[1])
        ax2.plot(self.sim.time_series, self.sim.queue_series, 'g-', linewidth=1.5, alpha=0.7)
        media_lq = self.sim.state()['lq_avg']
        ax2.axhline(media_lq, color='darkgreen', linestyle='--', linewidth=2, label=f'L̄q = {media_lq:.2f}')
        ax2.set_ylabel('Clientes en cola (Lq)', fontsize=11, fontweight='bold')
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)
        
        # Gráfico 3: Utilización instantánea (aproximada)
        ax3 = plt.subplot(gs[2])
        if isinstance(self.sim, MM1):
            # Para MM1, utilización es 1 si servidor ocupado, 0 si no
            util_series = [1 if L > 0 else 0 for L in self.sim.system_series]
        elif isinstance(self.sim, MMC):
            # Para MMC, utilización es proporción de servidores ocupados
            c = len(self.sim.servers)
            util_series = [min(L / c, 1.0) for L in self.sim.system_series]
        else:
            # Para otros modelos, aproximar
            util_series = [min(L / 5.0, 1.0) for L in self.sim.system_series]
        
        ax3.plot(self.sim.time_series, util_series, 'orange', linewidth=1.5, alpha=0.7)
        rho = self.sim.state()['rho']
        ax3.axhline(rho, color='red', linestyle='--', linewidth=2, label=f'ρ = {rho:.3f}')
        ax3.set_xlabel('Tiempo de simulación', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Utilización (ρ)', fontsize=11, fontweight='bold')
        ax3.set_ylim(0, 1.1)
        ax3.legend(loc='upper right')
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_utilizacion_servidores(self, figsize: tuple = (10, 6)):
        """
        Generar gráfico de utilización por servidor (solo para MMC, MMK1, MMKC)
        
        Parámetros:
            figsize: Tamaño de la figura
        """
        if isinstance(self.sim, MM1):
            print("⚠ Este gráfico solo está disponible para modelos con múltiples servidores")
            return
        
        # Calcular utilización por servidor basada en tiempo ocupado
        # Nota: Esta es una aproximación simplificada
        fig, ax = plt.subplots(figsize=figsize)
        
        if isinstance(self.sim, MMC):
            # Para MMC
            num_servers = len(self.sim.servers)
            utilizaciones = []
            for i, server in enumerate(self.sim.servers):
                # Tiempo ocupado / tiempo total
                tiempo_ocupado = server.busy_until if server.current_job else 0
                util = min(1.0, tiempo_ocupado / self.sim.time) if self.sim.time > 0 else 0
                utilizaciones.append(util)
            
            colores = plt.cm.viridis(np.linspace(0.2, 0.8, num_servers))
            bars = ax.bar(range(num_servers), utilizaciones, color=colores, edgecolor='black', linewidth=1.5)
            ax.set_xlabel('Servidor', fontsize=11, fontweight='bold')
            ax.set_ylabel('Utilización (ρ)', fontsize=11, fontweight='bold')
            ax.set_title(f'{self.nombre_modelo}: Utilización por Servidor', fontsize=13, fontweight='bold')
            ax.set_xticks(range(num_servers))
            ax.set_xticklabels([f'S{i+1}' for i in range(num_servers)])
            ax.set_ylim(0, 1.1)
            ax.grid(True, alpha=0.3, axis='y')
            
            # Añadir valores en las barras
            for i, (bar, util) in enumerate(zip(bars, utilizaciones)):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{util:.2f}',
                       ha='center', va='bottom', fontweight='bold')
        
        elif isinstance(self.sim, (MMK1, MMKC)):
            print("ℹ Visualización de utilización para modelos M/M/k/1 y M/M/k/c")
            print("  (Implementación simplificada - utilización global)")
            rho = self.sim.state()['rho']
            ax.bar([0], [rho], color='#4ECDC4', edgecolor='black', linewidth=1.5)
            ax.set_ylabel('Utilización promedio (ρ)', fontsize=11, fontweight='bold')
            ax.set_title(f'{self.nombre_modelo}: Utilización Global', fontsize=13, fontweight='bold')
            ax.set_xticks([0])
            ax.set_xticklabels(['Sistema'])
            ax.set_ylim(0, 1.1)
            ax.grid(True, alpha=0.3, axis='y')
            ax.text(0, rho, f'{rho:.3f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def generar_reporte_completo(self, incluir_teoria: bool = True):
        """
        Generar reporte completo con todas las visualizaciones
        
        Parámetros:
            incluir_teoria: Si True, incluir comparación con teoría (solo M/M/1 y M/M/c)
        """
        print("\n" + "="*80)
        print(f"REPORTE COMPLETO: {self.nombre_modelo}")
        print("="*80)
        
        # Métricas
        st = self.sim.state()
        print(f"\nPARÁMETROS:")
        print(f"  λ (tasa llegadas)    = {self.sim.lam:.3f}")
        print(f"  μ (tasa servicio)    = {self.sim.mu:.3f}")
        print(f"  Horizonte simulación = {self.sim.horizon:.2f}")
        print(f"  Periodo warmup       = {self.sim.warmup:.2f}")
        
        print(f"\nMÉTRICAS DE DESEMPEÑO:")
        print(f"  ρ (utilización)      = {st['rho']:.4f}")
        print(f"  L (clientes sistema) = {st['l_avg']:.4f}")
        print(f"  Lq (clientes cola)   = {st['lq_avg']:.4f}")
        print(f"  W (tiempo sistema)   = {st['w_avg']:.4f}")
        print(f"  Wq (tiempo cola)     = {st['wq_avg']:.4f}")
        print(f"  Clientes atendidos   = {st['served']}")
        
        # Comparación con teoría
        if incluir_teoria and isinstance(self.sim, (MM1, MMC)):
            try:
                if isinstance(self.sim, MM1):
                    theo = analytical_mm1(self.sim.lam, self.sim.mu)
                else:  # MMC
                    theo = analytical_mmc(self.sim.lam, self.sim.mu, len(self.sim.servers))
                
                sim_metrics = {
                    'L': st['l_avg'],
                    'Lq': st['lq_avg'],
                    'W': st['w_avg'],
                    'Wq': st['wq_avg'],
                    'rho': st['rho'],
                }
                
                print(f"\nCOMPARACIÓN CON TEORÍA:")
                print(f"{'Métrica':<10} {'Simulación':<15} {'Teoría':<15} {'Error':<15}")
                print("-"*55)
                for key in ['L', 'Lq', 'W', 'Wq', 'rho']:
                    sim_val = sim_metrics[key]
                    theo_val = theo[key]
                    error = abs(sim_val - theo_val) / theo_val if theo_val != 0 else 0
                    print(f"{key:<10} {sim_val:<15.4f} {theo_val:<15.4f} {error:<15.2%}")
            
            except ValueError as e:
                print(f"\n⚠ No se puede calcular teoría: {e}")
        
        print("="*80)
        
        # Generar gráficos
        print("\n📊 Generando visualizaciones...\n")
        self.plot_histograma_tiempos_espera()
        self.plot_serie_temporal_completa()
        self.plot_utilizacion_servidores()


def comparar_modelos(sims: List[EventSim], nombres: List[str], figsize: tuple = (14, 10)):
    """
    Comparar múltiples modelos en un solo gráfico
    
    Parámetros:
        sims: Lista de simulaciones ejecutadas
        nombres: Lista de nombres de modelos
        figsize: Tamaño de la figura
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    axes = axes.flatten()
    
    colores = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#F38181']
    
    # Gráfico 1: Comparación de L (clientes en sistema)
    ax1 = axes[0]
    for i, (sim, nombre) in enumerate(zip(sims, nombres)):
        st = sim.state()
        ax1.bar(i, st['l_avg'], color=colores[i % len(colores)], edgecolor='black', linewidth=1.5, label=nombre)
    ax1.set_ylabel('L̄ (Clientes promedio en sistema)', fontsize=11, fontweight='bold')
    ax1.set_title('Comparación: Clientes en Sistema', fontsize=12, fontweight='bold')
    ax1.set_xticks(range(len(nombres)))
    ax1.set_xticklabels(nombres, rotation=15, ha='right')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Gráfico 2: Comparación de W (tiempo en sistema)
    ax2 = axes[1]
    for i, (sim, nombre) in enumerate(zip(sims, nombres)):
        st = sim.state()
        ax2.bar(i, st['w_avg'], color=colores[i % len(colores)], edgecolor='black', linewidth=1.5, label=nombre)
    ax2.set_ylabel('W̄ (Tiempo promedio en sistema)', fontsize=11, fontweight='bold')
    ax2.set_title('Comparación: Tiempo en Sistema', fontsize=12, fontweight='bold')
    ax2.set_xticks(range(len(nombres)))
    ax2.set_xticklabels(nombres, rotation=15, ha='right')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Gráfico 3: Comparación de ρ (utilización)
    ax3 = axes[2]
    for i, (sim, nombre) in enumerate(zip(sims, nombres)):
        st = sim.state()
        ax3.bar(i, st['rho'], color=colores[i % len(colores)], edgecolor='black', linewidth=1.5, label=nombre)
    ax3.set_ylabel('ρ (Utilización)', fontsize=11, fontweight='bold')
    ax3.set_title('Comparación: Utilización del Sistema', fontsize=12, fontweight='bold')
    ax3.set_xticks(range(len(nombres)))
    ax3.set_xticklabels(nombres, rotation=15, ha='right')
    ax3.set_ylim(0, 1.1)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Gráfico 4: Comparación de Wq (tiempo en cola)
    ax4 = axes[3]
    for i, (sim, nombre) in enumerate(zip(sims, nombres)):
        st = sim.state()
        ax4.bar(i, st['wq_avg'], color=colores[i % len(colores)], edgecolor='black', linewidth=1.5, label=nombre)
    ax4.set_ylabel('W̄q (Tiempo promedio en cola)', fontsize=11, fontweight='bold')
    ax4.set_title('Comparación: Tiempo en Cola', fontsize=12, fontweight='bold')
    ax4.set_xticks(range(len(nombres)))
    ax4.set_xticklabels(nombres, rotation=15, ha='right')
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('Comparación de Modelos de Colas', fontsize=15, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # Ejemplo de uso
    print("🎨 Generando visualizaciones de ejemplo...\n")
    
    # Crear y ejecutar simulación M/M/1
    sim_mm1 = MM1(lam=0.6, mu=2.0, horizon=5000, warmup=500)
    while sim_mm1.time < sim_mm1.horizon:
        sim_mm1.step()
    
    # Generar reporte
    viz = VisualizadorColas(sim_mm1, "M/M/1 (λ=0.6, μ=2.0)")
    viz.generar_reporte_completo(incluir_teoria=True)
