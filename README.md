# 🎯 Sistema de Simulación de Colas - Proyecto IO

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![License](https://img.shields.io/badge/license-Educational-green.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![JavaScript](https://img.shields.io/badge/javascript-ES6+-yellow.svg)

**Simulador interactivo de teoría de colas con aplicación web moderna y análisis avanzado en Python**

[🚀 Inicio Rápido](#-inicio-rápido) • [📖 Manual de Usuario](MANUAL_USUARIO.md) • [🎓 Documentación](#-documentación) • [🐛 Reportar Bug](../../issues)

</div>

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Características Principales](#-características-principales)
- [Inicio Rápido](#-inicio-rápido)
- [Modelos Implementados](#-modelos-implementados)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Documentación](#-documentación)
- [Ejemplos de Uso](#-ejemplos-de-uso)
- [Requisitos del Sistema](#-requisitos-del-sistema)
- [Instalación](#-instalación)
- [Guía de Uso](#-guía-de-uso)
- [Casos de Uso Prácticos](#-casos-de-uso-prácticos)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Testing y Validación](#-testing-y-validación)
- [Solución de Problemas](#-solución-de-problemas)
- [Contribución](#-contribución)
- [Créditos y Licencia](#-créditos-y-licencia)

---

## 🎓 Descripción General

El **Sistema de Simulación de Colas** es un proyecto completo para el estudio y análisis de sistemas de teoría de colas, desarrollado para el curso de **Investigación de Operaciones** de la UPTC. 

Combina una **aplicación web moderna** con animaciones en tiempo real y **herramientas Python avanzadas** para análisis detallado, proporcionando una solución integral para estudiantes, profesores e investigadores.

### ¿Por qué usar este simulador?

- ✅ **Aprendizaje Visual**: Observa cómo funcionan los sistemas de colas en tiempo real
- ✅ **Validación Teórica**: Compara resultados de simulación con fórmulas analíticas
- ✅ **Sin Instalación**: La versión web funciona directamente en el navegador
- ✅ **Análisis Profundo**: Scripts Python para investigación avanzada
- ✅ **Profesional**: Interfaz moderna con exportación de datos
- ✅ **Educativo**: Ideal para enseñanza e investigación académica

---

## ⭐ Características Principales

### 🌐 Aplicación Web Interactiva

<table>
<tr>
<td width="50%">

**Visualización**
- 🎬 Animación en tiempo real con clientes
- 📊 Gráficas dinámicas actualizadas en vivo
- 🎨 Interfaz moderna con diseño glassmorphism
- 🌓 Tema claro/oscuro
- 📱 Diseño responsive

</td>
<td width="50%">

**Funcionalidades**
- ⚙️ 4 modelos de cola implementados
- 🎯 Indicador visual de estabilidad (ρ)
- 📐 Comparación automática con teoría
- 💾 Exportación a JSON y HTML
- 🎓 Tutorial interactivo integrado

</td>
</tr>
</table>

### 🐍 Scripts Python Avanzados

- 🔬 Simulación por eventos discretos (DES)
- 📈 Animaciones 2x2 con matplotlib
- 🧪 Suite completa de tests unitarios
- 📊 Visualizaciones post-simulación
- 📐 Cálculos analíticos precisos
- 💾 Exportación de datos estructurados
- ⚡ Periodo de warmup configurable

---

## 🚀 Inicio Rápido

### Opción 1: Aplicación Web (Recomendada) ⚡

**¡Sin instalación! Solo necesitas un navegador web.**

```bash
# Clonar el repositorio
git clone https://github.com/jdCarrillo15/Proyecto-IO-modelos-de-colas.git

# Abrir la aplicación
cd Proyecto-IO-modelos-de-colas
# Doble clic en: web-app/index.html
# O abrir: INICIO.html
```

**Acceso directo:**
- 📁 `web-app/index.html` - Aplicación principal
- 🏠 `INICIO.html` - Página de bienvenida con enlaces

### Opción 2: Scripts Python (Para Desarrollo) 🔧

```bash
# 1. Clonar repositorio
git clone https://github.com/jdCarrillo15/Proyecto-IO-modelos-de-colas.git
cd Proyecto-IO-modelos-de-colas

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar simulación básica
python sim_colas_animado.py

# 4. Ejecutar tests
python test_modelos.py

# 5. Ver ejemplos de uso
python ejemplos_uso.py
```

---

## 📚 Modelos Implementados

### 1️⃣ M/M/1 - Un Servidor, Capacidad Infinita
```
Sistema: [Llegadas] → [Cola] → [Servidor] → [Salida]
Parámetros: λ (llegadas), μ (servicio)
Estabilidad: ρ = λ/μ < 1
Teoría: ✅ Disponible
```
**Casos de uso:** Cajero único, servidor web simple, puesto de peaje

### 2️⃣ M/M/c - Múltiples Servidores, Capacidad Infinita
```
Sistema: [Llegadas] → [Cola] → [S1|S2|...|Sc] → [Salida]
Parámetros: λ, μ, c (servidores)
Estabilidad: ρ = λ/(c×μ) < 1
Teoría: ✅ Disponible
```
**Casos de uso:** Call center, banco con varios cajeros, sistema multiprocesador

### 3️⃣ M/M/k/1 - Un Servidor, Capacidad Limitada
```
Sistema: [Llegadas] → [Cola (máx k)] → [Servidor] → [Salida]
          ↓ (si lleno)
       [Rechazado]
Parámetros: λ, μ, k (capacidad máxima)
Característica: Rechaza clientes cuando hay k en el sistema
```
**Casos de uso:** Sala de espera limitada, buffer con capacidad fija

### 4️⃣ M/M/k/c - Múltiples Servidores, Capacidad Limitada
```
Sistema: [Llegadas] → [Cola (máx k)] → [S1|S2|...|Sc] → [Salida]
          ↓ (si lleno)
       [Rechazado]
Parámetros: λ, μ, c (servidores), k (capacidad, k≥c)
Característica: Combina paralelismo con límite de capacidad
```
**Casos de uso:** Hospital con salas limitadas, restaurant con capacidad máxima

---

## 📁 Estructura del Proyecto

```
Proyecto-IO-modelos-de-colas/
│
├── 🌐 web-app/                          # APLICACIÓN WEB INTERACTIVA
│   ├── index.html                       # → Página principal
│   ├── README.md                        # Documentación técnica web
│   ├── INSTRUCCIONES.md                 # Guía detallada de uso
│   │
│   ├── css/
│   │   ├── main.css                     # Estilos base, layout, temas
│   │   ├── components.css               # Componentes UI (botones, cards)
│   │   ├── animations.css               # Animaciones y transiciones
│   │   └── fixes.css                    # Correcciones específicas
│   │
│   ├── js/
│   │   ├── main.js                      # ⭐ Orquestador principal
│   │   └── modules/
│   │       ├── config.js                # Gestión de configuración
│   │       ├── simulation-engine.js     # Motor de eventos discretos
│   │       ├── visualization.js         # Animación Canvas 2D
│   │       ├── metrics.js               # Cálculo de métricas en vivo
│   │       ├── charts.js                # Gráficas Chart.js
│   │       ├── ui.js                    # Gestión de interfaz
│   │       ├── export.js                # Exportación JSON/HTML
│   │       └── tutorial.js              # Tutorial interactivo
│   │
│   └── assets/                          # Recursos adicionales
│
├── 🐍 SCRIPTS PYTHON
│   ├── teoria_colas.py                  # ⭐ Funciones analíticas M/M/1, M/M/c
│   ├── sim_colas_animado.py            # ⭐ Simulación DES con matplotlib
│   ├── visualizaciones.py               # Gráficos avanzados
│   ├── test_modelos.py                  # Suite de tests unitarios
│   ├── ejemplos_uso.py                  # Ejemplos y tutorial
│   └── animacion-comparacion.py         # Comparación animada
│
├── 📚 DOCUMENTACIÓN
│   ├── README.md                        # ⭐ Este archivo (overview)
│   ├── MANUAL_USUARIO.md               # ⭐ Manual completo del usuario
│   ├── INICIO.html                      # Página de bienvenida
│   ├── GUIA_DEMO.md                    # Guía para demostrar el proyecto
│   ├── INICIO_RAPIDO.md                # Tutorial express
│   ├── CORRECCIONES_APLICADAS.md       # Log de correcciones
│   └── RESUMEN_EJECUTIVO.md            # Resumen del proyecto
│
├── requirements.txt                     # Dependencias Python
└── .gitignore                          # Archivos ignorados
```

---

## 📖 Documentación

| 📄 Documento | 📝 Descripción | 🎯 Audiencia |
|-------------|---------------|-------------|
| **[MANUAL_USUARIO.md](MANUAL_USUARIO.md)** | 📖 Manual completo con guías paso a paso | Todos los usuarios |
| **[INICIO.html](INICIO.html)** | 🏠 Página de bienvenida con acceso rápido | Nuevos usuarios |
| **[web-app/README.md](web-app/README.md)** | 🌐 Documentación técnica de la app web | Desarrolladores |
| **[web-app/INSTRUCCIONES.md](web-app/INSTRUCCIONES.md)** | 📋 Instrucciones detalladas de uso | Usuarios web |
| **[GUIA_DEMO.md](GUIA_DEMO.md)** | 🎬 Cómo demostrar el proyecto | Presentadores |
| **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** | ⚡ Tutorial express (5 minutos) | Principiantes |
| **[CORRECCIONES_APLICADAS.md](CORRECCIONES_APLICADAS.md)** | 🔧 Historial de correcciones | Desarrolladores |
| **Este archivo (README.md)** | 📚 Visión general del proyecto | Todos |

### 🎯 ¿Qué documento leer?

- 🆕 **Primera vez aquí?** → Empieza con [`INICIO.html`](INICIO.html) o [`MANUAL_USUARIO.md`](MANUAL_USUARIO.md)
- 🌐 **Vas a usar la app web?** → Lee [`web-app/INSTRUCCIONES.md`](web-app/INSTRUCCIONES.md)
- 🐍 **Vas a programar en Python?** → Revisa `ejemplos_uso.py`
- 🎓 **Vas a enseñar/demostrar?** → Consulta [`GUIA_DEMO.md`](GUIA_DEMO.md)
- ⚡ **Tienes prisa?** → Ve directo a [`INICIO_RAPIDO.md`](INICIO_RAPIDO.md)

---

## 💡 Ejemplos de Uso

### 🌐 Aplicación Web

#### Ejemplo 1: Sistema Óptimo (Poca Carga)
```
1. Abre web-app/index.html
2. Selecciona: M/M/1
3. Configura:
   λ = 0.5
   μ = 1.0
   Horizonte = 1000
   ✅ Comparar con teoría
4. Ejecutar Simulación

Resultado esperado:
✅ ρ = 0.50 (Verde - Óptimo)
✅ L ≈ 1.0
✅ Wq ≈ 0.5
✅ Error vs teoría < 5%
```

#### Ejemplo 2: Sistema con Múltiples Servidores
```
1. Selecciona: M/M/c
2. Configura:
   λ = 1.5
   μ = 1.0
   c = 2 servidores
   Horizonte = 1000
   ✅ Comparar con teoría
3. Ejecutar

Resultado esperado:
✅ ρ = 0.75 (Amarillo - Aceptable)
✅ 2 servidores visibles (S1, S2)
✅ L ≈ 2.5
✅ Menos cola que M/M/1 equivalente
```

#### Ejemplo 3: Sistema con Rechazos
```
1. Selecciona: M/M/k/c
2. Configura:
   λ = 1.8
   μ = 1.0
   c = 2 servidores
   k = 8 capacidad
   Horizonte = 1000
3. Ejecutar

Resultado esperado:
⚠️ Clientes rechazados: ~15%
⚠️ Tasa de rechazo visible
📊 L máximo = 8 (no crece más)
```

### 🐍 Scripts Python

#### Ejemplo Básico: M/M/1
```python
from sim_colas_animado import MM1

# Crear simulación
sim = MM1(lam=0.6, mu=2.0, horizon=10000, warmup=1000)

# Ejecutar
while sim.time < sim.horizon:
    sim.step()

# Ver resultados
state = sim.state()
print(f"ρ = {state['rho']:.3f}")
print(f"L = {state['l_avg']:.3f}")
print(f"Lq = {state['lq_avg']:.3f}")
print(f"W = {state['w_avg']:.3f}")
print(f"Wq = {state['wq_avg']:.3f}")

# Exportar
sim.export_results("resultados.json")
```

#### Ejemplo Avanzado: Comparación con Teoría
```python
from teoria_colas import analytical_mm1, compare_simulation_vs_theory

# Métricas de simulación
sim_metrics = {
    'L': 1.234,
    'Lq': 0.834,
    'W': 2.057,
    'Wq': 1.390,
    'rho': 0.600
}

# Calcular teoría
theo_metrics = analytical_mm1(lam=0.6, mu=1.0)

# Comparar
comparison = compare_simulation_vs_theory(sim_metrics, theo_metrics)

# Resultado: Muestra tabla con errores porcentuales
```

#### Ejemplo: Visualización Completa
```python
from visualizaciones import VisualizadorColas

# Crear visualizador
viz = VisualizadorColas(sim, "M/M/1 Test")

# Generar reporte completo
viz.generar_reporte_completo(incluir_teoria=True)
# Crea: timeseries, distribuciones, comparación
```

---

## 💻 Requisitos del Sistema

### 🌐 Para Aplicación Web

| Componente | Requisito |
|------------|-----------|
| **Navegador** | Chrome 90+, Edge 90+, Firefox 88+, Safari 14+ |
| **Sistema Operativo** | Windows 7+, macOS 10.12+, Linux (cualquier) |
| **RAM** | 2 GB mínimo, 4 GB recomendado |
| **Resolución** | 1280x720 mínimo, 1920x1080 recomendado |
| **Internet** | Solo para carga inicial (CDN) |

### 🐍 Para Scripts Python

| Componente | Versión |
|------------|---------|
| **Python** | 3.9 o superior |
| **NumPy** | 1.21+ |
| **Matplotlib** | 3.4+ |
| **Sistema Operativo** | Windows, macOS, Linux |

---

## 🔧 Instalación

### Opción A: Solo Aplicación Web (Recomendada)

**No requiere instalación de software adicional:**

```bash
# 1. Descargar proyecto
git clone https://github.com/jdCarrillo15/Proyecto-IO-modelos-de-colas.git

# 2. Navegar a la carpeta
cd Proyecto-IO-modelos-de-colas

# 3. Abrir en navegador
# - Doble clic en: web-app/index.html
# - O abrir: INICIO.html
```

### Opción B: Instalación Completa (Web + Python)

**Para análisis avanzado y desarrollo:**

```bash
# 1. Descargar proyecto
git clone https://github.com/jdCarrillo15/Proyecto-IO-modelos-de-colas.git
cd Proyecto-IO-modelos-de-colas

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Verificar instalación
python test_modelos.py

# 5. Ver ejemplos
python ejemplos_uso.py
```

### Servidor Local (Opcional)

Si prefieres usar un servidor web local:

```bash
# Con Python
cd web-app
python -m http.server 8000
# Abrir: http://localhost:8000

# Con Node.js
npm install -g http-server
cd web-app
http-server -p 8000
```

---

## 📱 Guía de Uso

### 🌐 Usar la Aplicación Web

1. **Abrir**: `web-app/index.html` o `INICIO.html`
2. **Seleccionar modelo**: Haz clic en M/M/1, M/M/c, M/M/k/1 o M/M/k/c
3. **Configurar parámetros**: 
   - Ajusta λ (llegadas) y μ (servicio)
   - Configura c (servidores) y k (capacidad) si aplica
   - Establece horizonte y warmup
4. **Verificar estabilidad**: Observa el gauge (ρ < 1 = estable)
5. **Ejecutar**: Clic en "▶️ Ejecutar Simulación"
6. **Observar**: 
   - Animación de clientes en tiempo real
   - Gráficas que se actualizan
   - Métricas en el panel derecho
7. **Resultados**: Al finalizar, aparece modal con:
   - Métricas finales
   - Comparación con teoría (si aplica)
   - Gráficas completas
8. **Exportar** (opcional):
   - 💾 Descargar JSON con datos
   - 📄 Generar reporte HTML

**📖 Para guía detallada, ver [MANUAL_USUARIO.md](MANUAL_USUARIO.md)**

### 🐍 Usar Scripts Python

#### Simulación Básica
```bash
python sim_colas_animado.py
```

#### Ver Ejemplos
```bash
python ejemplos_uso.py
```

#### Ejecutar Tests
```bash
python test_modelos.py
```

#### Visualizaciones
```bash
python visualizaciones.py
```

---

## 🎯 Casos de Uso Prácticos

### 📊 Tabla de Referencia Rápida

| Escenario | Modelo Recomendado | Parámetros Sugeridos |
|-----------|-------------------|---------------------|
| **Cajero único** | M/M/1 | λ=0.6, μ=1.0 |
| **Call center** | M/M/c | λ=2.0, μ=1.0, c=3 |
| **Sala de espera** | M/M/k/1 | λ=1.2, μ=1.0, k=10 |
| **Restaurant** | M/M/k/c | λ=1.8, μ=1.0, c=2, k=15 |
| **Servidor web** | M/M/1 o M/M/c | Según carga |
| **Sistema con SLA** | M/M/k/c | k ajustado al SLA |

### 💼 Ejemplos Empresariales

#### Ejemplo 1: Dimensionamiento de Call Center
```
🎯 Problema: ¿Cuántos operadores necesito?
📊 Datos: λ = 5 llamadas/min, μ = 1.5 llamadas/min por operador

Prueba 1: M/M/c con c=3
→ ρ = 5/(3×1.5) = 1.11 ⚠️ INESTABLE
→ Las colas crecerán indefinidamente

Prueba 2: M/M/c con c=4  
→ ρ = 5/(4×1.5) = 0.83 ✅ ACEPTABLE
→ Wq ≈ 2.5 min promedio de espera

✅ Conclusión: Necesitas mínimo 4 operadores
```

#### Ejemplo 2: Análisis de Capacidad
```
🎯 Problema: ¿Qué capacidad k necesito para < 5% rechazos?
📊 Datos: λ = 2.0, μ = 1.0, c = 2

Prueba 1: M/M/k/c con k=5
→ Tasa rechazo ≈ 18% ❌

Prueba 2: M/M/k/c con k=8
→ Tasa rechazo ≈ 7% ⚠️

Prueba 3: M/M/k/c con k=10
→ Tasa rechazo ≈ 3% ✅

✅ Conclusión: k=10 cumple el objetivo
```

#### Ejemplo 3: Optimización de Costos
```
🎯 Problema: Minimizar costo total (servicio + espera)
📊 Datos: 
   - λ = 1.5 clientes/hora
   - μ = 1.0 cliente/hora por servidor
   - Costo servidor: $20/hora
   - Costo espera: $30/hora por cliente

Análisis:
c=1: Inestable (ρ > 1) ❌
c=2: ρ=0.75, L=3.0, Costo total = 2×20 + 3×30 = $130/hora
c=3: ρ=0.50, L=1.5, Costo total = 3×20 + 1.5×30 = $105/hora ✅
c=4: ρ=0.38, L=1.2, Costo total = 4×20 + 1.2×30 = $116/hora

✅ Conclusión: Óptimo con c=3 servidores
```

---

## 🛠️ Tecnologías Utilizadas

### Frontend (Aplicación Web)

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **HTML5** | - | Estructura de la aplicación |
| **CSS3** | - | Estilos y diseño responsive |
| **JavaScript (ES6+)** | - | Lógica de la aplicación |
| **Chart.js** | 4.4.0 | Gráficos interactivos |
| **GSAP** | 3.12.2 | Animaciones suaves |
| **FileSaver.js** | 2.0.5 | Descarga de archivos |

### Backend (Scripts Python)

| Biblioteca | Versión | Propósito |
|-----------|---------|-----------|
| **Python** | 3.9+ | Lenguaje base |
| **NumPy** | 1.21+ | Cálculos numéricos |
| **Matplotlib** | 3.4+ | Visualizaciones |
| **Random** | Built-in | Generación aleatoria |
| **JSON** | Built-in | Exportación de datos |

### Arquitectura

- **Patrón**: Modular (ES6 modules)
- **Simulación**: Eventos discretos (DES)
- **Distribuciones**: Exponencial (Poisson para llegadas)
- **Visualización**: Canvas 2D + Chart.js

---

## 🧪 Testing y Validación

### Suite de Tests Python

El archivo `test_modelos.py` incluye 15 tests completos:

```bash
python test_modelos.py

✓ test_invalid_params           # Validación de parámetros
✓ test_unstable_warning         # Advertencias ρ ≥ 1
✓ test_utilization              # Verificación de ρ
✓ test_littles_law              # Ley de Little (L = λW)
✓ test_analytical_comparison    # Comparación con teoría
✓ test_warmup_improvement       # Mejora con warmup
✓ test_reproducibility          # Determinismo (seed)
✓ test_json_export             # Exportación correcta
... y más

✅ Total: 15 tests ejecutados
✅ Exitosos: 15
✅ Fallidos: 0
```

### Validación de Precisión

Los tests verifican que:
- Error < 10% vs teoría (con horizonte adecuado)
- Ley de Little se cumple (L = λW)
- ρ calculado correctamente
- Warmup mejora precisión

### Testing Manual (Aplicación Web)

**Checklist de Verificación:**

- [ ] Todos los modelos se ejecutan sin errores
- [ ] Animación fluida (30 FPS+)
- [ ] Gráficas se actualizan correctamente
- [ ] Exportación JSON contiene datos completos
- [ ] Reporte HTML se genera con gráficas embebidas
- [ ] Comparación con teoría muestra error < 5%
- [ ] Rechazos funcionan en M/M/k/1 y M/M/k/c
- [ ] Tema claro/oscuro funciona
- [ ] Responsive en mobile

---

## 🐛 Solución de Problemas

### Aplicación Web

#### ❌ La simulación no inicia

**Posibles causas:**
1. Parámetros inválidos (λ ≤ 0 o μ ≤ 0)
2. horizonte ≤ warmup
3. En M/M/k/c: k < c

**Solución:**
- Revisa los mensajes de error en rojo
- Ajusta los parámetros según indicaciones
- Recarga la página (F5) si es necesario

#### ❌ La animación está muy lenta

**Soluciones:**
1. Aumenta la velocidad (selector: 2x, 5x, 10x)
2. Reduce el horizonte (usa 500 en vez de 5000)
3. Cierra otras pestañas del navegador

#### ❌ Las gráficas no se muestran

**Solución:**
- Espera a que la simulación termine (100%)
- No pauses justo antes del final
- Si persiste: F5 y repetir

#### ❌ Resultados muy diferentes a la teoría

**Error > 10%**

**Causas:**
1. Horizonte muy corto → Aumentar a 2000-5000
2. Warmup insuficiente → Usar 20% del horizonte
3. Sistema inestable → Verificar ρ < 1

### Scripts Python

#### ❌ Error de importación

```bash
# Solución
pip install -r requirements.txt
```

#### ❌ Versión de Python incorrecta

```bash
# Verificar versión
python --version  # Debe ser 3.9+

# Si es antigua, actualiza Python
```

#### ❌ Tests fallan

```bash
# Re-instalar dependencias
pip uninstall -y numpy matplotlib
pip install -r requirements.txt

# Ejecutar de nuevo
python test_modelos.py
```

---

## 👥 Contribución

### ¿Cómo Contribuir?

¡Las contribuciones son bienvenidas! Puedes ayudar con:

- 🐛 **Reportar bugs**: Abre un issue describiendo el problema
- ✨ **Nuevas características**: Propón mejoras o nuevos modelos
- 📖 **Documentación**: Mejora las guías existentes
- 🧪 **Tests**: Añade más casos de prueba
- 🎨 **UI/UX**: Mejora la interfaz y experiencia

### Proceso de Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Ideas para Contribuir

- [ ] Agregar modelo M/G/1 (servicio general)
- [ ] Implementar redes de colas (Jackson networks)
- [ ] Añadir más distribuciones (Erlang, Hiperexponencial)
- [ ] Crear modo "comparación lado a lado"
- [ ] Exportar gráficas individuales como PNG
- [ ] Agregar calculadora de nivel de servicio (SLA)
- [ ] Modo "batch simulation" (múltiples réplicas)
- [ ] Integración con Excel (import/export)

---

## 📄 Créditos y Licencia

### Desarrollado Por

- **Curso**: Investigación de Operaciones
- **Institución**: Universidad Pedagógica y Tecnológica de Colombia (UPTC)
- **Año**: 2025
- **Repositorio**: [github.com/jdCarrillo15/Proyecto-IO-modelos-de-colas](https://github.com/jdCarrillo15/Proyecto-IO-modelos-de-colas)

### Licencia

Este proyecto es de uso **educativo** para el curso de Investigación de Operaciones de la UPTC.

### Referencias Académicas

- Gross, D., & Harris, C. M. (1998). *Fundamentals of Queueing Theory*
- Kleinrock, L. (1975). *Queueing Systems, Volume 1: Theory*
- Taha, H. A. (2017). *Investigación de Operaciones*
- Hillier, F. S., & Lieberman, G. J. (2015). *Introducción a la Investigación de Operaciones*

### Agradecimientos

- Chart.js por la librería de gráficos
- GSAP por las animaciones suaves
- Comunidad de Stack Overflow por el apoyo técnico
- Profesores y estudiantes de la UPTC por el feedback

---

## 📊 Estadísticas del Proyecto

| Métrica | Valor |
|---------|-------|
| **Líneas de código JavaScript** | ~2,500 |
| **Líneas de código Python** | ~2,400 |
| **Líneas de CSS** | ~1,700 |
| **Modelos implementados** | 4 (M/M/1, M/M/c, M/M/k/1, M/M/k/c) |
| **Archivos Python** | 6 |
| **Módulos JavaScript** | 8 |
| **Tests unitarios** | 15+ |
| **Páginas de documentación** | 7+ |
| **Browsers compatibles** | 4+ (Chrome, Edge, Firefox, Safari) |

---

## 🎯 Próximos Pasos Recomendados

### Para Estudiantes
1. Lee el [**MANUAL_USUARIO.md**](MANUAL_USUARIO.md) completo
2. Prueba el [**tutorial interactivo**](web-app/index.html) en la aplicación
3. Simula los 4 modelos con diferentes parámetros
4. Compara resultados con teoría (M/M/1 y M/M/c)
5. Exporta y analiza los datos

### Para Profesores
1. Revisa la [**GUIA_DEMO.md**](GUIA_DEMO.md) para presentaciones
2. Usa la app web para demos en clase
3. Asigna ejercicios usando diferentes configuraciones
4. Compara resultados de simulación vs teoría

### Para Desarrolladores
1. Explora el código en `web-app/js/modules/`
2. Ejecuta los tests: `python test_modelos.py`
3. Revisa [**CORRECCIONES_APLICADAS.md**](CORRECCIONES_APLICADAS.md)
4. Considera contribuir con mejoras

---

## 📞 Soporte y Contacto

### ¿Necesitas Ayuda?

- 📖 **Documentación**: Lee el [Manual de Usuario](MANUAL_USUARIO.md)
- 🐛 **Reportar Bug**: [Crear Issue](../../issues)
- 💡 **Sugerencias**: [Discussions](../../discussions)
- 📧 **Email**: Contacta al curso de IO - UPTC

### Enlaces Útiles

- [🏠 Página de Inicio](INICIO.html)
- [⚡ Inicio Rápido](INICIO_RAPIDO.md)
- [🎬 Guía de Demo](GUIA_DEMO.md)
- [🌐 Aplicación Web](web-app/index.html)

---

<div align="center">

**¡Disfruta explorando la teoría de colas! 🎉**

*Desarrollado con ❤️ para Investigación de Operaciones - UPTC*

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/jdCarrillo15/Proyecto-IO-modelos-de-colas)
[![Documentation](https://img.shields.io/badge/Docs-Manual%20Usuario-green)](MANUAL_USUARIO.md)
[![Web App](https://img.shields.io/badge/Demo-Web%20App-orange)](web-app/index.html)

</div>
