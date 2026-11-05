# Clase 11: estado de la actividad

Se preparó el envío de la imagen, la interpretación del CSV y la comprobación del total. El modo predeterminado solo arma la solicitud; no transmite datos ni consume una cuenta de IA.

Se probaron la preparación y el validador con ejemplos sintéticos. Falta que el estudiante indique un modelo disponible, use su propia clave, lea el total del ticket y contraste cada renglón. La coincidencia de la suma por sí sola no garantiza una transcripción correcta.

No se inventó una respuesta de Gemini ni se presenta esta actividad como ejecutada de extremo a extremo.

```sh
python clases/clase11/leer_ticket.py
python clases/clase11/leer_ticket.py --enviar --modelo NOMBRE_DISPONIBLE --total TOTAL_LEIDO
```

La clave se toma de la variable de entorno `GEMINI_API_KEY`; no debe escribirse en un archivo público ni en el historial de comandos compartido.
