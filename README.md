# Simulación animada de colas M/M/1, M/M/c, M/M/k/1 y M/M/k/c

Proyecto independiente que genera una animación 2x2 con clientes (muñequitos) entrando, esperando y siendo atendidos en servidores, en tiempo real.

## Requisitos

- Python 3.9+
- Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecutar

```bash
python sim_colas_animado.py
```

## Parámetros por defecto

- M/M/1: λ=2.0, μ=3.0
- M/M/c: λ=5.0, μ=3.0, c=3
- M/M/k/1: λ=6.0, μ=4.0, k=3
- M/M/k/c: λ=8.0, μ=4.0, k=2, c=2

Puedes editar `sim_colas_animado.py` para cambiar tasas y horizonte.

## Notas de diseño

- Simulación por eventos discretos con tiempos de llegada ~Poisson(λ) y servicio ~Exponencial(μ).
- Modelos:
  - M/M/1: 1 cola, 1 servidor.
  - M/M/c: 1 cola, c servidores.
  - M/M/k/1: k colas, 1 servidor por cola, asignación a cola más corta.
  - M/M/k/c: k colas, c servidores por cola, asignación a cola más corta.
- Animación:
  - Panel 2x2 con métrica "En sistema" como línea temporal.
  - Muñequitos (cabeza y cuerpo) se generan y posicionan según la ocupación.
  - Cuadros de servidores a la derecha del panel.
