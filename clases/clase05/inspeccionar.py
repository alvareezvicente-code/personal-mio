"""Carga e inspección de residuos (trabajo previo) y del DEI (ampliación).
Referencia: ejemplo de carga de clase 5 del docente.
Solo se publican perfiles agregados, no los nombres/contactos del DEI.
"""
from pathlib import Path
import pandas as pd
RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ/'salidas'/'clase05'
SALIDA.mkdir(parents=True, exist_ok=True)

def perfil(df, nombre):
    resultado = pd.DataFrame({'tipo':df.dtypes.astype(str),'faltantes':df.isna().sum(),
                              'valores_distintos':df.nunique(dropna=True)})
    resultado.to_csv(SALIDA/f'{nombre}_perfil.csv')
    return f'{nombre}: {df.shape[0]} filas, {df.shape[1]} columnas, {df.duplicated().sum()} duplicadas exactas.'

def main():
    mensajes = []
    residuos = pd.read_csv(RAIZ/'data'/'residuos_2023.csv')
    mensajes.append(perfil(residuos, 'residuos_2023'))
    mensajes.append('Matrículas distintas no equivalen a pesadas distintas: un vehículo puede tener varios viajes.')
    empresas = pd.read_csv(RAIZ/'data'/'empresasdei_20230330.csv',na_values=['S/D','s/d'])
    empresas.columns = empresas.columns.str.strip()
    for col in empresas.select_dtypes(include=['object','str','string']):
        empresas[col] = empresas[col].str.replace('\u200b','',regex=False).str.strip()
    mensajes.append(perfil(empresas,'empresas_dei'))
    # Comprobar candidatos a clave; no publicar sus valores.
    for col in empresas:
        if 'rut' in col.lower():
            mensajes.append(f'Columna {col}: {empresas[col].isna().sum()} faltantes y {empresas[col].duplicated().sum()} repetidos.')
    mensajes.append('No se eliminan filas por tener un faltante en cualquier columna: el análisis debe definir qué variables necesita.')
    (SALIDA/'resultados.md').write_text('# Clase 5: carga e inspección\n\n'+'\n\n'.join(mensajes),encoding='utf-8')
    print('\n'.join(mensajes))

if __name__ == '__main__':
    main()
