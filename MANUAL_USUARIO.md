# Manual de Usuario - Sistema de Simulación de Colas

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Instalación y Configuración](#instalación-y-configuración)
4. [Interfaz de Usuario](#interfaz-de-usuario)
5. [Modelos de Cola Disponibles](#modelos-de-cola-disponibles)
6. [Guía de Uso Paso a Paso](#guía-de-uso-paso-a-paso)
7. [Parámetros de Configuración](#parámetros-de-configuración)
8. [Interpretación de Resultados](#interpretación-de-resultados)
9. [Exportación de Datos](#exportación-de-datos)
10. [Solución de Problemas](#solución-de-problemas)
11. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## Introducción

### Descripción del sistema

El Sistema de Simulación de Colas es una aplicación web interactiva diseñada para simular y analizar sistemas de teoría de colas. Permite a estudiantes, profesores e investigadores visualizar el comportamiento de diferentes modelos de colas en tiempo real, comparar resultados con valores teóricos y exportar datos para análisis posterior.

### Características principales

- Interfaz moderna e intuitiva con animaciones en tiempo real
- 4 modelos de cola implementados (M/M/1, M/M/c, M/M/k/1, M/M/k/c)
- Gráficas dinámicas que se actualizan durante la simulación
- Indicador de estabilidad visual para análisis rápido
- Comparación con teoría para modelos M/M/1 y M/M/c
- Exportación completa a JSON y reportes HTML con gráficas
- Tema claro/oscuro según preferencia del usuario

### Casos de uso

- **Educación**: Enseñanza de teoría de colas en cursos universitarios
- **Investigación**: Análisis de sistemas de espera y dimensionamiento
- **Análisis empresarial**: Evaluación de recursos (cajeros, servidores, etc.)
- **Toma de decisiones**: Determinación del número óptimo de servidores

---

## Requisitos del Sistema

### Navegadores compatibles

- Google Chrome (v90+) - Recomendado
- Microsoft Edge (v90+) - Recomendado
- Mozilla Firefox (v88+)
- Safari (v14+)
- Internet Explorer - No compatible

### Requisitos mínimos

- **Sistema Operativo**: Windows 7+, macOS 10.12+, Linux (cualquier distribución moderna)
- **RAM**: 2 GB mínimo, 4 GB recomendado
- **Resolución**: 1280x720 mínimo, 1920x1080 recomendado
- **Conexión a Internet**: Solo para carga inicial (CDN de librerías)

### Dependencias externas (cargadas automáticamente)

- Chart.js v4.4.0 - Gráficos interactivos
- GSAP v3.12.2 - Animaciones suaves
- FileSaver.js v2.0.5 - Descarga de archivos

---

## Instalación y Configuración

1. **Descarga o clona el repositorio:**
   ```bash
   git clone https://github.com/jdCarrillo15/Proyecto-IO-modelos-de-colas.git
   ```

2. **Navega a la carpeta del proyecto:**
   ```bash
   cd Proyecto-IO-modelos-de-colas/web-app
   ```

3. **Servidor Local:**

Si tienes Python instalado:

```bash
# Python 3
cd web-app
python -m http.server 8000

# Luego abre: http://localhost:8000
```

Si tienes Node.js:

```bash
# Instalar servidor simple
npm install -g http-server
```
---

## Interfaz de Usuario

### Componentes principales

#### 1. Barra superior

- Logo y título del sistema
- Botón de tema para cambiar entre modo oscuro y claro
- Botón de tutorial con guía interactiva
- Botón de ayuda con información sobre modelos y métricas

#### 2. Panel izquierdo (Configuración)

**Selector de Modelo**
- 4 botones para elegir el modelo de cola
- El modelo activo se resalta en azul

**Parámetros del Sistema**
- Sliders interactivos para ajustar valores
- Valores que se actualizan en tiempo real
- Tooltips informativos al pasar el ratón

**Indicador de Estabilidad**
- Gauge visual mostrando ρ (utilización)
- Código de colores:
  - Verde (ρ < 0.7): Óptimo
  - Amarillo (0.7 ≤ ρ < 0.9): Aceptable
  - Naranja (0.9 ≤ ρ < 1.0): Crítico
  - Rojo (ρ ≥ 1.0): Inestable

**Botones de Acción**
- Ejecutar Simulación: Inicia la simulación
- Pausar: Pausa/reanuda la simulación
- Reiniciar: Resetea todo el sistema
- Exportar Resultados: Guarda datos (habilitado al finalizar)

#### 3. Área central (Visualización)

**Control de Velocidad**
- Selector desplegable: 0.5x, 1x, 2x, 5x, 10x
- Permite acelerar o ralentizar la animación

**Canvas de Animación**
- Nodo de llegadas (izquierda): Punto de origen
- Cola (centro): Clientes esperando
- Servidores (derecha): Atendiendo clientes
- Clientes representados como círculos de colores

**Barra de Progreso**
- Muestra tiempo actual vs horizonte total
- Porcentaje de avance

**Pestañas de Gráficas**
- Series Temporales: Evolución de L y Lq
- Distribuciones: Histograma de tiempos de espera

#### 4. Panel derecho (Métricas)

**Métricas Instantáneas**
- ρ: Utilización del sistema
- L: Clientes en sistema
- Lq: Clientes en cola
- W: Tiempo en sistema
- Wq: Tiempo en cola

**Teoría vs Simulación**
- Aparece solo si se activa "Comparar con Teoría"
- Muestra valores teóricos y error porcentual

**Estadísticas Acumuladas**
- Clientes atendidos
- Clientes rechazados (modelos con capacidad)
- Tiempo de simulación
- Tiempo efectivo (sin warmup)

**Estado de Servidores**
- Visible en modelos M/M/c y M/M/k/c
- Muestra cada servidor (S1, S2, etc.)
- Estado: Ocupado (verde) o Libre (gris)

---

## Modelos de Cola Disponibles

### 1. M/M/1 - Un Servidor, Capacidad Infinita

**Descripción:**
Sistema con un único servidor y sin límite de capacidad. El modelo más básico de teoría de colas.

**Parámetros:**
- λ (lambda): Tasa de llegadas (clientes/tiempo)
- μ (mu): Tasa de servicio (clientes/tiempo)

**Condición de Estabilidad:**
- ρ = λ/μ < 1 (sistema estable)

**Fórmulas Teóricas:**
```
ρ = λ/μ
L = ρ/(1-ρ)
Lq = ρ²/(1-ρ)
W = 1/(μ-λ)
Wq = ρ/(μ-λ)
```

**Ejemplo de Uso:**
- Cajero único en banco pequeño
- Puesto de peajes con 1 caseta
- Servidor web con 1 procesador

**Configuración Sugerida:**
```
λ = 0.8
μ = 1.0
Horizonte = 1000
Warmup = 200
Comparar con teoría
```

---

### 2. M/M/c - Múltiples Servidores, Capacidad Infinita

**Descripción:**
Sistema con c servidores en paralelo y sin límite de capacidad. Los clientes forman una única cola y son atendidos por el primer servidor disponible.

**Parámetros:**
- λ: Tasa de llegadas
- μ: Tasa de servicio por servidor
- c: Número de servidores (1, 2, 3, ...)

**Condición de Estabilidad:**
- ρ = λ/(c×μ) < 1

**Fórmulas Teóricas:**
Usa fórmulas de Erlang-C (más complejas, calculadas automáticamente)

**Ejemplo de Uso:**
- Varios cajeros en banco
- Call center con múltiples operadores
- Sistema de múltiples procesadores

**Configuración Sugerida:**
```
λ = 0.8
μ = 1.0
c = 2
Horizonte = 1000
Warmup = 200
Comparar con teoría
```

---

### 3. M/M/k/1 - Un Servidor, Capacidad Limitada

**Descripción:**
Sistema con un servidor y capacidad máxima k. Cuando el sistema está lleno (k clientes), los nuevos clientes son rechazados y se pierden.

**Parámetros:**
- λ: Tasa de llegadas
- μ: Tasa de servicio
- k: Capacidad máxima del sistema (≥1)

**Característica Especial:**
- **Rechaza clientes** cuando hay k clientes en el sistema
- Muestra estadísticas de rechazo en resultados

**Ejemplo de Uso:**
- Sala de espera con asientos limitados
- Buffer de sistema con capacidad fija
- Estacionamiento con plazas limitadas

**Configuración Sugerida:**
```
λ = 1.2
μ = 1.0
k = 5
Horizonte = 1000
Warmup = 200
```

**Nota:** No hay comparación con teoría (sistema más complejo)

---

### 4. M/M/k/c - Múltiples Servidores, Capacidad Limitada

**Descripción:**
Sistema con c servidores y capacidad máxima k. Combina paralelismo con límite de capacidad.

**Parámetros:**
- λ: Tasa de llegadas
- μ: Tasa de servicio por servidor
- c: Número de servidores
- k: Capacidad máxima del sistema (k ≥ c)

**Restricción:**
- k debe ser mayor o igual que c (validado automáticamente)

**Característica Especial:**
- Rechaza clientes cuando hay k clientes en el sistema
- Más eficiente que M/M/k/1 debido a múltiples servidores

**Ejemplo de Uso:**
- Hospital con salas de espera limitadas
- Sistema con procesadores múltiples y buffer finito
- Restaurant con mesas limitadas y varios meseros

**Configuración Sugerida:**
```
λ = 1.5
μ = 1.0
c = 2
k = 8
Horizonte = 1000
Warmup = 200
```

---

## Guía de Uso Paso a Paso

### Simulación Básica (M/M/1)

#### Paso 1: Seleccionar Modelo
1. En el panel izquierdo, asegúrate que **M/M/1** esté seleccionado (azul)
2. Si no lo está, haz clic en el botón "M/M/1"

#### Paso 2: Configurar Parámetros
1. **λ (Lambda)** - Ajusta a 0.8
   - Usa el slider o escribe el valor
   - Representa 0.8 clientes por unidad de tiempo

2. **μ (Mu)** - Ajusta a 1.0
   - Representa que el servidor puede atender 1 cliente por unidad de tiempo

3. **Horizonte** - Deja en 1000
   - Tiempo total de simulación

4. **Warmup** - Deja en 200
   - Periodo inicial que se descarta para eliminar efectos transitorios

5. **Comparar con Teoría** - Activa esta opción
   - Mostrará comparación con valores teóricos

#### Paso 3: Verificar Estabilidad
1. Observa el gauge en el panel izquierdo
2. Debe mostrar: ρ = 0.800
3. Estado: "Aceptable" (amarillo/verde)
4. Gauge al 80%

#### Paso 4: Ejecutar Simulación
1. Haz clic en "Ejecutar Simulación"
2. Confirma si aparece advertencia de inestabilidad (si ρ ≥ 1)
3. La simulación comenzará automáticamente

#### Paso 5: Observar Durante la Simulación
1. **Animación:**
   - Clientes aparecen en el nodo de llegadas (izquierda)
   - Se mueven hacia la cola (centro)
   - Son atendidos por el servidor (derecha)
   - Desaparecen al completar el servicio

2. **Métricas en tiempo real:**
   - Panel derecho se actualiza continuamente
   - Observa cómo L, Lq, W, Wq evolucionan

3. **Gráficas:**
   - La gráfica de series temporales muestra la evolución
   - Cambia a pestaña "Distribuciones" para ver histograma

4. **Controles:**
   - Pausar si necesitas detener temporalmente
   - Cambia la velocidad si es muy lento (prueba 2x o 5x)
   - Reiniciar si quieres empezar de nuevo

#### Paso 6: Revisar Resultados
1. Al finalizar, aparecerá un modal con "Simulación Completada"

2. **Métricas Finales:**
   - ρ, L, Lq, W, Wq con valores finales
   - Clientes atendidos

3. **Comparación con Teoría:**
   - Tabla mostrando Simulación vs Teoría
   - Error porcentual (debe ser menor al 5%)

4. **Gráficas Finales:**
   - Evolución temporal completa
   - Distribución de tiempos de espera

#### Paso 7: Exportar Datos (Opcional)
1. **Descargar JSON:**
   - Descarga archivo con todos los datos
   - Formato: simulacion-colas-[timestamp].json
   - Útil para análisis posterior en Python, R, Excel

2. **Generar Reporte HTML:**
   - Crea reporte completo con gráficas embebidas
   - Se abre automáticamente en el navegador
   - Listo para imprimir o compartir

3. **Nueva Simulación:**
   - Cierra el modal y configura nuevos parámetros

---

### Simulación Avanzada (M/M/k/c con Rechazos)

#### Configuración
```
Modelo: M/M/k/c
λ = 1.5
μ = 1.0
c = 2 servidores
k = 8 capacidad
Horizonte = 1000
Warmup = 200
```

#### Qué Observar
1. **Visualización de servidores:**
   - Verás 2 servidores etiquetados S1 y S2
   - Ocupados: verde brillante
   - Libres: gris

2. **Rechazos:**
   - Cuando el sistema tenga 8 clientes, los nuevos serán rechazados
   - Mensaje en consola (F12): "Cliente X rechazado"

3. **Resultados finales:**
   - Clientes Atendidos: ~850
   - Clientes Rechazados: ~150
   - Tasa de Rechazo: ~15%

---

## Parámetros de Configuración

### λ (Lambda) - Tasa de Llegadas

**Rango:** 0.1 - 10.0 (ajustable)

**Significado:**
- Número promedio de clientes que llegan por unidad de tiempo
- Ejemplos:
  - λ = 0.5: En promedio, 1 cliente cada 2 unidades de tiempo
  - λ = 2.0: En promedio, 2 clientes por unidad de tiempo

**Cómo afecta:**
- Mayor λ: Más llegadas, sistema más cargado
- Menor λ: Menos llegadas, sistema más holgado

**Valores típicos:**
- Bajo: 0.5 - 2.0
- Medio: 2.0 - 5.0
- Alto: 5.0 - 10.0

---

### μ (Mu) - Tasa de Servicio

**Rango:** 0.1 - 15.0 (ajustable)

**Significado:**
- Número promedio de clientes que un servidor puede atender por unidad de tiempo
- Ejemplos:
  - μ = 1.0: Servidor atiende 1 cliente por unidad de tiempo
  - μ = 3.0: Servidor atiende 3 clientes por unidad de tiempo

**Cómo afecta:**
- Mayor μ: Servicio más rápido, sistema más eficiente
- Menor μ: Servicio más lento, más congestión

**Valores típicos:**
- Lento: 0.5 - 1.5
- Medio: 1.5 - 5.0
- Rápido: 5.0 - 15.0

---

### c - Número de Servidores

**Rango:** 1 - 10 (solo para M/M/c y M/M/k/c)

**Significado:**
- Cantidad de servidores trabajando en paralelo
- Cada servidor tiene tasa μ

**Cómo afecta:**
- Más servidores: Menor ρ por servidor, menos espera
- Capacidad total del sistema = c × μ

**Recomendaciones:**
- Sistema pequeño: c = 1-2
- Sistema mediano: c = 3-5
- Sistema grande: c = 6-10

**Nota:** ρ se calcula como λ/(c×μ)

---

### k - Capacidad Máxima

**Rango:** 5 - 100 (solo para M/M/k/1 y M/M/k/c)

**Significado:**
- Número máximo de clientes que puede haber en el sistema simultáneamente
- Incluye clientes en cola + clientes siendo atendidos

**Cómo afecta:**
- Menor k: Más rechazos, mayor pérdida de clientes
- Mayor k: Menos rechazos, mayor cola posible

**Restricción en M/M/k/c:**
- k debe ser mayor o igual que c (al menos un lugar por servidor)

**Valores típicos:**
- Muy limitado: k = 5-10
- Limitado: k = 10-30
- Amplio: k = 30-100

---

### Horizonte de Simulación

**Rango:** 100 - 10,000

**Significado:**
- Tiempo total que durará la simulación
- Unidades arbitrarias (puedes pensar en minutos, horas, etc.)

**Recomendaciones:**
- Pruebas rápidas: 100-500
- Simulación normal: 1,000-2,000
- Alta precisión: 5,000-10,000

**Nota:** Mayor horizonte = Más datos = Mejor precisión (pero más tiempo)

---

### Periodo de Warmup

**Rango:** 0 - 2,000

**Significado:**
- Tiempo inicial que se descarta para eliminar efectos transitorios
- El sistema "se calienta" hasta alcanzar estado estacionario

**Recomendaciones:**
- Warmup = 10-20% del horizonte
- Ejemplo: Horizonte 1000 → Warmup 200

**Importante:**
- Warmup debe ser < Horizonte (validado automáticamente)
- Tiempo efectivo = Horizonte - Warmup

---

### Comparar con Teoría

**Tipo:** Checkbox (Sí/No)

**Disponible en:** M/M/1 y M/M/c solamente

**Cuando Activado:**
- Calcula valores teóricos usando fórmulas matemáticas
- Muestra comparación en resultados finales
- Calcula error porcentual

**Útil para:**
- Verificar correctitud de la simulación
- Aprendizaje (comparar simulación vs teoría)
- Validación de resultados

---

## Interpretación de Resultados

### Métricas principales

#### ρ (Rho) - Utilización del Sistema

**Definición:**
- Fracción de tiempo que los servidores están ocupados
- Rango: 0.0 (nunca ocupado) a 1.0+ (siempre ocupado)

**Fórmulas:**
- M/M/1 y M/M/k/1: ρ = λ/μ
- M/M/c y M/M/k/c: ρ = λ/(c×μ)

**Interpretación:**
- **ρ < 0.7**: Sistema holgado, buen servicio
- **0.7 ≤ ρ < 0.9**: Sistema aceptable, puede haber picos
- **0.9 ≤ ρ < 1.0**: Sistema crítico, cerca de saturación
- **ρ ≥ 1.0**: Sistema inestable, colas crecen indefinidamente

**Ejemplo:**
- ρ = 0.80: Servidores ocupados 80% del tiempo

---

#### L - Número de Clientes en el Sistema

**Definición:**
- Promedio de clientes en el sistema completo (en cola + siendo atendidos)

**Interpretación:**
- L bajo (0-2): Sistema poco congestionado
- L medio (2-10): Congestión moderada
- L alto (>10): Sistema muy congestionado

**Ejemplo:**
- L = 4.5 → En promedio, hay 4-5 clientes en el sistema

**Relación con Otros:**
- L = Lq + (número promedio de servidores ocupados)
- Ley de Little: L = λ × W

---

#### Lq - Número de Clientes en Cola

**Definición:**
- Promedio de clientes esperando en la cola (sin contar los que están siendo atendidos)

**Interpretación:**
- Lq bajo (0-1): Poca espera
- Lq medio (1-5): Espera moderada
- Lq alto (>5): Mucha espera

**Ejemplo:**
- Lq = 2.3 → En promedio, 2-3 clientes esperan en la cola

**Nota:** Lq siempre ≤ L

---

#### W - Tiempo en el Sistema

**Definición:**
- Tiempo promedio que un cliente pasa en el sistema completo (esperando + siendo atendido)
- Unidades: Mismas que las del tiempo de simulación

**Interpretación:**
- Depende del contexto (minutos, horas, etc.)
- W alto = Mucho tiempo total en el sistema

**Ejemplo:**
- W = 5.2 → Un cliente pasa en promedio 5.2 unidades de tiempo

**Ley de Little:**
- L = λ × W
- W = L / λ

---

#### Wq - Tiempo en Cola

**Definición:**
- Tiempo promedio que un cliente espera en la cola (sin contar el servicio)

**Interpretación:**
- Wq bajo = Poca espera
- Wq alto = Mucha espera

**Ejemplo:**
- Wq = 3.8 → Un cliente espera en promedio 3.8 unidades antes de ser atendido

**Relación:**
- W = Wq + (tiempo promedio de servicio)
- Wq = Lq / λ

---

### Métricas Adicionales (Modelos con Capacidad)

#### Clientes Rechazados

**Aparece en:** M/M/k/1 y M/M/k/c

**Definición:**
- Número total de clientes que fueron rechazados porque el sistema estaba lleno

**Interpretación:**
- 0 rechazos: Capacidad suficiente
- Pocos rechazos (<5%): Capacidad adecuada
- Muchos rechazos (>20%): Considerar aumentar k o c

---

#### Tasa de Rechazo

**Fórmula:**
```
Tasa de Rechazo = (Rechazados / (Atendidos + Rechazados)) × 100%
```

**Interpretación:**
- 0-5%: Excelente, pérdida mínima
- 5-15%: Aceptable, pero mejorable
- 15-30%: Alta pérdida, revisar capacidad
- >30%: Crítico, sistema subdimensionado

**Ejemplo:**
- 12 rechazados de 50 totales → Tasa = 24%

---

### Comparación con Teoría

**Disponible en:** M/M/1 y M/M/c con "Comparar con Teoría" activado

**Tabla de Comparación:**

| Métrica | Simulación | Teoría | Error (%) |
|---------|-----------|--------|-----------|
| L | 4.1234 | 4.0000 | 3.09% |
| Lq | 3.3456 | 3.2000 | 4.55% |
| W | 5.1543 | 5.0000 | 3.09% |
| Wq | 4.1807 | 4.0000 | 4.52% |

**Interpretación del Error:**
- **Menor al 5%**: Excelente concordancia
- **5-10%**: Buena concordancia, aceptable
- **Mayor al 10%**: Revisar parámetros o aumentar horizonte

**Causas de Error:**
- Variabilidad estocástica (aleatorio)
- Horizonte corto
- Warmup insuficiente
- Efectos de borde

---

## Exportación de Datos

### Formato JSON

**Archivo:** `simulacion-colas-[timestamp].json`

**Contenido:**
```json
{
  "config": {
    "model": "mm1",
    "lambda": 0.8,
    "mu": 1.0,
    "horizon": 1000,
    "warmup": 200
  },
  "metrics": {
    "rho": 0.8000,
    "L": 4.1234,
    "Lq": 3.3456,
    "W": 5.1543,
    "Wq": 4.1807
  },
  "timeSeries": {
    "time": [0, 1, 2, ...],
    "system": [0, 1, 2, ...],
    "queue": [0, 0, 1, ...]
  },
  "completedJobs": [
    {
      "id": 1,
      "arrivalTime": 1.23,
      "startTime": 1.23,
      "departureTime": 2.45,
      "waitTime": 0.0,
      "systemTime": 1.22
    },
    ...
  ],
  "totalServed": 812,
  "totalRejected": 0
}
```

**Uso:**
- Análisis estadístico adicional
- Importar a Python, R, MATLAB
- Excel para gráficas personalizadas
- Documentación de experimentos

---

### Reporte HTML

**Archivo:** `reporte-simulacion-[timestamp].html`

**Contenido:**
1. **Configuración:** Tabla con todos los parámetros
2. **Métricas Finales:** Tabla con ρ, L, Lq, W, Wq
3. **Estadísticas:** Clientes atendidos, rechazados, tiempos
4. **Gráficas Embebidas:**
   - Evolución temporal (PNG en base64)
   - Distribución de tiempos (PNG en base64)
5. **Comparación con teoría** (si aplica)

**Características:**
- Autocontenido (no requiere conexión)
- Listo para imprimir
- Fácil de compartir por email
- Formato profesional

**Uso:**
- Reportes de tareas/proyectos
- Presentaciones
- Documentación de análisis
- Archivo histórico

---

## Solución de Problemas

### Problema: La simulación no inicia

**Posibles causas:**

1. **Parámetros inválidos**
   - Verificar que λ > 0 y μ > 0
   - Verificar que horizonte > warmup
   - En M/M/k/c: verificar k ≥ c

2. **Sistema inestable (ρ ≥ 1)**
   - Aparece advertencia
   - Puedes continuar, pero la cola crecerá indefinidamente
   - Solución: Reducir λ o aumentar μ/c

3. **Navegador no compatible**
   - Usar Chrome, Edge o Firefox actualizados

**Solución:**
- Revisar mensajes de error (en rojo)
- Ajustar parámetros según indicaciones
- Recargar página (F5) si es necesario

---

### Problema: La animación está muy lenta

**Causas:**
- Velocidad en 0.5x o 1x
- Demasiados clientes en pantalla
- Hardware limitado

**Soluciones:**
1. **Aumentar velocidad:**
   - Cambiar a 2x, 5x o 10x en el selector

2. **Reducir carga:**
   - Usar horizonte más corto (500 en vez de 5000)
   - Sistema ya optimizado (máx 50 clientes visuales)

3. **Mejorar rendimiento:**
   - Cerrar pestañas innecesarias del navegador
   - Cerrar otras aplicaciones

---

### Problema: Las gráficas no se muestran

**En el Modal de Resultados:**

**Causas:**
- Simulación no finalizó correctamente
- Error al capturar canvas

**Soluciones:**
1. Esperar a que la simulación termine (100%)
2. No pausar justo antes del final
3. Si persiste: F5 y repetir simulación

**Durante la Simulación:**

**Causas:**
- Warmup aún en progreso
- No hay suficientes datos

**Soluciones:**
- Esperar a que termine el warmup
- Las gráficas aparecen después del periodo de warmup

---

### Problema: Resultados muy diferentes a la teoría

**Error > 10%**

**Causas:**
1. **Horizonte muy corto**
   - Aumentar a 2000-5000

2. **Warmup insuficiente**
   - Usar 20% del horizonte

3. **Sistema inestable**
   - Verificar ρ < 1

4. **Variabilidad aleatoria**
   - Normal en simulaciones cortas
   - Repetir simulación varias veces

**Solución:**
- Aumentar horizonte a 5000
- Warmup = 1000
- Ejecutar múltiples réplicas y promediar

---

### Problema: No se descarga el JSON/HTML

**Causas:**
- Bloqueador de pop-ups activo
- Permiso de descarga denegado
- Navegador bloquea descargas

**Soluciones:**
1. Permitir pop-ups en el navegador
2. Verificar configuración de descargas
3. Intentar en modo incógnito
4. Probar otro navegador

---

### Problema: El tema no cambia

**Solución:**
1. Hacer clic en el botón de cambio de tema (Luna/Sol)
2. Limpiar caché del navegador (Ctrl+Shift+Del)
3. Recargar página (F5)
4. Si persiste: Limpiar localStorage
   - F12: Console: localStorage.clear()

---

## Preguntas Frecuentes

### General

**P: ¿Necesito instalar algo?**
R: No, solo un navegador web moderno. El sistema funciona completamente en el navegador.

**P: ¿Funciona sin internet?**
R: Necesitas conexión para la primera carga (librerías CDN). Después, puedes descargar el proyecto y usarlo offline.

**P: ¿Puedo usar esto en mi clase?**
R: Sí, es libre y gratuito. Diseñado específicamente para educación.

**P: ¿Dónde se guardan mis simulaciones?**
R: No se guardan automáticamente. Debes exportar manualmente a JSON o HTML.

---

### Modelos

**P: ¿Cuál modelo debo usar?**
R: Depende de tu caso:
- **M/M/1**: Sistema simple, 1 servidor, sin límites
- **M/M/c**: Múltiples servidores, sin límites  
- **M/M/k/1**: 1 servidor, con capacidad limitada
- **M/M/k/c**: Múltiples servidores, capacidad limitada

**P: ¿Por qué M/M/k/1 y M/M/k/c no tienen comparación con teoría?**
R: Las fórmulas para sistemas finitos son más complejas y requieren cálculos de estados estacionarios con cadenas de Markov.

**P: ¿Qué significa "M/M/..." en los nombres?**
R: Notación de Kendall:
- Primera M: Llegadas tipo Markoviano (exponencial)
- Segunda M: Servicios tipo Markoviano (exponencial)
- Números: Configuración del sistema

---

### Parámetros

**P: ¿Qué unidades usan λ y μ?**
R: Unidades arbitrarias (clientes/tiempo). Puedes pensar en minutos, horas, etc. Lo importante es la consistencia.

**P: ¿Qué pasa si ρ ≥ 1?**
R: El sistema es inestable. La cola crecerá indefinidamente. Puedes simular para observar el comportamiento, pero no alcanzará estado estacionario.

**P: ¿Cuánto debe durar la simulación?**
R: Recomendado: Horizonte = 1000-2000, Warmup = 200-400. Para alta precisión: 5000-10000.

**P: ¿Por qué usar warmup?**
R: El sistema inicia vacío (estado transitorio). El warmup permite que alcance comportamiento estacionario antes de medir.

---

### Resultados

**P: ¿Por qué los resultados varían cada vez?**
R: Es una simulación estocástica (aleatoria). Usa números aleatorios para generar llegadas y servicios. Es normal.

**P: ¿Cómo saber si mi simulación es correcta?**
R: 
1. Activa "Comparar con teoría" (M/M/1 o M/M/c)
2. Error < 5% = Correcto
3. Repetir varias veces y verificar consistencia

**P: ¿Qué hacer con los rechazos en M/M/k/1 y M/M/k/c?**
R: Analizar la tasa de rechazo:
- Si es alta (>20%): Aumentar k (capacidad) o c (servidores)
- Si es baja (<5%): Capacidad adecuada

---

### Exportación

**P: ¿Para qué sirve el JSON?**
R: Análisis adicional en Python, R, MATLAB, Excel. Contiene todos los datos crudos.

**P: ¿El HTML incluye las gráficas?**
R: Sí, las gráficas están embebidas en formato base64. Es un archivo autocontenido.

**P: ¿Puedo editar el reporte HTML?**
R: Sí, es HTML estándar. Puedes abrirlo en un editor y modificarlo.

---

### Técnicas

**P: ¿Qué algoritmo usa la simulación?**
R: Simulación por eventos discretos (DES) con generación de variables aleatorias exponenciales.

**P: ¿Es precisa la simulación?**
R: Sí, con parámetros adecuados. Comparación con teoría muestra error < 5%.

**P: ¿Puedo agregar mis propios modelos?**
R: Es posible, pero requiere modificar el código JavaScript. Ver documentación técnica.

---

### Reporte de Problemas
Al reportar un problema, incluye:
1. Navegador y versión
2. Modelo usado
3. Parámetros configurados
4. Descripción del problema
5. Capturas de pantalla (si aplica)

---

## Referencias

### Teoría de Colas
- Taha, H. A. (2017). *Investigación de Operaciones*
- Hillier, F. S., & Lieberman, G. J. (2015). *Introducción a la Investigación de Operaciones*
- Gross, D., & Harris, C. M. (1998). *Fundamentals of Queueing Theory*

### Recursos en Línea
- Queue Theory - Wikipedia: https://en.wikipedia.org/wiki/Queueing_theory
- Little's Law: https://en.wikipedia.org/wiki/Little%27s_law
- Erlang C Formula: https://en.wikipedia.org/wiki/Erlang_(unit)

---

## Historial de Versiones

### Versión 2.0 - Noviembre 2025
- 4 modelos completamente funcionales
- Gráficas en modal de resultados
- Distribuciones en tiempo real
- Modelos con capacidad limitada
- Estadísticas de rechazos
- Optimización de rendimiento
- Validaciones mejoradas

### Versión 1.0 - Octubre 2025
- Versión inicial
- M/M/1 y M/M/c básicos
- Interfaz web interactiva
- Comparación con teoría

---

## Licencia

**Proyecto:** Sistema de Simulación de Colas
**Curso:** Investigación de Operaciones - UPTC
**Año:** 2025

Desarrollado para fines educativos.

---

Para más información, consulta el README.md del proyecto.