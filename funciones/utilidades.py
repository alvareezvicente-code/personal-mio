"""Controles reutilizables. Los errores informan la causa antes de analizar."""
from pathlib import Path
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]

def validar_objetos(datos):
    """Lista de restricciones incumplidas; no se detiene en la primera."""
    problemas = []
    for col, condicion, mensaje in [
        ('peso_estimado_g', lambda x: x > 0, 'peso no positivo o ausente'),
        ('certeza_observador', lambda x: x.between(1, 5), 'certeza fuera de 1 a 5 o ausente'),
        ('num_aristas', lambda x: (x >= 0) & (x % 1 == 0), 'aristas no enteras, negativas o ausentes'),
    ]:
        valores = pd.to_numeric(datos[col].astype(object), errors='coerce')
        cantidad = (~condicion(valores).fillna(False)).sum()
        if cantidad:
            problemas.append(f'{mensaje}: {cantidad}')
    repetidos = datos['objeto_id'].duplicated().sum()
    if repetidos:
        problemas.append(f'identificadores repetidos: {repetidos}')
    if datos['objeto_id'].isna().any():
        problemas.append('identificadores ausentes')
    return problemas

def media_movil_horaria(serie, horas=8):
    """Reindexa a horas completas: una ventana no puede saltarse horas sin dato."""
    if not isinstance(serie.index, pd.DatetimeIndex) or serie.index.has_duplicates:
        raise ValueError('Se necesita un índice de fechas único')
    return serie.sort_index().asfreq('h').rolling(horas, min_periods=horas).mean()

def union_izquierda(izquierda, derecha, claves):
    """Unión muchos-a-uno; falla si la tabla derecha puede multiplicar filas."""
    return izquierda.merge(derecha, on=claves, how='left', validate='many_to_one')

def preparar_aire(ruta=None):
    """Conserva el reloj UTC rotulado en el CSV, igual que la consigna Python.
    No afirma que ese reloj represente la hora civil local de los sensores.
    """
    ruta = ruta or RAIZ / 'data' / 'transito_aire_junio2024.csv'
    df = pd.read_csv(ruta, parse_dates=['hora'])
    if df.duplicated(['estacion', 'hora']).any():
        raise ValueError('Hay más de una fila por estación y hora')
    df = df.sort_values(['estacion', 'hora']).copy()
    df['h'] = df['hora'].dt.hour
    df['tipo_dia'] = np.where(df['hora'].dt.dayofweek < 5, 'lunes a viernes', 'fin de semana')
    df['franja'] = pd.cut(df['h'], [-1, 5, 11, 17, 23], labels=['madrugada', 'mañana', 'tarde', 'noche'])
    df['transito_miles'] = df['transito'] / 1000
    df['transito_rel'] = df['transito'] / df.groupby('estacion')['transito'].transform('mean')
    df['log_pm25'] = np.log(df['pm25'].where(df['pm25'] > 0))
    return df
