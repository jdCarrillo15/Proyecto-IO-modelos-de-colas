# 📊 Sistema de Simulación de Colas - Proyecto IO

Proyecto completo de simulación de teoría de colas con **aplicación web interactiva** y scripts Python avanzados para el curso de Investigación de Operaciones - UPTC.

---

## 🚀 Inicio Rápido (3 pasos)

### Opción 1: Aplicación Web (Sin Instalación) ⭐

1. Navega a la carpeta `web-app/`
2. Abre `index.html` en tu navegador
3. ¡Listo! Configura y simula

**Alternativa:** Abre `INICIO.html` en la raíz para ver la página de bienvenida.

### Opción 2: Scripts Python (Para Análisis Avanzado)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar simulación
python sim_colas_animado.py

# 3. Ejecutar tests
python test_modelos.py
```

---

## 🌟 Aplicación Web Interactiva

**🎉 Simula teoría de colas sin instalar Python!**

### ✨ Características Principales
- 🎨 **Interfaz moderna** con diseño glassmorphism profesional
- 📊 **4 modelos de cola** (M/M/1, M/M/c, M/M/k/1, M/M/k/c)
- 🎬 **Animación en tiempo real** con clientes moviéndose por el sistema
- 📈 **Gráficos dinámicos** que se actualizan durante la simulación
- ⚙️ **Configuración interactiva** con sliders y validación automática
- 🎯 **Indicador de estabilidad** con gauge visual para ρ
- 💾 **Exportación completa** a JSON y reportes HTML
- 🎓 **Tutorial integrado** paso a paso para principiantes
- 🌓 **Tema claro/oscuro** según preferencia
- 📱 **Totalmente responsive** (desktop, tablet, móvil)

### 🎯 Ventajas
- ❌ **Sin instalación** - Solo navegador web moderno
- 📚 **Educativo** - Visualiza conceptos de teoría de colas
- ⚡ **Rápido** - Resultados en tiempo real
- 💼 **Profesional** - Diseño moderno y limpio

## 📁 Estructura del Proyecto

```
Proyecto-IO-modelos-de-colas/
├── 🌐 web-app/                      # ⭐ APLICACIÓN WEB INTERACTIVA
│   ├── index.html                   # Página principal
│   ├── README.md                    # Documentación técnica
│   ├── css/
│   │   ├── main.css                 # Estilos base y layout
│   │   ├── components.css           # Componentes UI
│   │   └── animations.css           # Animaciones y transiciones
│   └── js/
│       ├── main.js                  # Aplicación principal
│       └── modules/
│           ├── config.js            # Configuración y validación
│           ├── simulation-engine.js # Motor de simulación
│           ├── visualization.js     # Animación canvas
│           ├── metrics.js           # Métricas en tiempo real
│           ├── charts.js            # Gráficos Chart.js
│           ├── ui.js                # Gestión de interfaz
│           ├── export.js            # Exportación de datos
│           └── tutorial.js          # Tutorial interactivo
│
├── 🐍 Scripts Python
│   ├── teoria_colas.py              # Funciones analíticas (M/M/1, M/M/c)
│   ├── sim_colas_animado.py         # Simulación con matplotlib
│   ├── visualizaciones.py           # Gráficos avanzados
│   ├── test_modelos.py              # Tests unitarios
│   ├── ejemplos_uso.py              # Ejemplos de uso y tutorial
│   └── animacion-comparacion.py     # Comparación animada de modelos
│
├── 📚 Documentación
│   ├── README.md                    # Este archivo
│   └── INICIO.html                  # Página de bienvenida
│
├── requirements.txt                 # Dependencias Python
└── .gitignore                       # Archivos ignorados por git
```

## 🎯 ¿Qué Herramienta Usar?

| Necesidad | Herramienta | Ventaja Principal |
|-----------|-------------|-------------------|
| **Aprender conceptos** | 🌐 App Web | Visual e interactivo |
| **Demos/Presentaciones** | 🌐 App Web | Sin instalación |
| **Análisis básico** | 🌐 App Web | Resultados rápidos |
| **Investigación avanzada** | 🐍 Python | Análisis detallado |
| **Extensiones/Modificaciones** | 🐍 Python | Código abierto |
| **Tests automatizados** | 🐍 Python | Suite completa |

## 🚀 Características del Proyecto

### Aplicación Web (NUEVO) 🌐
- ✅ **Sin instalación**: Funciona en el navegador
- ✅ **Interfaz moderna**: Diseño glassmorphism profesional
- ✅ **Visualización animada**: Red de colas con clientes moviéndose
- ✅ **Configuración interactiva**: Sliders y controles intuitivos
- ✅ **Validación en tiempo real**: Indicador de estabilidad
- ✅ **Métricas dinámicas**: Actualización continua durante simulación
- ✅ **Gráficos interactivos**: Series temporales y distribuciones
- ✅ **Comparación con teoría**: Para M/M/1 y M/M/c
- ✅ **Tutorial integrado**: Guía paso a paso
- ✅ **Exportación completa**: JSON y reportes HTML

### Scripts Python (Original) 🐍
- ✅ **Simulación por eventos discretos** con distribuciones exponenciales
- ✅ **Animación 2x2 en tiempo real** con matplotlib
- ✅ **Validación de parámetros** y advertencias de sistemas inestables
- ✅ **Periodo de warmup** para mejorar precisión de métricas
- ✅ **Política determinista** en asignación de colas (reproducible)
- ✅ **Exportación de resultados** en formato JSON
- ✅ **Comparación con teoría analítica** (M/M/1 y M/M/c)
- ✅ **Suite de pruebas unitarias** automatizadas
- ✅ **Visualizaciones avanzadas** post-simulación

## � Inicio Rápido

### Opción 1: Aplicación Web (Recomendado para Principiantes)

**No requiere instalación:**

1. Abre `web-app/index.html` en tu navegador
2. O abre `INICIO.html` para ver la página de bienvenida
3. Configura parámetros y ejecuta simulación
4. ¡Listo!

### Opción 2: Scripts Python (Para Desarrollo Avanzado)

**Requisitos:**
- Python 3.9+
- Bibliotecas: matplotlib, numpy

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar simulación animada
python sim_colas_animado.py

# 3. Ejecutar tests
python test_modelos.py

# 4. Generar visualizaciones
python visualizaciones.py
```

## 📖 Guías y Documentación

| Documento | Descripción |
|-----------|-------------|
| `INICIO.html` | Página de bienvenida con enlaces rápidos |
| `web-app/README.md` | Documentación de la aplicación web |
| `web-app/INSTRUCCIONES.md` | Guía detallada de uso |
| `GUIA_COMPLETA.md` | Comparación web vs Python y casos de uso |
| Este archivo | Visión general del proyecto |

---

## 💡 Ejemplos de Configuración

### Ejemplo 1: Sistema Ligero (Óptimo)
```
Modelo: M/M/1
λ = 0.5, μ = 1.0
ρ = 0.5 ✅ Óptimo
Resultado: Sistema fluido, pocas esperas
```

### Ejemplo 2: Sistema Moderado
```
Modelo: M/M/c
λ = 1.5, μ = 1.0, c = 2
ρ = 0.75 ⚠️ Aceptable  
Resultado: Algunas esperas, sistema estable
```

### Ejemplo 3: Sistema Crítico
```
Modelo: M/M/1
λ = 0.9, μ = 1.0
ρ = 0.9 🔶 Crítico
Resultado: Colas largas, tiempos altos
```

### Ejemplo 4: Con Capacidad Limitada
```
Modelo: M/M/k/c
λ = 1.8, μ = 1.0, c = 2, k = 10
Resultado: Habrá rechazos cuando esté lleno
```

---

## 🐛 Solución de Problemas

### Aplicación Web
- **No se ve nada**: Asegúrate de abrir `web-app/index.html`
- **Errores en consola**: Verifica conexión a internet (librerías CDN)
- **Animación lenta**: Reduce horizonte o aumenta velocidad

### Scripts Python
- **Error de importación**: `pip install -r requirements.txt`
- **Versión de Python**: Requiere Python 3.9+

---

## � Próximos Pasos Sugeridos

1. **Explorar**: Prueba los 4 modelos con diferentes parámetros
2. **Comparar**: Activa "Comparar con Teoría" en M/M/1
3. **Experimentar**: Observa cómo ρ afecta el comportamiento
4. **Exportar**: Descarga resultados para análisis externo
5. **Personalizar**: Modifica colores y velocidades en CSS/JS

---

## 👥 Contribuciones

¿Quieres mejorar el proyecto?
- Nuevos modelos de cola
- Mejoras en la UI
- Optimización de rendimiento
- Documentación adicional
- Tests adicionales

---

## 📝 Licencia

Proyecto educativo para el curso de Investigación de Operaciones - UPTC.

---

## 📧 Contacto

Para preguntas o sugerencias, crea un issue en el repositorio.

---

**Desarrollado para el curso de Investigación de Operaciones - UPTC**  
*Sistema de Simulación de Colas © 2024*

---

## 📊 Estadísticas del Proyecto

| Métrica | Valor |
|---------|-------|
| **Líneas de código Python** | ~2,400 |
| **Líneas de código JavaScript** | ~2,500 |
| **Líneas de CSS** | ~1,700 |
| **Modelos implementados** | 4 (M/M/1, M/M/c, M/M/k/1, M/M/k/c) |
| **Archivos Python** | 6 |
| **Módulos JavaScript** | 8 |
| **Tests unitarios** | ✅ Incluidos |
| **Documentación** | ✅ Completa |

---

## 📊 Información Adicional (M/M/1 - Detalle)
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
from teoria_colas import analytical_mm1, print_comparison, compare_simulation_vs_theory
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
