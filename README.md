# Simulación Animada de Modelos de Colas: M/M/1, M/M/c, M/M/k/1 y M/M/k/c

Proyecto de simulación por eventos discretos con animación visual interactiva para análisis de sistemas de colas.

## 🚀 Características

- ✅ **Simulación por eventos discretos** con distribuciones exponenciales
- ✅ **Animación 2x2 en tiempo real** con representación visual de clientes
- ✅ **Validación de parámetros** y advertencias de sistemas inestables
- ✅ **Periodo de warmup** para mejorar precisión de métricas
- ✅ **Política determinista** en asignación de colas (reproducible)
- ✅ **Exportación de resultados** en formato JSON
- ✅ **Comparación con teoría analítica** (M/M/1 y M/M/c)
- ✅ **Suite de pruebas unitarias** automatizadas
- ✅ **Visualizaciones avanzadas** post-simulación

## 📋 Requisitos

- Python 3.9+
- Bibliotecas: matplotlib, numpy

```bash
pip install -r requirements.txt
```

## 🎯 Ejecución

### Simulación básica con animación
```bash
python sim_colas_animado.py
```

### Ejecutar pruebas unitarias
```bash
python test_modelos.py
```

### Generar visualizaciones avanzadas
```bash
python visualizaciones.py
```

### Calcular métricas analíticas
```bash
python teoría_colas.py
```

## 📊 Modelos Implementados

### M/M/1
- **Descripción**: 1 cola, 1 servidor
- **Parámetros**: λ (llegadas), μ (servicio)
- **Estabilidad**: ρ = λ/μ < 1

### M/M/c
- **Descripción**: 1 cola, c servidores
- **Parámetros**: λ, μ, c
- **Estabilidad**: ρ = λ/(c·μ) < 1

### M/M/k/1
- **Descripción**: k colas paralelas, 1 servidor por cola
- **Parámetros**: λ, μ, k
- **Asignación**: Cola más corta (determinista)

### M/M/k/c
- **Descripción**: k colas, c servidores por cola
- **Parámetros**: λ, μ, k, c
- **Asignación**: Cola más corta (determinista)

## 📁 Estructura del Proyecto

```
Proyecto-IO-modelos-de-colas/
├── sim_colas_animado.py      # Simulación principal con animación
├── teoría_colas.py            # Funciones analíticas (M/M/1, M/M/c)
├── test_modelos.py            # Suite de pruebas unitarias
├── visualizaciones.py         # Herramientas de visualización avanzada
├── animacion-comparacion.py   # Comparación visual básica
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Documentación

clase/
├── comparacion.py             # Comparación de modelos (versión simple)
└── comparacion2.py            # Variantes adicionales
```

## 🔬 Ejemplo de Uso Completo

```python
from sim_colas_animado import MM1
from teoría_colas import analytical_mm1, print_comparison, compare_simulation_vs_theory
from visualizaciones import VisualizadorColas

# 1. Crear y ejecutar simulación
sim = MM1(lam=0.6, mu=2.0, horizon=10000, warmup=1000)

while sim.time < sim.horizon:
    sim.step()

# 2. Exportar resultados
sim.export_results("resultados.json")

# 3. Comparar con teoría
st = sim.state()
sim_metrics = {
    'L': st['l_avg'],
    'Lq': st['lq_avg'],
    'W': st['w_avg'],
    'Wq': st['wq_avg'],
    'rho': st['rho'],
}

theo_metrics = analytical_mm1(lam=0.6, mu=2.0)
comparison = compare_simulation_vs_theory(sim_metrics, theo_metrics)
print_comparison(comparison)

# 4. Generar visualizaciones
viz = VisualizadorColas(sim, "M/M/1 (λ=0.6, μ=2.0)")
viz.generar_reporte_completo(incluir_teoria=True)
```

## 📈 Métricas Calculadas

- **ρ**: Utilización del sistema (λ/μ para M/M/1, λ/(c·μ) para M/M/c)
- **L**: Número promedio de clientes en el sistema
- **Lq**: Número promedio de clientes en cola
- **W**: Tiempo promedio en el sistema
- **Wq**: Tiempo promedio en cola

### Fórmulas Analíticas (M/M/1)

$$\rho = \frac{\lambda}{\mu}$$

$$L = \frac{\rho}{1-\rho}$$

$$L_q = \frac{\rho^2}{1-\rho}$$

$$W = \frac{1}{\mu - \lambda}$$

$$W_q = \frac{\rho}{\mu - \lambda}$$

## ⚙️ Parámetros de Configuración

### Simulación básica
```python
MM1(lam=0.6, mu=2.0, horizon=10000, warmup=1000)
```

### Animación
```python
specs = [
    ModelSpec('M/M/1', 'mm1', {'lam': 0.6, 'mu': 2.0}),
    ModelSpec('M/M/c', 'mmc', {'lam': 0.7, 'mu': 2.5, 'c': 3}),
    ModelSpec('M/M/k/1', 'mmk1', {'lam': 0.8, 'mu': 2.5, 'k': 3}),
    ModelSpec('M/M/k/c', 'mmkc', {'lam': 0.9, 'mu': 2.5, 'k': 2, 'c': 2}),
]
anim = AnimatedComparison(specs, horizon=120.0, seed=42)
anim.run(dt=0.2, frames=500, interval_ms=100)
```

## 🧪 Testing

El módulo `test_modelos.py` incluye:

- ✅ Validación de parámetros inválidos
- ✅ Verificación de warnings en sistemas inestables
- ✅ Pruebas de utilización en estado estacionario
- ✅ Validación de Ley de Little (L = λW)
- ✅ Comparación con resultados analíticos
- ✅ Verificación de mejora con warmup
- ✅ Pruebas de reproducibilidad (determinismo)
- ✅ Pruebas de exportación JSON

```bash
python test_modelos.py
# ✓ Pruebas ejecutadas: 15
# ✓ Exitosas: 15
```

## 📖 Referencias

- Gross, D., & Harris, C. M. (1998). *Fundamentals of Queueing Theory*.
- Kleinrock, L. (1975). *Queueing Systems, Volume 1: Theory*.
- Ley de Little: L = λW (conservación de flujo)
