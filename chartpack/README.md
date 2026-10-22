# Chartpack de Expectativas (Estudios Económicos Santander)

`actualizar_chartpack.py` descarga los datos y regenera las 10 láminas del chartpack
(IMCE, expectativas EEE/EOF, compensación inflacionaria, EDEP/EPN, GSCPI, TCN/TCM, SPC,
EEE de actividad e IMCE vs. Imacec no minero). Mantiene el formato Santander: portada,
logo, títulos en rojo #EC0000, Calibri y la paleta de colores de los gráficos originales.

## Uso

```bash
pip install pandas matplotlib python-pptx requests openpyxl
export BCCH_USER="correo registrado en la BDE"
export BCCH_PASS="api key de la BDE"     # no la suba al repositorio
python actualizar_chartpack.py
```

El resultado queda en `salida/AAAAMMDD_Chartpack_Expectativas.pptx` (y `.pdf` si está
instalado LibreOffice). Los datos llegan hasta la fecha de ejecución.

## Revisión de series

Los códigos de la BDE se resuelven por palabras clave contra el catálogo (`SearchSeries`).
Revise `salida/series_resueltas.csv`: muestra el código y título elegidos y las alternativas.
Si alguna serie no es la correcta, fije su código en el diccionario `SERIES`:

```python
"imce_pre_com": dict(frec=["MONTHLY"], codigo="F0XX.XXX.XXX.M"),
```

Para buscar códigos: `python actualizar_chartpack.py --buscar "imce precio comercio"`.

El GSCPI (costos de transporte) se descarga de la Fed de Nueva York; si no hay acceso,
use `--gscpi ruta/gscpi_data.xlsx`.
