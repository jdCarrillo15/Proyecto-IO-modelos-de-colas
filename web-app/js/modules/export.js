/**
 * EXPORT MANAGER - Gestor de Exportación de Resultados
 */

export class ExportManager {
    constructor() {}

    downloadJSON(results) {
        const data = {
            config: results.config,
            metrics: results.metrics,
            totalServed: results.totalServed,
            totalRejected: results.totalRejected,
            timeSeries: {
                time: results.timeSeries,
                system: results.systemSeries,
                queue: results.queueSeries
            },
            completedJobs: results.completedJobs.map(j => ({
                id: j.id,
                arrivalTime: j.arrivalTime,
                startTime: j.startTime,
                departureTime: j.departureTime,
                waitTime: j.startTime - j.arrivalTime,
                systemTime: j.departureTime - j.arrivalTime
            }))
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `simulacion-colas-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
        
        console.log('Resultados exportados a JSON');
    }

    generateReport(results) {
        const html = this.createReportHTML(results);
        const blob = new Blob([html], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `reporte-simulacion-${Date.now()}.html`;
        a.click();
        URL.revokeObjectURL(url);
        
        console.log('Reporte HTML generado');
    }

    createReportHTML(results) {
        const { config, metrics, totalServed, totalRejected } = results;
        
        return `
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte de Simulación de Colas</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        h1, h2, h3 { color: #2563EB; }
        .section {
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th { background: #2563EB; color: white; }
        .metric { font-family: 'Courier New', monospace; font-weight: bold; }
        .info { color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>📊 Reporte de Simulación de Colas</h1>
    <p class="info">Generado el ${new Date().toLocaleString('es-ES')}</p>
    
    <div class="section">
        <h2>⚙️ Configuración</h2>
        <table>
            <tr><th>Parámetro</th><th>Valor</th></tr>
            <tr><td>Modelo</td><td>${config.model.toUpperCase()}</td></tr>
            <tr><td>Tasa de Llegadas (λ)</td><td class="metric">${config.lambda}</td></tr>
            <tr><td>Tasa de Servicio (μ)</td><td class="metric">${config.mu}</td></tr>
            ${config.c ? `<tr><td>Servidores (c)</td><td class="metric">${config.c}</td></tr>` : ''}
            ${config.k ? `<tr><td>Capacidad (k)</td><td class="metric">${config.k}</td></tr>` : ''}
            <tr><td>Horizonte</td><td class="metric">${config.horizon}</td></tr>
            <tr><td>Warmup</td><td class="metric">${config.warmup}</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>📈 Métricas Finales</h2>
        <table>
            <tr><th>Métrica</th><th>Valor</th><th>Descripción</th></tr>
            <tr>
                <td>ρ (Rho)</td>
                <td class="metric">${metrics.rho.toFixed(4)}</td>
                <td>Utilización del sistema</td>
            </tr>
            <tr>
                <td>L</td>
                <td class="metric">${metrics.L.toFixed(4)}</td>
                <td>Clientes promedio en el sistema</td>
            </tr>
            <tr>
                <td>Lq</td>
                <td class="metric">${metrics.Lq.toFixed(4)}</td>
                <td>Clientes promedio en la cola</td>
            </tr>
            <tr>
                <td>W</td>
                <td class="metric">${metrics.W.toFixed(4)}</td>
                <td>Tiempo promedio en el sistema</td>
            </tr>
            <tr>
                <td>Wq</td>
                <td class="metric">${metrics.Wq.toFixed(4)}</td>
                <td>Tiempo promedio en la cola</td>
            </tr>
        </table>
    </div>
    
    <div class="section">
        <h2>📊 Estadísticas Generales</h2>
        <table>
            <tr><th>Concepto</th><th>Valor</th></tr>
            <tr><td>Clientes Atendidos</td><td class="metric">${totalServed}</td></tr>
            <tr><td>Clientes Rechazados</td><td class="metric">${totalRejected}</td></tr>
            <tr><td>Tiempo de Simulación</td><td class="metric">${config.horizon}</td></tr>
            <tr><td>Tiempo Efectivo</td><td class="metric">${config.horizon - config.warmup}</td></tr>
        </table>
    </div>
    
    <div class="section info">
        <p><strong>Nota:</strong> Este reporte fue generado automáticamente por el Sistema de Simulación de Colas.</p>
    </div>
</body>
</html>
        `;
    }
}
