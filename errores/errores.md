# Errores y decisiones comprobados

Registro de esta preparación, con asistencia de Codex; no representa errores históricos del estudiante.

| Caso | Cómo se detectó | Corrección |
|---|---|---|
| CSV latin1 leído como UTF-8 | UnicodeDecodeError en el ejercicio generado | Declarar encoding, sep y decimal. |
| Peso como texto por coma decimal | dtype no numérico aun sin excepción | decimal=',' y verificación del tipo. |
| -99 incluido en el promedio | Media 48,45 frente a 85,3125 g al declararlo faltante | na_values y conteo de ausencias por columna. |
| Fecha de corte sin zona frente a índice UTC | TypeError al ejecutar clase 10 | Derivar la fecha de corte del propio índice. |
| Ventana móvil que podría saltar horas | Caso de prueba con una hora eliminada | Reindexar a frecuencia horaria antes de rolling. |
| Unión con clave incompleta | Ejercicio 60 pasa de tres a seis filas | Clave origin + hour y validate='many_to_one'. |

En todos los casos se conserva la diferencia entre dato ausente y cero. Corregir un error de ejecución no verifica por sí solo la interpretación estadística.
