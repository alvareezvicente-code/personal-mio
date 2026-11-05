# Leer un CSV y verificar su interpretación

1. Inspeccionar el texto del encabezado y algunas filas antes de elegir el lector.
2. Declarar separador, decimal, codificación y códigos de ausencia.
3. Revisar cantidad de filas, columnas, dtypes, faltantes y duplicados.
4. Comparar uno o dos importes con el texto original; una lectura sin errores puede ser incorrecta.

```python
df = pd.read_csv(ruta, sep=';', decimal=',', encoding='latin1', na_values=['s/d', -99])
assert pd.api.types.is_numeric_dtype(df['peso_estimado_g'])
```

Estos argumentos sirven para el archivo de práctica de clase 3; no se aplican ciegamente a otras fuentes.
