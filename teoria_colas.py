"""
Módulo de funciones analíticas para teoría de colas

Este módulo proporciona funciones para calcular métricas teóricas
de modelos de colas M/M/1 y M/M/c, útiles para validar simulaciones.
"""

import math
from typing import Dict, Optional


def analytical_mm1(lam: float, mu: float) -> Dict[str, float]:
    """
    Calcular métricas analíticas para modelo M/M/1
    
    Parámetros:
        lam: Tasa de llegadas (λ)
        mu: Tasa de servicio (μ)
    
    Retorna:
        Diccionario con métricas: rho, L, Lq, W, Wq
    
    Raises:
        ValueError: Si λ o μ no son positivos, o si ρ ≥ 1 (sistema inestable)
    """
    if lam <= 0:
        raise ValueError(f"λ debe ser positiva, recibido: {lam}")
    if mu <= 0:
        raise ValueError(f"μ debe ser positiva, recibido: {mu}")
    
    rho = lam / mu
    
    if rho >= 1.0:
        raise ValueError(
            f"Sistema M/M/1 inestable: ρ = {rho:.3f} ≥ 1. "
            f"No se pueden calcular métricas en estado estacionario."
        )
    
    # Fórmulas de estado estacionario para M/M/1
    L = rho / (1 - rho)              # Clientes promedio en el sistema
    Lq = (rho ** 2) / (1 - rho)      # Clientes promedio en cola
    W = 1 / (mu - lam)               # Tiempo promedio en el sistema
    Wq = rho / (mu - lam)            # Tiempo promedio en cola
    
    return {
        'rho': rho,
        'L': L,
        'Lq': Lq,
        'W': W,
        'Wq': Wq,
    }


def factorial(n: int) -> int:
    """Calcular factorial de n"""
    if n <= 1:
        return 1
    return math.factorial(n)


def analytical_mmc(lam: float, mu: float, c: int) -> Dict[str, float]:
    """
    Calcular métricas analíticas para modelo M/M/c
    
    Parámetros:
        lam: Tasa de llegadas (λ)
        mu: Tasa de servicio (μ)
        c: Número de servidores
    
    Retorna:
        Diccionario con métricas: rho, L, Lq, W, Wq, P0
    
    Raises:
        ValueError: Si parámetros inválidos o sistema inestable
    """
    if lam <= 0:
        raise ValueError(f"λ debe ser positiva, recibido: {lam}")
    if mu <= 0:
        raise ValueError(f"μ debe ser positiva, recibido: {mu}")
    if c <= 0:
        raise ValueError(f"c debe ser positivo, recibido: {c}")
    
    rho = lam / (c * mu)
    a = lam / mu  # Factor de utilización total
    
    if rho >= 1.0:
        raise ValueError(
            f"Sistema M/M/c inestable: ρ = {rho:.3f} ≥ 1. "
            f"No se pueden calcular métricas en estado estacionario."
        )
    
    # Calcular P0 (probabilidad de 0 clientes en el sistema)
    # Fórmula de Erlang-C
    sum_term = sum((a ** n) / factorial(n) for n in range(c))
    last_term = ((a ** c) / factorial(c)) * (1 / (1 - rho))
    P0 = 1 / (sum_term + last_term)
    
    # Probabilidad de espera (fórmula C de Erlang)
    C = ((a ** c) / factorial(c)) * (1 / (1 - rho)) * P0
    
    # Métricas de estado estacionario
    Lq = C * rho / (1 - rho)        # Clientes promedio en cola
    Wq = Lq / lam                    # Tiempo promedio en cola (Little's Law)
    W = Wq + (1 / mu)                # Tiempo promedio en sistema
    L = lam * W                      # Clientes promedio en sistema (Little's Law)
    
    return {
        'rho': rho,
        'L': L,
        'Lq': Lq,
        'W': W,
        'Wq': Wq,
        'P0': P0,
        'C': C,  # Probabilidad de espera (Erlang-C)
    }


def littles_law_check(L: float, lam: float, W: float, tolerance: float = 0.1) -> bool:
    """
    Verificar la Ley de Little: L = λ × W
    
    Parámetros:
        L: Número promedio de clientes en el sistema
        lam: Tasa de llegadas
        W: Tiempo promedio en el sistema
        tolerance: Tolerancia relativa para considerar válida la ley (10% por defecto)
    
    Retorna:
        True si se cumple la ley dentro de la tolerancia, False en caso contrario
    """
    if lam == 0:
        return L == 0
    
    expected_L = lam * W
    
    if expected_L == 0:
        return abs(L) < tolerance
    
    relative_error = abs(L - expected_L) / expected_L
    return relative_error <= tolerance


def compare_simulation_vs_theory(
    sim_metrics: Dict[str, float],
    theoretical_metrics: Dict[str, float],
    tolerance: float = 0.15
) -> Dict[str, Dict[str, float]]:
    """
    Comparar métricas de simulación vs teoría
    
    Parámetros:
        sim_metrics: Métricas obtenidas de la simulación
        theoretical_metrics: Métricas calculadas analíticamente
        tolerance: Tolerancia relativa (15% por defecto)
    
    Retorna:
        Diccionario con comparación por métrica: valor_sim, valor_teoria, error_rel, ok
    """
    results = {}
    
    for key in ['L', 'Lq', 'W', 'Wq', 'rho']:
        if key in sim_metrics and key in theoretical_metrics:
            sim_val = sim_metrics.get(key, 0.0)
            theo_val = theoretical_metrics.get(key, 0.0)
            
            if theo_val != 0:
                rel_error = abs(sim_val - theo_val) / theo_val
            else:
                rel_error = abs(sim_val - theo_val)
            
            ok = rel_error <= tolerance
            
            results[key] = {
                'simulacion': sim_val,
                'teoria': theo_val,
                'error_relativo': rel_error,
                'ok': ok,
            }
    
    return results


def print_comparison(comparison: Dict[str, Dict[str, float]]):
    """
    Imprimir comparación de forma legible
    
    Parámetros:
        comparison: Resultado de compare_simulation_vs_theory()
    """
    print("\n" + "="*80)
    print("COMPARACIÓN SIMULACIÓN vs TEORÍA")
    print("="*80)
    print(f"{'Métrica':<10} {'Simulación':<15} {'Teoría':<15} {'Error Rel.':<15} {'Válido':<10}")
    print("-"*80)
    
    for key, data in comparison.items():
        sim_val = data['simulacion']
        theo_val = data['teoria']
        error = data['error_relativo']
        ok = "✓" if data['ok'] else "✗"
        
        print(f"{key:<10} {sim_val:<15.4f} {theo_val:<15.4f} {error:<15.2%} {ok:<10}")
    
    print("="*80)
    
    # Resumen
    total = len(comparison)
    passed = sum(1 for d in comparison.values() if d['ok'])
    
    print(f"\nResumen: {passed}/{total} métricas dentro de tolerancia")
    if passed == total:
        print("✓ La simulación coincide con la teoría")
    else:
        print("⚠ Algunas métricas difieren de la teoría (considere aumentar horizonte o warmup)")
    print()


if __name__ == '__main__':
    # Ejemplo de uso
    print("Ejemplo: Modelo M/M/1 con λ=0.6, μ=2.0")
    mm1_metrics = analytical_mm1(lam=0.6, mu=2.0)
    print(f"ρ = {mm1_metrics['rho']:.3f}")
    print(f"L = {mm1_metrics['L']:.3f}")
    print(f"Lq = {mm1_metrics['Lq']:.3f}")
    print(f"W = {mm1_metrics['W']:.3f}")
    print(f"Wq = {mm1_metrics['Wq']:.3f}")
    
    print("\nVerificación de Ley de Little:")
    is_valid = littles_law_check(
        L=mm1_metrics['L'],
        lam=0.6,
        W=mm1_metrics['W']
    )
    print(f"L = λW: {'✓ Válido' if is_valid else '✗ Inválido'}")
    
    print("\n" + "="*80)
    print("Ejemplo: Modelo M/M/c con λ=0.7, μ=2.5, c=3")
    mmc_metrics = analytical_mmc(lam=0.7, mu=2.5, c=3)
    print(f"ρ = {mmc_metrics['rho']:.3f}")
    print(f"L = {mmc_metrics['L']:.3f}")
    print(f"Lq = {mmc_metrics['Lq']:.3f}")
    print(f"W = {mmc_metrics['W']:.3f}")
    print(f"Wq = {mmc_metrics['Wq']:.3f}")
    print(f"P0 = {mmc_metrics['P0']:.3f}")
    print(f"C (Prob. espera) = {mmc_metrics['C']:.3f}")
