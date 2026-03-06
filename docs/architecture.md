# Architecture du projet

Ce document décrit les décisions d'architecture et la structure technique du template.

---

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Structure des répertoires](#structure-des-répertoires)
3. [Gestionnaire de paquets : uv](#gestionnaire-de-paquets--uv)
4. [Build backend : hatchling](#build-backend--hatchling)
5. [Qualité du code : ruff](#qualité-du-code--ruff)
6. [Conteneurisation : Docker](#conteneurisation--docker)
7. [Flux de données typique](#flux-de-données-typique)
8. [Extension du template](#extension-du-template)
9. [Décisions techniques](#décisions-techniques)

---

## Vue d'ensemble

```
┌──────────────────────────────────────────────────────────────────┐
│                    Analytics Template Project                     │
│                                                                  │
│   ┌────────────────┐          ┌──────────────────────────────┐   │
│   │   scripts/     │ importe  │           src/               │   │
│   │                │ ───────▶ │                              │   │
│   │  main.py       │          │  utils/                      │   │
│   │  example_*.py  │          │    helpers.py                │   │
│   │  mon_script.py │          │    (log_step, timer, ...)    │   │
│   └────────────────┘          │                              │   │
│                               │  data/      (à ajouter)      │   │
│                               │  models/    (à ajouter)      │   │
│                               └──────────────────────────────┘   │
│                                                                  │
│   ┌────────────────┐   ┌──────────────┐   ┌──────────────────┐  │
│   │  pyproject.toml│   │   uv.lock    │   │   Dockerfile     │  │
│   │  (config)      │   │   (lock)     │   │   (container)    │  │
│   └────────────────┘   └──────────────┘   └──────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Structure des répertoires

```
analytics-template-project/
│
├── scripts/                    # Scripts d'entrée (exécutables directement)
│   ├── main.py
│   ├── example_analysis.py
│   └── example_pipeline.py
│
├── src/                        # Package Python installé dans le venv
│   ├── __init__.py
│   └── utils/
│       ├── __init__.py         # Ré-exports publics (API publique du package)
│       └── helpers.py          # Implémentations
│
├── docs/                       # Documentation développeur
│   ├── onboarding.md
│   ├── bonnes_pratiques.md
│   └── architecture.md         ← vous êtes ici
│
├── pyproject.toml              # Source de vérité : dépendances + config outils
├── uv.lock                     # Dépendances épinglées (reproductibilité)
├── .python-version             # Version Python (utilisée par uv)
├── .gitignore
└── Dockerfile
```

### Principe de séparation scripts / src

| `scripts/` | `src/` |
|---|---|
| Contient des programmes complets avec un point d'entrée `main()` | Contient des bibliothèques importables |
| Ne devrait pas être importé par d'autres modules | Doit être importable et réutilisable |
| Couplé à un cas d'usage métier | Agnostique du cas d'usage |
| Un fichier = un job | Un module = une responsabilité |

---

## Gestionnaire de paquets : uv

**uv** est utilisé à la place de `pip` + `venv` pour les raisons suivantes :

| Fonctionnalité | pip + venv | uv |
|---|---|---|
| Vitesse d'installation | Lente | 10–100× plus rapide |
| Gestion de Python | Manuelle | Automatique (via `.python-version`) |
| Fichier de lock | Non (sauf pip-tools) | Oui (`uv.lock`) |
| Reproductibilité | Approximative | Garantie |
| Commande tout-en-un | Non | `uv sync` |

### Fichiers clés

- **`pyproject.toml`** : déclare les dépendances et leurs contraintes de version
- **`uv.lock`** : contient les versions exactes résolues (à commiter absolument)
- **`.python-version`** : pin la version Python (lu automatiquement par uv)

---

## Build backend : hatchling

Le projet utilise **hatchling** comme build backend (défini dans `pyproject.toml`). Cela permet à `uv sync` d'installer le package `src/` dans le venv en mode éditable.

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src"]
```

**Effet concret :** après `uv sync`, n'importe quel script peut faire :

```python
from src.utils import log_step, timer   # ✅ fonctionne sans PYTHONPATH
```

---

## Qualité du code : ruff

**ruff** remplace plusieurs outils en un seul binaire ultra-rapide :

| Outil remplacé | Fonctionnalité |
|---|---|
| `black` | Formatage du code |
| `isort` | Tri des imports |
| `flake8` | Détection des erreurs de style |
| `pyupgrade` | Modernisation de la syntaxe Python |
| `flake8-bugbear` | Détection de bugs courants |

### Configuration (`pyproject.toml`)

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP"]
ignore = ["E501"]   # Géré par le formateur

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "auto"
```

---

## Conteneurisation : Docker

Le `Dockerfile` utilise une image `python:3.12.9-slim` pour minimiser la taille de l'image tout en garantissant la reproductibilité.

### Stratégie de build en deux étapes

```
Stage 1 : builder
  → Installe uv
  → Copie pyproject.toml + uv.lock
  → uv sync --frozen (installe les dépendances dans /app/.venv)

Stage 2 : image finale
  → Copie .venv depuis le builder
  → Copie le code source
  → Lance le script via Python du venv
```

### Avantages

- **Image légère** : `python:3.12.9-slim` sans outils de build inutiles
- **Couches Docker mises en cache** : les dépendances sont réinstallées seulement si `uv.lock` change
- **Reproductibilité** : mêmes dépendances que le développement local (via `uv.lock`)

---

## Flux de données typique

```
Source de données               Pipeline Python                  Destination
(CSV, API, DB, etc.)                                          (DB, fichiers, etc.)

     │                                                               │
     ▼                                                               ▼
┌──────────┐    ┌──────────┐    ┌───────────┐    ┌───────────┐    ┌──────────┐
│ Extract  │───▶│ Validate │───▶│ Transform │───▶│   Load    │───▶│  Sortie  │
│          │    │          │    │           │    │           │    │          │
│ load_*() │    │ check_*()│    │ compute_* │    │ export_*()│    │          │
└──────────┘    └──────────┘    └───────────┘    └───────────┘    └──────────┘
     │               │                │                │
     └───────────────┴────────────────┴────────────────┘
                              │
                     Chaque étape est une
                    fonction décorée @timer
                    dans scripts/<job>.py
```

---

## Extension du template

### Ajouter un nouveau domaine métier

```bash
mkdir -p src/mon_domaine
touch src/mon_domaine/__init__.py
touch src/mon_domaine/loaders.py
touch src/mon_domaine/transformers.py
```

### Ajouter des tests

```bash
mkdir -p tests
touch tests/__init__.py
touch tests/test_helpers.py

# Ajouter pytest comme dépendance de dev
uv add --dev pytest
```

### Ajouter un CI/CD

Exemple de workflow GitHub Actions (`.github/workflows/ci.yml`) :

```yaml
name: CI
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync
      - run: ruff format --check .
      - run: ruff check .
```

---

## Décisions techniques

### Pourquoi uv et pas poetry / conda ?

- **uv** : rapide, simple, standard (PEP 517/518), excellent support des workspaces
- **poetry** : plus lent, gestion des versions parfois complexe
- **conda** : adapté au calcul scientifique mais lourd pour les projets Python purs

### Pourquoi ruff et pas black + flake8 ?

- Une seule commande pour tout
- 10–100× plus rapide que l'équivalent black + isort + flake8
- Configuration centralisée dans `pyproject.toml`

### Pourquoi hatchling ?

- Backend léger, standard, sans configuration superflue
- Recommandé par la PyPA pour les projets simples
- Compatible avec uv nativement

### Pourquoi `python:3.12.9-slim` dans Docker ?

- `slim` : image Debian minimale — réduit la surface d'attaque et la taille de l'image (~150 Mo vs ~900 Mo pour l'image complète)
- `3.12.9` : correspond exactement à `.python-version` — cohérence garantie entre local et container
