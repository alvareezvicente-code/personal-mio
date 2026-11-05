# Rutas y uniones reproducibles

En un script de `clases/claseXX/`, la raíz es `Path(__file__).resolve().parents[2]`. Construir rutas desde esa raíz permite ejecutarlo desde otra carpeta.

Para agregar atributos sin multiplicar observaciones:

```python
resultado = vuelos.merge(clima, on=['origin', 'hour'], how='left', validate='many_to_one')
assert len(resultado) == len(vuelos)
```

Contar después las filas sin pareja. Una unión izquierda puede conservar todas las filas y dejar atributos faltantes. Si la derecha repite la clave, hay que resolver su unidad de observación antes de unir.
