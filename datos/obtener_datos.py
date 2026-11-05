"""Descargas de fuentes originales, con fecha, URL, tamaño, filas y SHA256.
Los archivos crudos son locales. No subir claves ni datos personales.
"""
from pathlib import Path
from urllib.request import urlretrieve
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
DATA = RAIZ/'data'
CURSO = 'https://raw.githubusercontent.com/DavytJ/Introduccion-a-la-ciencia-de-datos/71cbebe1b3cd96d58b4bc9789fd016c7ac874cbd'
FUENTES = {
 'transito_aire_junio2024.csv': CURSO+'/clases/clase10/transito_aire_junio2024.csv',
 'ticket.jpg': CURSO+'/clases/clase11/clase_ia/ticket.jpg',
 'o3_01_2024_04_2024.csv': 'https://ckan-data.montevideo.gub.uy/dataset/70a1a63d-4157-43c0-9ae6-00fc14dae29a/resource/a97d7ffb-be66-4438-8de8-fa4c7cacf66c/download/o3_01_2024_04_2024.csv',
 'empresasdei_20230330.csv': 'https://catalogodatos.gub.uy/dataset/575ccb87-ae74-4dcd-ba4b-cf050bd8e08a/resource/e56d1949-3e94-42a9-801f-c6d2523b185d/download/empresasdei_20230330.csv',
}

def main():
    DATA.mkdir(exist_ok=True)
    registro = DATA/'manifest_descargas.json'
    historial = json.loads(registro.read_text(encoding='utf-8')) if registro.exists() else {}
    for nombre, url in FUENTES.items():
        destino = DATA/nombre
        if not destino.exists():
            temporal = destino.with_suffix(destino.suffix+'.parcial')
            urlretrieve(url, temporal)
            temporal.replace(destino)
            historial[nombre] = {'obtenido':datetime.now(ZoneInfo('America/Montevideo')).isoformat()}
        info = historial.setdefault(nombre, {'obtenido':None})
        info.update(url=url, bytes=destino.stat().st_size, sha256=hashlib.sha256(destino.read_bytes()).hexdigest())
        if nombre.endswith('.csv'):
            info['filas'] = len(pd.read_csv(destino))
        registro.write_text(json.dumps(historial,ensure_ascii=False,indent=2),encoding='utf-8')
        print(nombre, info.get('filas', 'imagen'), 'registros')

if __name__ == '__main__':
    main()
