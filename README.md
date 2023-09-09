# Cross platform (multi)stopwatch and (multi)timer implemented in Python/QT

Time intervals are being saved into file on disk, they survive application restart.

It is possible to create multiple timer/stopwatches and give them a name.

## How to install:
```
python3 -m venv .venv # optional
source .venv/bin/activate # optional

pip install --upgrade pip
pip install -r requirements.txt
```

## How to run multitimer
```
python multitimer.pyw
```
In Windows you can double click multitimer.pyw

## How to run multistopwatch
```
python multistopwatch.pyw
```
In Windows you can double click multistopwatch.pyw

## How to launch game using docker compose

```
docker-compose up
```

Open http://localhost:8080/ in browser. Click on `vnc_auto.html`
