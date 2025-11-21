# EcoTrack API & Dashboard

Projet FastAPI complet répondant au cahier des charges « Projet API ». L’application expose :

- Une API REST sécurisée (FastAPI + SQLAlchemy + JWT) pour suivre des indicateurs environnementaux (qualité de l’air, CO₂, énergie, déchets) par zone géographique.
- Un nouveau front-end moderne (React + Vite + Tailwind) avec plusieurs vues (dashboard, statistiques, gestion des entités, administration).

## Fonctionnalités clés

- Authentification JWT avec rôles `user` (lecture) et `admin` (gestion complète).
- CRUD complets pour utilisateurs, zones, sources et indicateurs avec filtres, pagination et recherche par période.
- Endpoints statistiques : moyennes de qualité de l’air et tendances agrégées (daily/weekly/monthly).
- Script d’ingestion externe basé sur l’API OpenAQ (avec fallback v3 + clé API).
- Script CLI pour créer un administrateur initial.
- Nouveau front-end « dashboard » (`frontend-app/`) pour piloter l’API : login, filtres avancés, graphiques, CRUD zones/sources/utilisateurs.
- Suite de tests Pytest couvrant les principaux parcours (authentification, indicateurs, statistiques).

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate  # PowerShell
pip install -r requirements.txt
```

Configurer éventuellement un fichier `.env` :

```
DATABASE_URL=sqlite:///./ecotrack.db
SECRET_KEY=une_clé_ultra_secrète
ACCESS_TOKEN_EXPIRE_MINUTES=60
FIRST_SUPERUSER_EMAIL=admin@ecotrack.local
FIRST_SUPERUSER_PASSWORD=ChangeMe123!
```

## Lancement de l’API

```bash
uvicorn app.main:app --reload
```

Endpoints disponibles sous `http://localhost:8000/api/v1`. Documentation interactive via `/docs`.

## Scripts utiles

```powershell
$env:PYTHONPATH="C:\Users\<vous>\EcoTrack"
python scripts/create_admin.py
python scripts/ingest_external_data.py --limit 25 --city "Paris 18"
```

> Remplacez le chemin par celui du dépôt local si nécessaire. Les scripts doivent être exécutés avec `PYTHONPATH` pointant vers la racine du projet pour que les imports `app.*` fonctionnent.

### Ingestion OpenAQ (fallback v3)

Depuis avril 2024, l’endpoint public `v2/latest` retourne `410 Gone`. Le service d’ingestion tente d’abord `v2`, puis bascule automatiquement sur `v3/measurements` (qui requiert une clé personnelle gratuite). Ajoutez-la dans `.env` :

```
OPENAQ_API_KEY=xxxxxxxxxxxxxxxx
```

Une fois la clé définie, relancez en précisant au moins un filtre (`--city`, `--country` ou `--location-id`) basé sur les valeurs retournées par les endpoints `v3/cities` ou `v3/locations` :

```powershell
$env:PYTHONPATH="C:\Users\<vous>\EcoTrack"
python scripts/ingest_external_data.py --limit 25 --country FR
```

Le script crée automatiquement les zones/sources manquantes et insère les mesures OpenAQ. En cas d’échec réseau ou d’un filtre invalide, il détaille l’URL concernée pour faciliter le débogage.

## Tests

```bash
pytest
```

## Front-end moderne (React + Vite)

Le nouveau dashboard vit dans `frontend-app/`. Pré-requis : Node.js 18+ et npm.

```bash
cd frontend-app
npm install
npm run dev
```

L’application expose :

- Connexion JWT avec persistance locale et protection de routes.
- Dashboard avec filtres, KPIs et graphiques (Recharts).
- Pages dédiées aux indicateurs, statistiques, utilisateurs, zones et sources.
- Actions CRUD (ex: création de zones) connectées directement à l’API.

> Ancien front statique (`frontend/`) reste présent pour référence mais n’est plus la voie recommandée.

## Prochaines pistes

- Brancher Alembic pour gérer les migrations.
- Ajouter des rôles intermédiaires (analyste) et une gestion fine des autorisations.
- Mettre en cache les statistiques (Redis) pour accélérer les tableaux de bord.
