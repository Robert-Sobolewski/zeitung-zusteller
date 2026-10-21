# maps/ — lokalny serwer kafelków (opcjonalne)

Serwis `openfreemap` w docker-compose.yml działa pod profilem `maps`:

```bash
docker compose --profile maps up -d openfreemap
```

- `config.json` — placeholder; schemat zweryfikować z dokumentacją tileserver-gl przy Fazie 5
- `data/` — lokalne dane OSM (.pbf/.mvt) dla offline map (gitignore)

Alternatywa (Faza 5): frontend pobiera kafelki OpenFreeMap (https://tiles.openfreemap.org,
bez API key) i cache'uje je w IndexedDB przez Workbox → mapa działa offline bez lokalnego serwera.
