# AI Dev News Feed — Dashboard

Stack minimale: Flask + HTML/CSS/JS vanilla + JSON come storage.

## Struttura

- `items.json` — DB articoli (titolo, url, descrizione, stato lettura)
- `news_server.py` — backend Flask: serve UI + API read/unread
- `index.html` — UI card-based, dark mode, responsive
- `sync_to_github.sh` — commit + push automatico su GitHub

## Avvio locale

```bash
pip install --user flask
python3 news_server.py
```

Poi apri `http://localhost:8765`

## API

- `GET /api/items` — lista articoli
- `POST /api/items/<id>/read`
- `POST /api/items/<id>/unread`

## Sincronizzazione GitHub

```bash
./sync_to_github.sh /percorso/del/repo
```
