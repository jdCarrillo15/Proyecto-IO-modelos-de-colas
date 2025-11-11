# 📘 Guía de Uso - Aplicación Web de Simulación de Colas

**Aplicación web interactiva** para simular modelos de teoría de colas sin instalación.

> 💡 **Para documentación general del proyecto**, ver [`README.md`](../README.md) en la raíz.

## 📦 Funcionalidades de la Aplicación

### ✅ Funcionalidades Implementadas

#### 1. **Interfaz de Usuario Moderna** 🎨
- Diseño glassmorphism con efectos de vidrio esmerilado
- Tema claro y oscuro alternables
- Layout responsive (desktop, tablet, móvil)
- Animaciones fluidas y transiciones suaves

#### 2. **4 Modelos de Cola** 📊
- **M/M/1**: Un servidor, capacidad infinita
- **M/M/c**: Múltiples servidores, capacidad infinita
- **M/M/k/1**: Un servidor, capacidad limitada
- **M/M/k/c**: Múltiples servidores, capacidad limitada

#### 3. **Panel de Configuración Interactivo** ⚙️
- Sliders para ajustar parámetros (λ, μ, c, k, horizonte, warmup)
- Valores en tiempo real
- Validación automática de estabilidad
- Gauge visual para ρ (utilización)
- Indicadores de estado (Óptimo, Aceptable, Crítico, Inestable)

#### 4. **Visualización Animada** 🎬
- Canvas con red de colas tipo diagrama de flujo
- Clientes animados con movimiento suave
- Nodos de llegada, cola y servidores
- Métricas en vivo en overlay transparente
- Control de velocidad (0.5x a 10x)
- Barra de progreso de simulación

#### 5. **Métricas en Tiempo Real** 📈
- ρ (Utilización del sistema)
- L (Clientes en sistema)
- Lq (Clientes en cola)
- W (Tiempo en sistema)
- Wq (Tiempo en cola)
- Comparación con teoría (M/M/1 y M/M/c)
- Estadísticas acumuladas

#### 6. **Gráficos Interactivos** 📊
- Series temporales con Chart.js
- Evolución de L(t) y Lq(t)
- Distribuciones de tiempos de espera
- Actualización en tiempo real

#### 7. **Exportación de Resultados** 💾
- Descarga en formato JSON
- Generación de reporte HTML standalone
- Datos completos de la simulación

#### 8. **Tutorial Interactivo** 🎓
- Guía paso a paso para nuevos usuarios
- Explicación de conceptos clave
- Tooltips informativos

## 📁 Estructura de Archivos Creados

```
web-app/
├── index.html                 # Página principal (ABRIR ESTE)
├── README.md                  # Documentación detallada
├── css/
│   ├── main.css              # Estilos base y layout
│   ├── components.css        # Componentes UI
│   └── animations.css        # Animaciones
└── js/
    ├── main.js               # Aplicación principal
    └── modules/
        ├── config.js         # Configuración y validación
        ├── simulation-engine.js  # Motor de simulación
        ├── visualization.js  # Animación canvas
        ├── metrics.js        # Gestión de métricas
        ├── charts.js         # Gráficos Chart.js
        ├── ui.js            # Gestión de interfaz
        ├── export.js        # Exportación de datos
        └── tutorial.js      # Tutorial paso a paso
```

## 🚀 Cómo Usar la Aplicación

### Método 1: Abrir Directamente (Recomendado)

1. **Navega a la carpeta `web-app`**
2. **Doble clic en `index.html`**
3. **¡La aplicación se abrirá en tu navegador predeterminado!**

### Método 2: Con Servidor Local (Opcional)

Si prefieres usar un servidor:

```bash
# Opción A: Python
cd web-app
python -m http.server 8000

# Opción B: Node.js
npx http-server web-app -p 8000

# Luego abre: http://localhost:8000
```

### Método 3: Usar el Archivo de Inicio

1. **Abre `INICIO.html` (en la raíz del proyecto)**
2. **Haz clic en "Abrir Aplicación"**

## 📖 Guía de Uso Paso a Paso

### Paso 1: Primera Ejecución
1. Abre `web-app/index.html` en tu navegador
2. Haz clic en el ícono de tutorial (🎓) en la esquina superior derecha
3. Sigue la guía paso a paso

### Paso 2: Configurar una Simulación
1. **Selecciona un modelo**: Haz clic en M/M/1 (recomendado para empezar)
2. **Ajusta parámetros**:
   - **λ (Lambda)**: Tasa de llegadas (ejemplo: 0.8)
   - **μ (Mu)**: Tasa de servicio (ejemplo: 1.0)
   - **Horizonte**: Tiempo de simulación (ejemplo: 1000)
   - **Warmup**: Periodo de calentamiento (ejemplo: 200)
3. **Verifica estabilidad**: Observa el gauge de ρ
   - 🟢 Verde: ρ < 0.7 (Óptimo)
   - 🟡 Amarillo: 0.7 ≤ ρ < 0.9 (Aceptable)
   - 🟠 Naranja: 0.9 ≤ ρ < 1.0 (Crítico)
   - 🔴 Rojo: ρ ≥ 1.0 (Inestable)

### Paso 3: Ejecutar Simulación
1. Haz clic en "▶ Ejecutar Simulación"
2. Observa la animación de clientes moviéndose
3. Controla la velocidad con el selector (1x, 2x, 5x, etc.)
4. Pausa/reanuda si es necesario

### Paso 4: Analizar Resultados
1. Observa las métricas en el panel derecho
2. Cambia entre los tabs de gráficos:
   - **Series Temporales**: Evolución de L(t) y Lq(t)
   - **Distribuciones**: Histograma de tiempos de espera
3. Espera a que la simulación termine

### Paso 5: Ver Resultados Finales
1. Aparecerá un modal con el resumen
2. Revisa las métricas finales
3. Si habilitaste "Comparar con Teoría", verás la tabla comparativa
4. Exporta los resultados:
   - **JSON**: Para análisis externo
   - **HTML**: Reporte standalone

## 💡 Ejemplos de Configuración

### Ejemplo 1: Sistema Ligero (Óptimo)
```
Modelo: M/M/1
λ = 0.5
μ = 1.0
ρ = 0.5 ✅ Óptimo
```
**Resultado esperado**: Pocas esperas, sistema fluido

### Ejemplo 2: Sistema Moderado (Aceptable)
```
Modelo: M/M/2
λ = 1.5
μ = 1.0
c = 2
ρ = 0.75 ⚠️ Aceptable
```
**Resultado esperado**: Algunas esperas, sistema estable

### Ejemplo 3: Sistema Crítico
```
Modelo: M/M/1
λ = 0.9
μ = 1.0
ρ = 0.9 🔶 Crítico
```
**Resultado esperado**: Colas largas, tiempos altos

### Ejemplo 4: Con Capacidad Limitada
```
Modelo: M/M/10/2
λ = 1.8
μ = 1.0
c = 2
k = 10
```
**Resultado esperado**: Habrá rechazos cuando el sistema esté lleno

## 🎯 Características Técnicas

### Tecnologías Utilizadas
- **HTML5 Canvas**: Animación de red
- **CSS3**: Variables, Grid, Flexbox, Glassmorphism
- **JavaScript ES6+**: Módulos, clases, async/await
- **Chart.js 4.4**: Gráficos interactivos
- **GSAP 3.12**: Animaciones fluidas
- **FileSaver.js**: Exportación de archivos

### Arquitectura Modular
- **ConfigManager**: Gestión de configuración y validación
- **SimulationEngine**: Motor de simulación por eventos discretos
- **VisualizationManager**: Animación canvas
- **MetricsManager**: Cálculo y visualización de métricas
- **ChartManager**: Gráficos dinámicos
- **UIManager**: Gestión de interfaz y temas
- **ExportManager**: Exportación de datos
- **TutorialManager**: Sistema de tutorial

### Rendimiento
- Simulación optimizada para 60 FPS
- Submuestreo de datos para gráficos
- Animaciones con requestAnimationFrame
- Buffer circular para series temporales

## 🔧 Personalización

### Cambiar Tema por Defecto
En `js/modules/ui.js`, línea 4:
```javascript
this.theme = 'dark'; // Cambiar a 'light' para tema claro
```

### Ajustar Colores
En `css/main.css`, variables CSS:
```css
:root {
    --color-primary: #2563EB;  /* Cambia este valor */
    --color-success: #10B981;
    /* ... más colores ... */
}
```

### Modificar Velocidad Base
En `js/modules/simulation-engine.js`:
```javascript
const dt = 0.016 * this.speed; // Cambia 0.016 para velocidad base
```

## 🐛 Solución de Problemas

### Problema: No se ve nada
**Solución**: Asegúrate de abrir `web-app/index.html`, no otros archivos HTML

### Problema: Errores en consola
**Solución**: 
1. Abre DevTools (F12)
2. Ve a la pestaña Console
3. Verifica que todos los archivos JS se carguen correctamente
4. Asegúrate de tener conexión a internet (para CDN de Chart.js, GSAP)

### Problema: Animación lenta
**Solución**:
- Reduce el horizonte de simulación a 500-1000
- Aumenta la velocidad a 5x o 10x
- Cierra otras pestañas del navegador

### Problema: Gráficos no aparecen
**Solución**: Verifica tu conexión a internet (Chart.js se carga desde CDN)

## 📚 Recursos Adicionales

### Documentación
- **web-app/README.md**: Documentación detallada de la aplicación web
- **GUIA_COMPLETA.md**: Comparación web vs Python y casos de uso

### Archivos de Ayuda
- **INICIO.html**: Página de bienvenida con enlaces rápidos
- Este archivo: Resumen de implementación

### Para Aprender Más
- Teoría de colas: Lee los comentarios en `js/modules/config.js`
- Simulación por eventos: Revisa `js/modules/simulation-engine.js`
- Animaciones: Explora `js/modules/visualization.js`

## ✨ Próximos Pasos Sugeridos

1. **Explorar la aplicación**:
   - Prueba los 4 modelos diferentes
   - Experimenta con distintos valores de λ y μ
   - Observa cómo afecta ρ al comportamiento

2. **Comparar con teoría**:
   - Activa "Comparar con Teoría" en M/M/1
   - Ejecuta simulaciones largas (horizonte 5000+)
   - Verifica que los resultados converjan

3. **Exportar y analizar**:
   - Descarga resultados en JSON
   - Ábrelos en Excel o Python para análisis adicional

4. **Personalizar**:
   - Cambia colores en CSS
   - Ajusta velocidades de animación
   - Modifica textos y etiquetas

5. **Compartir**:
   - La carpeta `web-app` es completamente autónoma
   - Puedes compartirla por completo
   - O subirla a un hosting estático (GitHub Pages, Netlify, etc.)

## 🎓 Para Estudiantes

Esta aplicación es ideal para:
- ✅ Entender visualmente teoría de colas
- ✅ Experimentar con parámetros
- ✅ Validar cálculos teóricos
- ✅ Crear presentaciones con capturas de pantalla
- ✅ Comparar diferentes configuraciones

## 👨‍💻 Para Desarrolladores

Si quieres extender la aplicación:
- Todos los módulos son independientes
- Código bien comentado
- Estructura clara y mantenible
- Fácil de agregar nuevos modelos
- Preparado para agregar más gráficos

## 📊 Métricas del Proyecto

- **Archivos creados**: 13
- **Líneas de código**: ~3,500+
- **Módulos JavaScript**: 8
- **Archivos CSS**: 3
- **Modelos implementados**: 4
- **Gráficos**: 2 tipos
- **Temas**: 2 (claro/oscuro)

## 🎉 ¡Listo para Usar!

La aplicación está **100% funcional** y lista para usar.

### Inicio Rápido:
1. Abre `web-app/index.html`
2. Selecciona M/M/1
3. Haz clic en "▶ Ejecutar Simulación"
4. ¡Disfruta!

### ¿Necesitas Ayuda?
- Haz clic en el ícono de tutorial (🎓) en la app
- Lee `web-app/README.md` para detalles técnicos
- Revisa `GUIA_COMPLETA.md` para casos de uso

---

## 🌟 Características Destacadas

- ❌ **Sin instalación**: Solo abre y usa
- 🎨 **Visualmente atractivo**: Diseño moderno profesional
- 📊 **Educativo**: Aprende mientras simulas
- 💾 **Exportable**: Guarda tus resultados
- 📱 **Responsive**: Funciona en cualquier dispositivo
- 🌓 **Temas**: Claro y oscuro
- ⚡ **Rápido**: Simulación optimizada
- 🎓 **Tutorial incluido**: Para nuevos usuarios

---

**¡Gracias por usar el Sistema de Simulación de Colas! 🎊**

*Desarrollado para el curso de Investigación de Operaciones - UPTC*
