# Terroir Project

**Data‑driven site‑selection for Argentine vineyards**

![Interactive heatmap of vineyard suitability and existing vineyards in Argentina](https://i.ibb.co/n8fkCGD/Terroir.png)

## Overview
Terroir Project is an open‑source spatial‑analytics pipeline that helps winegrowers quantify and visualise the suitability of potential vineyard sites across Argentina. It blends historical climate normals, topographic variables and the locations of existing high‑performing vineyards to predict a _Terroir Score_ for every 1 km² cell in the country.

## How it works
1. **Data ingestion**
   - 30‑year (1991‑2020) temperature & precipitation normals from WorldClim v2.
   - Digital elevation model (SRTM 30 m).
   - Geocoded database of commercial vineyards and their quality ratings.

2. **Feature engineering**
   - Bioclimatic indices: Growing Degree Days, Huglin Index, Dry‑month count, etc.
   - Terrain descriptors: elevation, slope, aspect.

3. **Modelling**
   - Gradient‑boosted regression (scikit‑learn) trained on vineyard quality vs predictors.
   - 10‑fold spatial cross‑validation and permutation feature importance.

## Interactive web map

An interactive prototype (see screenshot above) lets you explore both layers directly in the browser:

- **Toggle Vineyards Layer** — displays existing estates as blue‑ring hotspots.
- **Toggle Scoring Layer** — shows modelled suitability as a green‑to‑red heat‑map.
- Real‑time controls to tweak each layer’s colour gradient, point radius and opacity.

The viewer is written in vanilla JavaScript on top of the Google Maps JavaScript API. The watermark “For development purposes only” that you can see in development builds disappears once you supply a billing‑enabled API key.

## Why use it
- **Objective** — moves beyond anecdotal “old‑vine wisdom”.
- **Transparent** — fully reproducible with open data and Python.
- **Actionable** — export GeoTIFF/GeoJSON to any GIS for site scouting.

## Quick start
```bash
git clone https://github.com/your‑org/terroir‑project.git
cd terroir‑project
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # matplotlib, scikit‑learn, numpy, geopandas, rasterio …
```

## Contributing
Pull requests are welcome! Please open an issue to discuss major changes first.

## License
Released under the GNU General Public License v3.0 – see `LICENSE` for details.

## Citation
If you use this code or data, please cite:
> Terroir Project (2025). *Site‑selection modelling for Argentine vineyards*. GitHub repository.
