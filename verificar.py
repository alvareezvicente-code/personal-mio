"""Comprobación local: scripts desde una carpeta ajena, casos de borde y tickets.
No descarga datos ni realiza solicitudes a servicios de IA.
"""
from pathlib import Path
import os
import runpy
import sys
import tempfile
import unittest
RAIZ=Path(__file__).resolve().parent
sys.path.insert(0,str(RAIZ))

def main():
    original=Path.cwd()
    with tempfile.TemporaryDirectory() as otra:
        os.chdir(otra)
        try:
            for archivo in ['clases/clase03/resolver.py','clases/clase05/inspeccionar.py',
                'clases/clase07/ozono.py','clases/clase10/transito_aire.py',
                'clases/clase12/resolver.py','clases/clase14/resolver.py']:
                print('\nCOMPROBANDO',archivo,flush=True)
                runpy.run_path(str(RAIZ/archivo),run_name='__main__')
            sys.path.insert(0,str(RAIZ/'funciones'))
            casos=runpy.run_path(str(RAIZ/'funciones'/'test_utilidades.py'))
            resultado=unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(casos['Controles']))
            if not resultado.wasSuccessful():
                raise AssertionError('Fallaron las pruebas de utilidades')
            ticket=runpy.run_path(str(RAIZ/'clases'/'clase11'/'leer_ticket.py'))
            validar=ticket['verificar_csv']
            tabla,suma=validar('descripcion,monto\nPan,50.25\nLeche,40.75','91.00')
            assert float(suma)==91 and len(tabla)==2
            for texto,total in [('descripcion,monto\nPan,50','60'),('descripcion,monto\nPan,','0'),
                 ('otra,monto\nPan,50','50'),('descripcion,monto\nPan,NaN','0')]:
                try:
                    validar(texto,total)
                except ValueError:
                    pass
                else:
                    raise AssertionError('El ticket inválido pasó el control')
            sys.argv=['leer_ticket.py']
            ticket['main']()
        finally:
            os.chdir(original)
    print('\nTODAS LAS COMPROBACIONES PASARON',flush=True)

if __name__=='__main__':
    main()
