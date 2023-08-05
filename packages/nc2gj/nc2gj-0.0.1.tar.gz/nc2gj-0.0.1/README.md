# ecfas_geojson

## Dependencies
geopandas==0.10.2

Conversion of the ecfas nc coastal TWL time-series to geojson format

## usage
Specify the following arguments:

- -r <region> : Region, matching the 6 Copernicus Marine Service regional domains.

- -o <outputdir>: Output directory where the regional forecasts are saved.
- -t <%Y%m%d_%H%M%S>: Bulleting date for the forecast data. Default: Forecast update time of execution day

nc2geojson -r <region> -o <outputdir> -t <%Y%m%d_%H%M%S>
