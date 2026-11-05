# Fuentes y obtención

Descargas efectuadas el 05/11/2026. El registro reproducible conserva URL, fecha con zona horaria, tamaño y SHA256; cada nueva ejecución registra su propia descarga, no una fecha inventada.

| Fuente | Unidad | Filas verificadas | Origen |
|---|---|---:|---|
| Empresas DEI, corte 30/03/2023 | Empresa registrada | 1.422 | [MIEM](https://catalogodatos.gub.uy/dataset/miem-dei) |
| Ozono enero-abril 2024 | Estación y registro minutal | 291.926 | [Intendencia de Montevideo](https://catalogodatos.gub.uy/dataset/calidad-del-aire-ozono-o3) |
| Tránsito-aire junio 2024 | Estación y hora | 2.160 | [Tabla preparada por el docente](https://github.com/DavytJ/Introduccion-a-la-ciencia-de-datos/blob/71cbebe1b3cd96d58b4bc9789fd016c7ac874cbd/clases/clase10/transito_aire_junio2024.csv) |
| Ticket de ejemplo | Imagen de comprobante | Una imagen | [Material de clase 11](https://github.com/DavytJ/Introduccion-a-la-ciencia-de-datos/tree/71cbebe1b3cd96d58b4bc9789fd016c7ac874cbd/clases/clase11/clase_ia) |
| Residuos 2023 | Registro de pesada | 1.222 | Archivo local previo; URL original en el script de residuos |

Ozono contiene registros hasta el 29/04/2024, aunque el nombre abarque abril. El DEI se procesa localmente porque contiene nombres y contactos; solo se publican sus perfiles agregados.

Los enlaces exactos de descarga están en `obtener_datos.py`. Para condiciones de reutilización, consultar las fichas originales y su campo de licencia. La tabla preparada y la imagen son material docente atribuido; no se les asigna una licencia que no se haya confirmado.

Los nuevos datos crudos se ignoran en Git. Los CSV de residuos ya estaban publicados en el repositorio antes de esta ampliación; este cambio no reescribe ese historial.
