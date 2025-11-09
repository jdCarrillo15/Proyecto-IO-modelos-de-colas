"""
Ejemplos de uso del proyecto de simulación de colas

Este archivo contiene ejemplos prácticos de cómo usar las diferentes
funcionalidades del proyecto.
"""

import random
from sim_colas_animado import MM1, MMC, MMK1, MMKC, ModelSpec, AnimatedComparison
from teoría_colas import (
    analytical_mm1, 
    analytical_mmc,
    compare_simulation_vs_theory,
    print_comparison,
    littles_law_check
)
from visualizaciones import VisualizadorColas, comparar_modelos


def ejemplo_1_simulacion_basica():
    """Ejemplo 1: Simulación básica de M/M/1"""
    print("\n" + "="*80)
    print("EJEMPLO 1: SIMULACIÓN BÁSICA M/M/1")
    print("="*80)
    
    # Crear simulación
    sim = MM1(lam=0.6, mu=2.0, horizon=10000, warmup=1000)
    
    print(f"\nSimulando M/M/1 con λ=0.6, μ=2.0...")
    print(f"Horizonte: {sim.horizon}, Warmup: {sim.warmup}")
    
    # Ejecutar simulación
    while sim.time < sim.horizon:
        sim.step()
    
    # Mostrar resultados
    st = sim.state()
    print(f"\n✓ Simulación completada!")
    print(f"\nRESULTADOS:")
    print(f"  ρ (utilización)      = {st['rho']:.4f}")
    print(f"  L (clientes sistema) = {st['l_avg']:.4f}")
    print(f"  Lq (clientes cola)   = {st['lq_avg']:.4f}")
    print(f"  W (tiempo sistema)   = {st['w_avg']:.4f}")
    print(f"  Wq (tiempo cola)     = {st['wq_avg']:.4f}")
    print(f"  Clientes atendidos   = {st['served']}")


def ejemplo_2_validacion_teoria():
    """Ejemplo 2: Validación con teoría analítica"""
    print("\n" + "="*80)
    print("EJEMPLO 2: VALIDACIÓN CON TEORÍA ANALÍTICA")
    print("="*80)
    
    lam, mu = 0.6, 2.0
    
    # Simulación
    print(f"\n1. Ejecutando simulación M/M/1 (λ={lam}, μ={mu})...")
    sim = MM1(lam=lam, mu=mu, horizon=20000, warmup=2000)
    
    while sim.time < sim.horizon:
        sim.step()
    
    # Teoría
    print(f"2. Calculando métricas analíticas...")
    theo = analytical_mm1(lam, mu)
    
    # Comparación
    st = sim.state()
    sim_metrics = {
        'L': st['l_avg'],
        'Lq': st['lq_avg'],
        'W': st['w_avg'],
        'Wq': st['wq_avg'],
        'rho': st['rho'],
    }
    
    comparison = compare_simulation_vs_theory(sim_metrics, theo, tolerance=0.15)
    print_comparison(comparison)
    
    # Verificar Ley de Little
    print("\n3. Verificando Ley de Little (L = λW)...")
    is_valid = littles_law_check(st['l_avg'], lam, st['w_avg'], tolerance=0.1)
    print(f"   L = {st['l_avg']:.4f}")
    print(f"   λW = {lam * st['w_avg']:.4f}")
    print(f"   {'✓ Válido' if is_valid else '✗ Inválido'}")


def ejemplo_3_exportacion():
    """Ejemplo 3: Exportar resultados a JSON"""
    print("\n" + "="*80)
    print("EJEMPLO 3: EXPORTACIÓN DE RESULTADOS")
    print("="*80)
    
    # Simulación
    sim = MMC(lam=0.7, mu=2.5, c=3, horizon=5000, warmup=500)
    
    print(f"\nSimulando M/M/c con λ=0.7, μ=2.5, c=3...")
    while sim.time < sim.horizon:
        sim.step()
    
    # Exportar
    filename = "resultados_mmc_ejemplo.json"
    sim.export_results(filename)
    
    print(f"\n💾 Resultados guardados en: {filename}")
    print(f"   El archivo contiene:")
    print(f"   - Parámetros de simulación")
    print(f"   - Métricas calculadas")
    print(f"   - Series temporales (L(t), Lq(t))")
    print(f"   - Tiempos de espera individuales")


def ejemplo_4_visualizaciones():
    """Ejemplo 4: Generar visualizaciones avanzadas"""
    print("\n" + "="*80)
    print("EJEMPLO 4: VISUALIZACIONES AVANZADAS")
    print("="*80)
    
    # Simulación
    sim = MM1(lam=0.6, mu=2.0, horizon=5000, warmup=500)
    
    print(f"\nSimulando M/M/1 para visualizaciones...")
    while sim.time < sim.horizon:
        sim.step()
    
    # Crear visualizador
    viz = VisualizadorColas(sim, "M/M/1 (λ=0.6, μ=2.0)")
    
    print(f"\n📊 Generando visualizaciones...")
    print(f"   1. Histogramas de tiempos de espera")
    print(f"   2. Series temporales completas")
    print(f"   3. Utilización de servidores")
    print(f"   4. Comparación con teoría")
    
    # Generar reporte completo
    viz.generar_reporte_completo(incluir_teoria=True)


def ejemplo_5_comparacion_modelos():
    """Ejemplo 5: Comparar múltiples modelos"""
    print("\n" + "="*80)
    print("EJEMPLO 5: COMPARACIÓN ENTRE MODELOS")
    print("="*80)
    
    # Configuración común
    horizon = 10000
    warmup = 1000
    
    # Crear y ejecutar simulaciones
    print(f"\nEjecutando simulaciones de 4 modelos diferentes...")
    
    sims = []
    nombres = []
    
    # M/M/1
    print("  1/4 M/M/1...")
    sim1 = MM1(lam=0.6, mu=2.0, horizon=horizon, warmup=warmup)
    while sim1.time < sim1.horizon:
        sim1.step()
    sims.append(sim1)
    nombres.append("M/M/1")
    
    # M/M/c
    print("  2/4 M/M/c...")
    sim2 = MMC(lam=0.7, mu=2.5, c=3, horizon=horizon, warmup=warmup)
    while sim2.time < sim2.horizon:
        sim2.step()
    sims.append(sim2)
    nombres.append("M/M/c")
    
    # M/M/k/1
    print("  3/4 M/M/k/1...")
    sim3 = MMK1(lam=0.8, mu=2.5, k=3, horizon=horizon, warmup=warmup)
    while sim3.time < sim3.horizon:
        sim3.step()
    sims.append(sim3)
    nombres.append("M/M/k/1")
    
    # M/M/k/c
    print("  4/4 M/M/k/c...")
    sim4 = MMKC(lam=0.9, mu=2.5, k=2, c=2, horizon=horizon, warmup=warmup)
    while sim4.time < sim4.horizon:
        sim4.step()
    sims.append(sim4)
    nombres.append("M/M/k/c")
    
    # Comparar
    print(f"\n📊 Generando gráficos comparativos...")
    comparar_modelos(sims, nombres)


def ejemplo_6_sistema_inestable():
    """Ejemplo 6: Detectar sistema inestable"""
    print("\n" + "="*80)
    print("EJEMPLO 6: DETECCIÓN DE SISTEMAS INESTABLES")
    print("="*80)
    
    print("\nIntentando crear M/M/1 con ρ = 1.5 (inestable)...")
    print("λ = 3.0, μ = 2.0")
    
    # Esto lanzará un warning
    import warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        sim = MM1(lam=3.0, mu=2.0, horizon=1000)
        
        if w:
            print(f"\n⚠️  WARNING DETECTADO:")
            print(f"    {w[0].message}")
            print(f"\n✓ El sistema detectó automáticamente que ρ ≥ 1")
            print(f"  Esto significa que la cola crecerá indefinidamente.")
    
    print("\nPara sistemas estables, usar ρ < 1:")
    print("Ejemplo: λ = 0.6, μ = 2.0 → ρ = 0.3 < 1 ✓")


def ejemplo_7_reproducibilidad():
    """Ejemplo 7: Reproducibilidad con semilla"""
    print("\n" + "="*80)
    print("EJEMPLO 7: REPRODUCIBILIDAD CON SEMILLA")
    print("="*80)
    
    print("\nEjecutando dos simulaciones idénticas con la misma semilla...")
    
    # Simulación 1
    random.seed(42)
    sim1 = MMK1(lam=0.8, mu=2.5, k=3, horizon=1000)
    while sim1.time < sim1.horizon:
        sim1.step()
    
    # Simulación 2
    random.seed(42)
    sim2 = MMK1(lam=0.8, mu=2.5, k=3, horizon=1000)
    while sim2.time < sim2.horizon:
        sim2.step()
    
    # Comparar
    st1 = sim1.state()
    st2 = sim2.state()
    
    print(f"\nRESULTADOS:")
    print(f"  Simulación 1 - L: {st1['l_avg']:.6f}, Clientes: {st1['served']}")
    print(f"  Simulación 2 - L: {st2['l_avg']:.6f}, Clientes: {st2['served']}")
    
    if st1['served'] == st2['served'] and abs(st1['l_avg'] - st2['l_avg']) < 1e-6:
        print(f"\n✓ Resultados idénticos - Reproducibilidad confirmada!")
    else:
        print(f"\n✗ Resultados diferentes")


def ejemplo_8_animacion():
    """Ejemplo 8: Ejecutar animación comparativa"""
    print("\n" + "="*80)
    print("EJEMPLO 8: ANIMACIÓN COMPARATIVA 2x2")
    print("="*80)
    
    print("\nConfigurando animación con 4 modelos...")
    
    # Definir especificaciones
    specs = [
        ModelSpec('M/M/1', 'mm1', {'lam': 0.6, 'mu': 2.0}),
        ModelSpec('M/M/c', 'mmc', {'lam': 0.7, 'mu': 2.5, 'c': 3}),
        ModelSpec('M/M/k/1', 'mmk1', {'lam': 0.8, 'mu': 2.5, 'k': 3}),
        ModelSpec('M/M/k/c', 'mmkc', {'lam': 0.9, 'mu': 2.5, 'k': 2, 'c': 2}),
    ]
    
    print(f"\nModelos a animar:")
    for spec in specs:
        print(f"  - {spec.name}: {spec.params}")
    
    print(f"\n🎬 Iniciando animación...")
    print(f"   (Cerrar ventana para continuar)")
    
    anim = AnimatedComparison(specs, horizon=120.0, seed=42)
    anim.run(dt=0.2, frames=500, interval_ms=100)


def menu_ejemplos():
    """Menú interactivo de ejemplos"""
    ejemplos = {
        '1': ("Simulación básica M/M/1", ejemplo_1_simulacion_basica),
        '2': ("Validación con teoría analítica", ejemplo_2_validacion_teoria),
        '3': ("Exportación de resultados", ejemplo_3_exportacion),
        '4': ("Visualizaciones avanzadas", ejemplo_4_visualizaciones),
        '5': ("Comparación entre modelos", ejemplo_5_comparacion_modelos),
        '6': ("Detección de sistemas inestables", ejemplo_6_sistema_inestable),
        '7': ("Reproducibilidad", ejemplo_7_reproducibilidad),
        '8': ("Animación comparativa", ejemplo_8_animacion),
    }
    
    print("\n" + "="*80)
    print("EJEMPLOS DE USO - SIMULACIÓN DE COLAS")
    print("="*80)
    print("\nSeleccione un ejemplo:")
    
    for key, (desc, _) in ejemplos.items():
        print(f"  {key}. {desc}")
    
    print("  0. Salir")
    print("  A. Ejecutar todos")
    
    opcion = input("\nOpción: ").strip()
    
    if opcion == '0':
        print("\n¡Hasta luego!")
        return
    elif opcion.upper() == 'A':
        print("\n🚀 Ejecutando todos los ejemplos...\n")
        for _, (_, func) in ejemplos.items():
            try:
                func()
                input("\nPresione Enter para continuar...")
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("\nPresione Enter para continuar...")
    elif opcion in ejemplos:
        _, func = ejemplos[opcion]
        try:
            func()
        except Exception as e:
            print(f"\n❌ Error: {e}")
    else:
        print("\n❌ Opción inválida")


if __name__ == '__main__':
    menu_ejemplos()
