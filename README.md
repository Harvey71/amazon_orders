# amazon_orders

Crawler für eigene Amazon-Bestellungen.

# Installation

## Voraussetzugen

1. Python 3.7
2. Optional: Virtualenv für Python
3. Ein gültiges Amazon.de-Konto mit bereits getätigten Bestellungen.

## Vorbereitungen

1. Klone das Git-Repository.
2. Optional: Erstelle eine neue virtuelle Python Umgebung:

```bash
cd amazon_orders
virtualenv venv
```

Unter Linux/macOS:
```bash
source venv/bin/activate
```

Unter Windows: 
```
venv/Scripts/activate.bat
```

3. Installiere notwendige Python-Pakete
```bash
pip install -r requirements.txt
```

4. Crawler starten
```bash
scrapy crawl my_orders -s AMAZON_LOGIN_EMAIL=<my_email> -s AMAZON_LOGIN_PASSWORD=<my_password>
```
Ersetze dabei <my_email> durch die E-Mail-Adresse und <my_password> durch dass Passwort des Amazon-Kontos.
