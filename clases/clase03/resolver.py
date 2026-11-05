"""Prácticos A y B, ejercicios 1 a 8. Datos de caja negra del docente.
Fuente: DavytJ/Introduccion-a-la-ciencia-de-datos, clases/clase3.
Solución escrita con asistencia de Codex, 05/11/2026.
"""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from funciones.utilidades import validar_objetos

SALIDA = RAIZ / 'salidas' / 'clase03'
SALIDA.mkdir(parents=True, exist_ok=True)

def main():
    df = pd.DataFrame({
        'objeto_id':range(1,11),
        'textura':['suave','rugoso','poroso','suave','rugoso','suave','poroso','rugoso','suave','poroso'],
        'rigidez':['blando','rígido','medio','blando','rígido','rígido','blando','medio','medio','blando'],
        'num_aristas':[0,8,0,4,12,0,0,6,4,0],
        'peso_estimado_g':[45.,120.5,15.,85.,210.,35.,18.5,95.,70.,22.],
        'certeza_observador':[5,4,3,5,4,2,4,3,4,3]})
    df['textura'] = pd.Categorical(df['textura'], categories=['suave','rugoso','poroso'])
    df['rigidez'] = pd.Categorical(df['rigidez'], categories=['blando','medio','rígido'], ordered=True)
    df['certeza_observador'] = pd.Categorical(df['certeza_observador'], categories=range(1,6), ordered=True)
    assert (df['rigidez'] > 'blando').sum() == 6
    assert not any(str(t) in ('object','str','string') for t in df.dtypes)
    roto = df.copy()
    roto.loc[0,'peso_estimado_g'] = -12.
    roto.loc[3,'num_aristas'] = -1
    roto.loc[7,'objeto_id'] = 1
    assert validar_objetos(df) == []
    assert len(validar_objetos(roto)) == 3
    filas = [
        ['objeto_id','identificador','sin unidad','numeración en la actividad','único y no vacío','vacío'],
        ['textura','categórica nominal','sin unidad','clasificación táctil propuesta; protocolo real no aportado','suave/rugoso/poroso','vacío'],
        ['rigidez','categórica ordinal','sin unidad','clasificación táctil propuesta; protocolo real no aportado','blando < medio < rígido','vacío'],
        ['num_aristas','conteo entero','aristas','conteo táctil propuesto; 0 es ausencia de aristas, no desconocimiento','entero >= 0','vacío si no se pudo contar'],
        ['peso_estimado_g','numérica continua','gramos','ejemplo docente: estimación táctil, 15 s, sin ver el objeto','> 0','vacío'],
        ['certeza_observador','categórica ordinal','escala 1-5','autoevaluación propuesta al terminar la observación','1 a 5','vacío']]
    diccionario = pd.DataFrame(filas, columns=['variable','tipo','unidad','instrumento','rango_valido','faltante'])
    diccionario.to_csv(SALIDA/'diccionario_variables.csv', index=False)
    assert diccionario.shape == (6,6) and diccionario['faltante'].notna().all()

    # 4: demostrar las pérdidas, corregir y contrastar con parquet.
    df.to_csv(SALIDA/'con_indice.csv')
    malo = pd.read_csv(SALIDA/'con_indice.csv')
    assert 'Unnamed: 0' in malo and str(malo['rigidez'].dtype) != 'category'
    df.to_csv(SALIDA/'caja_negra.csv', index=False)
    leido = pd.read_csv(SALIDA/'caja_negra.csv')
    leido['rigidez'] = pd.Categorical(leido['rigidez'], categories=['blando','medio','rígido'], ordered=True)
    assert list(leido.columns) == list(df.columns)
    assert leido['rigidez'].cat.ordered
    df.to_parquet(SALIDA/'caja_negra.parquet', index=False)
    assert pd.read_parquet(SALIDA/'caja_negra.parquet')['rigidez'].cat.ordered

    # 5: generar el mismo problema de formato antes de resolverlo.
    df.to_csv(SALIDA/'excel.csv', sep=';', decimal=',', encoding='latin1', index=False)
    try:
        pd.read_csv(SALIDA/'excel.csv')
    except UnicodeDecodeError as error:
        error_excel = f'{type(error).__name__}: {error}'
    else:
        raise AssertionError('Se esperaba el fallo de codificación del archivo de práctica')
    bueno = pd.read_csv(SALIDA/'excel.csv', sep=';', decimal=',', encoding='latin1')
    sin_decimal = pd.read_csv(SALIDA/'excel.csv', sep=';', encoding='latin1')
    assert pd.api.types.is_numeric_dtype(bueno['peso_estimado_g'])
    assert not pd.api.types.is_numeric_dtype(sin_decimal['peso_estimado_g'])

    # 6: la ruta se construye a partir del script, no de la carpeta de la consola.
    ruta = SALIDA/'caja_negra.csv'
    if not ruta.exists():
        raise FileNotFoundError(f'Falta {ruta}; ejecutar este script desde el principio')
    assert pd.read_csv(ruta).shape == (10,6)

    # 7: cuatro formas de codificar el mismo fenómeno: ausencia de medición.
    faltantes = df.astype(object)
    faltantes.loc[[2,6],'peso_estimado_g'] = -99
    faltantes.loc[5,'textura'] = 's/d'
    faltantes.loc[8,'num_aristas'] = 'NA'
    faltantes.loc[1,'certeza_observador'] = ''
    faltantes.to_csv(SALIDA/'faltantes.csv', index=False)
    ingenuo = pd.read_csv(SALIDA/'faltantes.csv')
    declarado = pd.read_csv(SALIDA/'faltantes.csv', na_values=[-99,'s/d'])
    assert declarado['peso_estimado_g'].isna().sum() == 2
    print('Valores únicos:', {c: sorted(faltantes[c].astype(str).unique()) for c in faltantes})
    comparacion = pd.DataFrame({'sin_declarar':ingenuo.isna().sum(),'declarados':declarado.isna().sum()})
    comparacion.to_csv(SALIDA/'conteo_faltantes.csv')

    # 8: reproducir el archivo vecino con la misma semilla del generador docente.
    rng = np.random.default_rng(42)
    suc = rng.choice(['Centro','Pocitos ',' Carrasco','Centro '], 40)
    montos = np.round(rng.gamma(2.,900.,40),0)
    vecino = pd.DataFrame({'ID Transaccion':range(1001,1041),
        'Fecha Operacion':pd.date_range('2026-03-02',periods=40).strftime('%d/%m/%Y'),
        'Sucursal ':suc, 'Monto UYU':[f'{m:,.0f}'.replace(',','.') for m in montos],
        'Medio de Pago':rng.choice(['debito','credito','efectivo'],40)})
    vecino.to_csv(SALIDA/'vecino.csv', index=False)
    lectura_mala = pd.read_csv(SALIDA/'vecino.csv')
    limpio = pd.read_csv(SALIDA/'vecino.csv', thousands='.')
    limpio.columns = limpio.columns.str.strip().str.lower().str.replace(' ','_')
    limpio['fecha_operacion'] = pd.to_datetime(limpio['fecha_operacion'],format='%d/%m/%Y')
    for c in ['sucursal','medio_de_pago']:
        limpio[c] = limpio[c].str.strip().astype('category')
    assert limpio['sucursal'].nunique() == 3
    assert limpio['monto_uyu'].sum() == montos.sum()
    limpio.to_csv(SALIDA/'vecino_limpio.csv', index=False)
    limpio.describe(include='all').to_csv(SALIDA/'perfil_vecino.csv')
    informe = f'''# Resultados de clase 3

Ejercicios 1-4: tipos declarados; seis objetos por encima de blando; validación correcta sin problemas y copia rota con tres problemas. Diccionario de 6 x 6. CSV pierde categorías; parquet conserva rigidez ordenada.

Ejercicio 5, error real del intento sin configuración:

```text
{error_excel}
```

El separador es punto y coma, el decimal es coma y la codificación latin1. Omitir decimal no detiene el programa: deja el peso como texto.

Ejercicio 6: la ruta parte de __file__. Una ruta con el nombre de usuario de otra persona no describe la estructura compartida.

Ejercicio 7: media ingenua {ingenuo['peso_estimado_g'].mean():.4f} g; media declarada {declarado['peso_estimado_g'].mean():.4f} g. Pandas reconoce NA y vacío; hay que declarar -99 y s/d. Es un problema de representación de una medición ausente que contamina el cálculo.

Ejercicio 8: monto medio ingenuo {lectura_mala['Monto UYU'].mean():.4f}; correcto {limpio['monto_uyu'].mean():.4f} UYU. Hay 40 transacciones, fechas con día primero y tres sucursales tras quitar espacios. Son propiedades del archivo; no prueban cómo se recolectó. Pregunta al productor: ¿cada fila representa una venta final, e incluye devoluciones e impuestos?

Un cero de aristas es una medición si se constató que el objeto no tiene aristas. Si no se pudieron contar, corresponde un faltante. El diccionario debe precisar ambas convenciones en instrumento y faltante.

Desafío de equipo: pendiente de confirmar el tema y la unidad de observación del equipo; no se inventó una entrega grupal.
'''
    (SALIDA/'resultados.md').write_text(informe, encoding='utf-8')
    print(informe)

if __name__ == '__main__':
    main()
