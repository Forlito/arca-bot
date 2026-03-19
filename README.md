# arca-bot

Bot de Telegram para consultar marcas registradas en el INPI Argentina sin tener que pelear con el portal.

## Qué hace

- Busca marcas por nombre en la base pública del INPI
- Verifica si un nombre de marca podría estar disponible
- Muestra info sobre las 45 clases Niza
- No requiere clave fiscal para las consultas

## Comandos

| Comando | Qué hace |
|---|---|
| `/buscar <nombre> [clase]` | Busca marcas vigentes que contengan el nombre |
| `/disponible <nombre> [clase]` | Verifica disponibilidad (con disclaimer legal) |
| `/buscar_todas <nombre>` | Busca incluyendo marcas no vigentes |
| `/clase <numero>` | Info sobre una clase Niza |
| `/clases <palabra>` | Busca clases por actividad |
| `/ayuda` | Más info y ejemplos |

## Setup

1. Creá un bot con [@BotFather](https://t.me/BotFather) en Telegram
2. Copiá `.env.example` a `.env` y poné tu token
3. Instalá dependencias:

```bash
pip install -r requirements.txt
```

4. Corré el bot:

```bash
python -m bot.main
```

## Deploy con Docker

```bash
docker build -t arca-bot .
docker run --env-file .env arca-bot
```

## Deploy en Railway

1. Forkeá el repo
2. Conectalo a Railway
3. Agregá la variable `TELEGRAM_BOT_TOKEN` en el dashboard
4. Railway detecta el Dockerfile automáticamente

## Cómo funciona

El bot hace POST al buscador público del INPI (`portaltramites.inpi.gob.ar/MarcasConsultas/Grilla`) y parsea el HTML de los resultados. No usa APIs privadas ni requiere autenticación para las consultas.

## Disclaimer

La búsqueda es por texto, no fonética. Que un nombre no aparezca NO garantiza que esté disponible para registro. El INPI puede denegar marcas por similitud fonética. Para una búsqueda formal, consultá con un agente de propiedad industrial.

## Licencia

MIT
