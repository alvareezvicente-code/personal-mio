"""Casos de borde: faltantes, huecos temporales y uniones que duplican."""
import unittest
import pandas as pd
from utilidades import validar_objetos, media_movil_horaria, union_izquierda

class Controles(unittest.TestCase):
    def test_todos_los_problemas(self):
        df = pd.DataFrame({'objeto_id':[1,1], 'peso_estimado_g':[1,None],
                           'certeza_observador':[2,6], 'num_aristas':[0,1.5]})
        self.assertEqual(len(validar_objetos(df)), 4)

    def test_no_saltar_huecos(self):
        indice = pd.date_range('2024-01-01', periods=10, freq='h').delete(4)
        self.assertTrue(media_movil_horaria(pd.Series(10., index=indice)).isna().all())
        completa = pd.Series(10., index=pd.date_range('2024-01-01', periods=8, freq='h'))
        self.assertEqual(media_movil_horaria(completa).iloc[-1], 10.)

    def test_union_no_multiplica(self):
        izquierda = pd.DataFrame({'id':[1,2]})
        derecha = pd.DataFrame({'id':[1,1], 'x':[3,4]})
        with self.assertRaises(pd.errors.MergeError):
            union_izquierda(izquierda, derecha, ['id'])
        resultado = union_izquierda(izquierda, derecha.iloc[:1], ['id'])
        self.assertEqual(len(resultado), 2)
        self.assertTrue(pd.isna(resultado.loc[1,'x']))

if __name__ == '__main__':
    unittest.main()
