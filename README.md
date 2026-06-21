# Antas AI News — Dashboard

Stack statico: HTML + CSS + JS vanilla, nessun backend.

## Struttura

- `items.json` — database articoli (titolo, url, descrizione, stato lettura)
- `index.html` — UI card-based, dark mode, responsive
- `sync_to_github.sh` — commit + push automatico su GitHub

## Avvio locale

```bash
python3 -m http.server 8765
```

Poi apri `http://localhost:8765`

## Funzionamento

- `index.html` carica direttamente `items.json` con `fetch('items.json')`
- Nessun server Python o API: tutto gira nel browser
- Lo stato "letto/non letto" è salvato nel `localStorage` del browser
- Se vuoi, puoi servire la cartella con qualsiasi server statico o aprirla direttamente, ma il fetch funziona meglio via HTTP locale

## Sito pubblico

Dashboard disponibile su GitHub Pages:
[https://emaxgms.github.io/Antas-ai-news-feed/](https://emaxgms.github.io/Antas-ai-news-feed/)

## Sincronizzazione GitHub

```bash
./sync_to_github.sh /percorso/del/repo
```
