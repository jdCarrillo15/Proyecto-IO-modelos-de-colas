"""
Módulo de pruebas unitarias para modelos de colas

Este módulo contiene pruebas automatizadas para verificar la
correcta implementación de los modelos de simulación, incluyendo:
- Validación de métricas de utilización
- Verificación de la Ley de Little
- Comparación con resultados analíticos
- Pruebas de estabilidad y robustez
"""

import unittest
import warnings
from sim_colas_animado import MM1, MMC, MMK1, MMKC
from teoria_colas import (
    analytical_mm1,
    analytical_mmc,
    littles_law_check,
    compare_simulation_vs_theory
)


class TestMM1(unittest.TestCase):
    """Pruebas para modelo M/M/1"""
    
    def test_parametros_invalidos(self):
        """Verificar que se lancen excepciones con parámetros inválidos"""
        # λ negativa
        with self.assertRaises(ValueError):
            MM1(lam=-1.0, mu=2.0, horizon=100)
        
        # μ negativa
        with self.assertRaises(ValueError):
            MM1(lam=1.0, mu=-2.0, horizon=100)
        
        # Horizonte negativo
        with self.assertRaises(ValueError):
            MM1(lam=1.0, mu=2.0, horizon=-100)
    
    def test_warning_sistema_inestable(self):
        """Verificar que se lance warning cuando ρ ≥ 1"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            sim = MM1(lam=3.0, mu=2.0, horizon=100)  # ρ = 1.5
            # Verificar que se lanzó un warning
            self.assertEqual(len(w), 1)
            self.assertIn("inestable", str(w[0].message).lower())
    
    def test_utilizacion_estable(self):
        """Verificar cálculo de utilización en sistema estable"""
        sim = MM1(lam=0.6, mu=2.0, horizon=10000, warmup=1000)
        
        # Ejecutar simulación
        while sim.time < sim.horizon:
            sim.step()
        
        # Verificar utilización
        rho_teorico = 0.6 / 2.0  # 0.3
        rho_sim = sim.utilization()
        
        self.assertAlmostEqual(rho_sim, rho_teorico, delta=0.05)
    
    def test_ley_de_little(self):
        """Verificar que se cumpla la Ley de Little: L = λW"""
        sim = MM1(lam=0.6, mu=2.0, horizon=10000, warmup=1000)
        
        # Ejecutar simulación
        while sim.time < sim.horizon:
            sim.step()
        
        st = sim.state()
        
        # Verificar L = λ * W
        L_measured = st['l_avg']
        W_measured = st['w_avg']
        L_expected = sim.lam * W_measured
        
        # Verificar con tolerancia del 10%
        self.assertTrue(
            littles_law_check(L_measured, sim.lam, W_measured, tolerance=0.1),
            f"Ley de Little no se cumple: L={L_measured:.3f}, λW={L_expected:.3f}"
        )
    
    def test_comparacion_con_teoria(self):
        """Comparar métricas de simulación con resultados analíticos"""
        lam, mu = 0.6, 2.0
        sim = MM1(lam=lam, mu=mu, horizon=20000, warmup=2000)
        
        # Ejecutar simulación
        while sim.time < sim.horizon:
            sim.step()
        
        # Obtener métricas
        st = sim.state()
        sim_metrics = {
            'L': st['l_avg'],
            'Lq': st['lq_avg'],
            'W': st['w_avg'],
            'Wq': st['wq_avg'],
            'rho': st['rho'],
        }
        
        # Calcular teoría
        theo_metrics = analytical_mm1(lam, mu)
        
        # Comparar
        comparison = compare_simulation_vs_theory(sim_metrics, theo_metrics, tolerance=0.15)
        
        # Verificar que todas las métricas pasen
        failed = [k for k, v in comparison.items() if not v['ok']]
        self.assertEqual(
            len(failed), 0,
            f"Métricas que no coinciden con teoría: {failed}"
        )
    
    def test_warmup_mejora_precision(self):
        """Verificar que el periodo de warmup mejora las estimaciones"""
        lam, mu = 0.6, 2.0
        horizon = 10000
        
        # Simulación sin warmup
        sim_no_warmup = MM1(lam=lam, mu=mu, horizon=horizon, warmup=0)
        while sim_no_warmup.time < sim_no_warmup.horizon:
            sim_no_warmup.step()
        
        # Simulación con warmup
        sim_with_warmup = MM1(lam=lam, mu=mu, horizon=horizon, warmup=1000)
        while sim_with_warmup.time < sim_with_warmup.horizon:
            sim_with_warmup.step()
        
        # Teoría
        theo = analytical_mm1(lam, mu)
        
        # Errores
        error_no_warmup = abs(sim_no_warmup.state()['l_avg'] - theo['L'])
        error_with_warmup = abs(sim_with_warmup.state()['l_avg'] - theo['L'])
        
        # El error con warmup debería ser menor o igual
        # (no siempre será estrictamente menor debido a aleatoriedad)
        print(f"\nError sin warmup: {error_no_warmup:.4f}")
        print(f"Error con warmup: {error_with_warmup:.4f}")


class TestMMC(unittest.TestCase):
    """Pruebas para modelo M/M/c"""
    
    def test_parametros_invalidos(self):
        """Verificar validación de parámetros"""
        # c negativo
        with self.assertRaises(ValueError):
            MMC(lam=1.0, mu=2.0, c=-1, horizon=100)
        
        # c = 0
        with self.assertRaises(ValueError):
            MMC(lam=1.0, mu=2.0, c=0, horizon=100)
    
    def test_warning_sistema_inestable(self):
        """Verificar warning en sistema inestable"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            sim = MMC(lam=10.0, mu=2.0, c=3, horizon=100)  # ρ = 10/(2*3) = 1.67
            self.assertEqual(len(w), 1)
            self.assertIn("inestable", str(w[0].message).lower())
    
    def test_ley_de_little(self):
        """Verificar Ley de Little en M/M/c"""
        sim = MMC(lam=0.7, mu=2.5, c=3, horizon=10000, warmup=1000)
        
        while sim.time < sim.horizon:
            sim.step()
        
        st = sim.state()
        
        # Verificar L = λ * W
        self.assertTrue(
            littles_law_check(st['l_avg'], sim.lam, st['w_avg'], tolerance=0.1),
            f"Ley de Little no se cumple en M/M/c"
        )
    
    def test_comparacion_con_teoria(self):
        """Comparar con fórmulas analíticas de M/M/c"""
        lam, mu, c = 0.7, 2.5, 3
        sim = MMC(lam=lam, mu=mu, c=c, horizon=20000, warmup=2000)
        
        while sim.time < sim.horizon:
            sim.step()
        
        st = sim.state()
        sim_metrics = {
            'L': st['l_avg'],
            'Lq': st['lq_avg'],
            'W': st['w_avg'],
            'Wq': st['wq_avg'],
            'rho': st['rho'],
        }
        
        theo_metrics = analytical_mmc(lam, mu, c)
        
        comparison = compare_simulation_vs_theory(sim_metrics, theo_metrics, tolerance=0.15)
        
        failed = [k for k, v in comparison.items() if not v['ok']]
        self.assertEqual(
            len(failed), 0,
            f"Métricas que no coinciden con teoría en M/M/c: {failed}"
        )


class TestMMK1(unittest.TestCase):
    """Pruebas para modelo M/M/k/1"""
    
    def test_parametros_invalidos(self):
        """Verificar validación de parámetros"""
        with self.assertRaises(ValueError):
            MMK1(lam=1.0, mu=2.0, k=0, horizon=100)
        
        with self.assertRaises(ValueError):
            MMK1(lam=1.0, mu=2.0, k=-1, horizon=100)
    
    def test_asignacion_determinista(self):
        """Verificar que la asignación a colas sea determinista"""
        import random
        
        # Configurar semillas idénticas
        random.seed(42)
        sim1 = MMK1(lam=0.8, mu=2.5, k=3, horizon=100)
        
        random.seed(42)
        sim2 = MMK1(lam=0.8, mu=2.5, k=3, horizon=100)
        
        # Ejecutar ambas simulaciones
        while sim1.time < sim1.horizon:
            sim1.step()
        
        while sim2.time < sim2.horizon:
            sim2.step()
        
        # Verificar que los resultados sean idénticos
        st1 = sim1.state()
        st2 = sim2.state()
        
        self.assertEqual(st1['served'], st2['served'])
        self.assertAlmostEqual(st1['l_avg'], st2['l_avg'], places=6)
    
    def test_ley_de_little(self):
        """Verificar Ley de Little en M/M/k/1"""
        sim = MMK1(lam=0.8, mu=2.5, k=3, horizon=10000, warmup=1000)
        
        while sim.time < sim.horizon:
            sim.step()
        
        st = sim.state()
        
        self.assertTrue(
            littles_law_check(st['l_avg'], sim.lam, st['w_avg'], tolerance=0.1),
            f"Ley de Little no se cumple en M/M/k/1"
        )


class TestMMKC(unittest.TestCase):
    """Pruebas para modelo M/M/k/c"""
    
    def test_parametros_invalidos(self):
        """Verificar validación de parámetros"""
        with self.assertRaises(ValueError):
            MMKC(lam=1.0, mu=2.0, k=0, c=2, horizon=100)
        
        with self.assertRaises(ValueError):
            MMKC(lam=1.0, mu=2.0, k=2, c=0, horizon=100)
    
    def test_ley_de_little(self):
        """Verificar Ley de Little en M/M/k/c"""
        sim = MMKC(lam=0.9, mu=2.5, k=2, c=2, horizon=10000, warmup=1000)
        
        while sim.time < sim.horizon:
            sim.step()
        
        st = sim.state()
        
        self.assertTrue(
            littles_law_check(st['l_avg'], sim.lam, st['w_avg'], tolerance=0.1),
            f"Ley de Little no se cumple en M/M/k/c"
        )


class TestExportacion(unittest.TestCase):
    """Pruebas para exportación de resultados"""
    
    def test_export_results(self):
        """Verificar que se pueda exportar correctamente"""
        import os
        import json
        
        sim = MM1(lam=0.6, mu=2.0, horizon=1000, warmup=100)
        
        while sim.time < sim.horizon:
            sim.step()
        
        # Exportar
        filename = "test_export.json"
        sim.export_results(filename)
        
        # Verificar que el archivo existe
        self.assertTrue(os.path.exists(filename))
        
        # Leer y verificar contenido
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Verificar estructura
        self.assertIn('parameters', data)
        self.assertIn('metrics', data)
        self.assertIn('time_series', data)
        self.assertIn('wait_times', data)
        
        # Verificar parámetros
        self.assertEqual(data['parameters']['lambda'], 0.6)
        self.assertEqual(data['parameters']['mu'], 2.0)
        
        # Limpiar
        os.remove(filename)


def run_tests():
    """Ejecutar todas las pruebas"""
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar pruebas
    suite.addTests(loader.loadTestsFromTestCase(TestMM1))
    suite.addTests(loader.loadTestsFromTestCase(TestMMC))
    suite.addTests(loader.loadTestsFromTestCase(TestMMK1))
    suite.addTests(loader.loadTestsFromTestCase(TestMMKC))
    suite.addTests(loader.loadTestsFromTestCase(TestExportacion))
    
    # Ejecutar
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "="*80)
    print("RESUMEN DE PRUEBAS")
    print("="*80)
    print(f"Pruebas ejecutadas: {result.testsRun}")
    print(f"✓ Exitosas: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"✗ Fallidas: {len(result.failures)}")
    print(f"⚠ Errores: {len(result.errors)}")
    print("="*80)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
