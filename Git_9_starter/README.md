# Git töötuba

Kuupäev: 10.11.2026

Ava index.html oma brauseris. Veebimajutust ei ole vaja.
Registreerimislink on väljamõeldud näidis, mitte päris teenus.

## Kvaliteedinõuded

- Lehel peab olema ürituse nimi ja kehtiv kuupäev.
- Registreerimislink peab kasutama HTTPS-i ja sisaldama serveri nime.
- Lehe kuupäev ja README kuupäev peavad kattuma.
- Kontrolli enne ühendamist nii automaatkontrolli kui ka kaaslase tagasisidet.

## Automaatkontroll

GitHub Actions käivitab kontrolli main-haru push'i ja main-harusse suunatud
pull request'i korral. Kohalik kontroll (Python 3):

    python check_site.py

Kontroll analüüsib HTML-faili. See ei ava registreerimislinki ega võrdle README
kuupäeva lehega. Need piirangud tuleb arvestada koodi ülevaatamisel.
