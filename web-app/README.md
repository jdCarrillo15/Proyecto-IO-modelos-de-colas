# 🎯 Sistema Interactivo de Simulación de Colas

## 📋 Descripción

Aplicación web interactiva para simular y visualizar modelos de teoría de colas en tiempo real. Ofrece una experiencia visual atractiva tipo Cisco Packet Tracer, sin necesidad de instalar Python ni editar código.

## ✨ Características Principales

### 🎨 Interfaz Moderna
- **Diseño Glassmorphism**: Interfaz moderna con efectos de vidrio esmerilado
- **Tema Claro/Oscuro**: Cambia entre temas según tu preferencia
- **Responsive**: Funciona perfectamente en desktop, tablet y móvil
- **Animaciones Fluidas**: Transiciones y animaciones suaves con GSAP

### 📊 Modelos Soportados
1. **M/M/1**: Un servidor, capacidad infinita
2. **M/M/c**: Múltiples servidores, capacidad infinita
3. **M/M/k/1**: Un servidor, capacidad limitada
4. **M/M/k/c**: Múltiples servidores, capacidad limitada

### 🔧 Funcionalidades

#### Panel de Configuración
- ✅ Selector de modelos con tabs elegantes
- ✅ Sliders interactivos para parámetros (λ, μ, c, k)
- ✅ Indicador de estabilidad en tiempo real
- ✅ Gauge visual para visualización de ρ
- ✅ Validación automática de parámetros
- ✅ Advertencias para sistemas inestables

#### Visualización Animada
- ✅ Red de colas tipo diagrama de flujo
- ✅ Clientes animados con movimiento suave
- ✅ Nodos de llegada, cola y servidores
- ✅ Métricas en vivo en overlay transparente
- ✅ Controles de velocidad (0.5x a 10x)
- ✅ Barra de progreso de simulación

#### Métricas en Tiempo Real
- ✅ Utilización del sistema (ρ)
- ✅ Clientes en sistema (L) y cola (Lq)
- ✅ Tiempos promedio W y Wq
- ✅ Comparación con teoría (M/M/1 y M/M/c)
- ✅ Estadísticas acumuladas

#### Gráficos Interactivos
- ✅ Series temporales de L(t) y Lq(t)
- ✅ Distribución de tiempos de espera
- ✅ Actualización en tiempo real
- ✅ Charts.js para visualización

#### Exportación de Resultados
- ✅ Descarga en formato JSON
- ✅ Generación de reporte HTML standalone
- ✅ Datos completos de la simulación

#### Tutorial Interactivo
- ✅ Guía paso a paso para nuevos usuarios
- ✅ Explicación de parámetros y métricas
- ✅ Tooltips informativos

## 🚀 Cómo Usar

### Opción 1: Abrir Directamente (Recomendado)
1. Navega a la carpeta `web-app`
2. Abre el archivo `index.html` en tu navegador favorito
3. ¡Listo! La aplicación está completamente funcional sin servidor

### Opción 2: Con Servidor Local (Opcional)
Si prefieres usar un servidor local:

```bash
# Con Python 3
cd web-app
python -m http.server 8000

# Con Node.js
npx http-server web-app -p 8000
```

Luego abre `http://localhost:8000` en tu navegador.

## 📖 Guía de Uso Rápido

### 1. Seleccionar Modelo
Haz clic en uno de los tabs: M/M/1, M/M/c, M/M/k/1 o M/M/k/c

### 2. Ajustar Parámetros
- **λ (Lambda)**: Tasa de llegadas (clientes/tiempo)
- **μ (Mu)**: Tasa de servicio (clientes/tiempo/servidor)
- **c**: Número de servidores (para M/M/c y M/M/k/c)
- **k**: Capacidad máxima del sistema (para M/M/k/1 y M/M/k/c)

### 3. Verificar Estabilidad
- 🟢 **Verde (ρ < 0.7)**: Sistema óptimo
- 🟡 **Amarillo (0.7 ≤ ρ < 0.9)**: Aceptable
- 🟠 **Naranja (0.9 ≤ ρ < 1.0)**: Crítico
- 🔴 **Rojo (ρ ≥ 1.0)**: Inestable

### 4. Ejecutar Simulación
Haz clic en "▶ Ejecutar Simulación" y observa:
- Animación de clientes moviéndose por el sistema
- Actualización de métricas en tiempo real
- Gráficos dinámicos de series temporales

### 5. Ver Resultados
Al finalizar, aparecerá un modal con:
- Resumen de métricas finales
- Comparación con teoría (si está habilitada)
- Opciones de exportación

## 🎓 Conceptos de Teoría de Colas

### Notación de Kendall (A/B/c/k)
- **A**: Distribución de llegadas (M = Markoviana/Exponencial)
- **B**: Distribución de servicio (M = Markoviana/Exponencial)
- **c**: Número de servidores
- **k**: Capacidad del sistema (omitido si es infinita)

### Métricas Principales
- **ρ (Rho)**: Utilización = λ/(c·μ). Debe ser < 1 para estabilidad
- **L**: Número promedio de clientes en el sistema
- **Lq**: Número promedio de clientes en la cola
- **W**: Tiempo promedio en el sistema
- **Wq**: Tiempo promedio en la cola

### Ley de Little
```
L = λ · W
Lq = λ · Wq
```

## 🛠️ Arquitectura Técnica

### Estructura de Archivos
```
web-app/
├── index.html              # Página principal
├── css/
│   ├── main.css           # Estilos base y layout
│   ├── components.css     # Componentes UI
│   └── animations.css     # Animaciones y transiciones
├── js/
│   ├── main.js           # Punto de entrada
│   └── modules/
│       ├── config.js         # Gestión de configuración
│       ├── simulation-engine.js  # Motor de simulación
│       ├── visualization.js      # Animación canvas
│       ├── metrics.js           # Cálculo de métricas
│       ├── charts.js           # Gráficos Chart.js
│       ├── ui.js              # Gestión de UI
│       ├── export.js         # Exportación de datos
│       └── tutorial.js       # Tutorial interactivo
└── assets/                # Recursos adicionales
```

### Tecnologías Utilizadas
- **HTML5 Canvas**: Para animaciones de red
- **CSS3**: Variables, Grid, Flexbox, Glassmorphism
- **JavaScript ES6+**: Módulos, async/await, clases
- **Chart.js 4.4**: Gráficos interactivos
- **GSAP 3.12**: Animaciones fluidas
- **FileSaver.js**: Exportación de archivos

### Módulos Principales

#### ConfigManager
Gestiona la configuración de parámetros, validación y cálculos teóricos.

#### SimulationEngine
Motor de simulación por eventos discretos. Implementa la lógica de:
- Programación de eventos (llegadas, salidas)
- Manejo de cola y servidores
- Cálculo de métricas acumuladas
- Control de periodo de warmup

#### VisualizationManager
Renderiza la red animada en Canvas:
- Nodos de llegada, cola y servidores
- Clientes animados con movimiento suave
- Conexiones y flujo de datos

#### MetricsManager
Actualiza y muestra métricas en tiempo real en los paneles laterales.

#### ChartManager
Gestiona los gráficos interactivos con Chart.js.

#### UIManager
Controla elementos de la interfaz: modales, toasts, tema, progreso.

#### ExportManager
Maneja la exportación a JSON y generación de reportes HTML.

#### TutorialManager
Proporciona el tutorial paso a paso para nuevos usuarios.

## 🎨 Personalización

### Cambiar Colores
Edita las variables CSS en `css/main.css`:
```css
:root {
    --color-primary: #2563EB;
    --color-success: #10B981;
    --color-warning: #F59E0B;
    --color-danger: #EF4444;
    /* ... más variables ... */
}
```

### Ajustar Velocidades de Animación
En `js/modules/simulation-engine.js`:
```javascript
const dt = 0.016 * this.speed; // Modifica 0.016 para cambiar velocidad base
```

### Modificar Gráficos
En `js/modules/charts.js`, personaliza las configuraciones de Chart.js.

## 📊 Ejemplos de Uso

### Ejemplo 1: Sistema Ligero (M/M/1)
- λ = 0.5
- μ = 1.0
- ρ = 0.5 (óptimo)

### Ejemplo 2: Sistema Moderado (M/M/2)
- λ = 1.5
- μ = 1.0
- c = 2
- ρ = 0.75 (aceptable)

### Ejemplo 3: Sistema Crítico (M/M/1)
- λ = 0.9
- μ = 1.0
- ρ = 0.9 (crítico)

### Ejemplo 4: Con Capacidad Limitada (M/M/10/2)
- λ = 1.8
- μ = 1.0
- c = 2
- k = 10
- Habrá rechazos cuando el sistema esté lleno

## 🐛 Solución de Problemas

### La animación se ve lenta
- Reduce el horizonte de simulación
- Aumenta la velocidad de animación
- Cierra otras pestañas del navegador

### Los gráficos no se actualizan
- Verifica que estés en el periodo post-warmup
- Asegúrate de que la simulación esté corriendo

### Errores de validación
- Verifica que λ y μ sean positivos
- Asegúrate de que ρ < 1 (o acepta la advertencia)
- Comprueba que warmup < horizon

## 🔮 Futuras Mejoras

- [ ] Soporte para distribuciones G (General)
- [ ] Comparación entre múltiples configuraciones
- [ ] Exportación a CSV de series temporales
- [ ] Generación de gráficos en alta resolución
- [ ] Análisis estadístico avanzado
- [ ] Guardado de configuraciones favoritas
- [ ] Modo de presentación/demo
- [ ] Integración con datos reales

## 📝 Licencia

Este proyecto es parte del material educativo del curso de Investigación de Operaciones.

## 👥 Créditos

Desarrollado para el curso de Investigación de Operaciones - UPTC

## 📧 Contacto

Para reportar problemas o sugerencias, crea un issue en el repositorio del proyecto.

---

**¡Disfruta explorando la teoría de colas de forma interactiva! 🎉**
