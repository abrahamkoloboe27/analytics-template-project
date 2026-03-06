# Analytics Template Project 🇫🇷

> Un template Python prêt à l'emploi pour les projets d'analyse de données, propulsé par **[uv](https://docs.astral.sh/uv/)** et **[ruff](https://docs.astral.sh/ruff/)**.

---

## Table des matières

1. [Structure du projet](#structure-du-projet)
2. [Prérequis](#prérequis)
3. [Démarrage rapide](#démarrage-rapide)
   - [1 · Cloner le dépôt](#1--cloner-le-dépôt)
   - [2 · Installer uv](#2--installer-uv)
   - [3 · Installer les dépendances](#3--installer-les-dépendances)
   - [4 · Activer l'environnement virtuel](#4--activer-lenvironnement-virtuel)
4. [Lancer les scripts](#lancer-les-scripts)
5. [Qualité du code avec Ruff](#qualité-du-code-avec-ruff)
   - [Formatage](#formatage)
   - [Lint / Vérification](#lint--vérification)
   - [Checklist avant de pousser](#checklist-avant-de-pousser)
6. [Workflow de développement](#workflow-de-développement)
7. [Ajouter de nouveaux scripts et utilitaires](#ajouter-de-nouveaux-scripts-et-utilitaires)
8. [Docker](#docker)
9. [Documentation complémentaire](#documentation-complémentaire)

---

## Structure du projet

```
analytics-template-project/
├── pyproject.toml              # Métadonnées, dépendances, config ruff
├── uv.lock                     # Graphe de dépendances verrouillé (commité)
├── .python-version             # Version Python imposée par uv
├── .gitignore
├── Dockerfile                  # Image Docker python:3.12.9-slim
│
├── scripts/                    # ← Scripts d'entrée (un fichier = un job)
│   ├── main.py                 #   Point d'entrée minimaliste
│   ├── example_analysis.py     #   Exemple : pipeline de statistiques descriptives
│   └── example_pipeline.py     #   Exemple : pipeline ETL multi-étapes
│
├── src/                        # ← Packages Python réutilisables
│   └── utils/
│       ├── __init__.py         #   Ré-exports publics
│       └── helpers.py          #   Helpers : logging, timing, formatage, config
│
└── docs/                       # ← Documentation complémentaire
    ├── onboarding.md           #   Guide de prise en main pour les nouveaux
    ├── bonnes_pratiques.md     #   Bonnes pratiques de développement
    └── architecture.md         #   Vue d'ensemble de l'architecture
```

**Convention :**

| Répertoire | Contenu |
|---|---|
| `scripts/` | Scripts exécutables avec une fonction `main()` et un guard `if __name__ == "__main__"` |
| `src/utils/` | Helpers réutilisables importés par plusieurs scripts |
| `src/<domaine>/` | Modules métier (ex : `src/models/`, `src/data/`) — à ajouter selon les besoins |
| `docs/` | Documentation pour les développeurs (onboarding, architecture, bonnes pratiques) |

---

## Prérequis

| Outil | Version minimale | Notes |
|---|---|---|
| **Python** | 3.12 | Géré automatiquement par uv |
| **uv** | 0.4+ | Gestionnaire de paquets et de projets Python ultra-rapide |
| **git** | toute version | |
| **Docker** | toute version | Optionnel — pour exécuter le projet en conteneur |

---

## Démarrage rapide

### 1 · Cloner le dépôt

```bash
git clone https://github.com/<votre-org>/analytics-template-project.git
cd analytics-template-project
```

### 2 · Installer uv

```bash
# macOS / Linux (recommandé)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Ou via pip (fonctionne partout où Python est déjà installé)
pip install uv
```

Vérifier l'installation :

```bash
uv --version
```

### 3 · Installer les dépendances

`uv sync` lit `pyproject.toml` et `uv.lock` puis crée un `.venv` local avec toutes les dépendances épinglées :

```bash
uv sync
```

> **Astuce :** `uv sync` installe également la bonne version de Python automatiquement si elle n'est pas présente sur votre machine, grâce au fichier `.python-version`.

### 4 · Activer l'environnement virtuel

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (cmd)
.venv\Scripts\activate.bat

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Votre invite de commande affichera `(gozem-analytics-template)` (ou similaire), confirmant que l'environnement est actif.

> **Astuce :** vous pouvez aussi lancer n'importe quelle commande *sans* activer l'environnement en la préfixant par `uv run` :
> ```bash
> uv run python scripts/example_analysis.py
> ```

---

## Lancer les scripts

Tous les scripts se trouvent dans `scripts/` et doivent être lancés **depuis la racine du projet** pour que le package `src` soit importable :

```bash
# Point d'entrée minimaliste
python scripts/main.py

# Exemple : statistiques descriptives sur des données simulées
python scripts/example_analysis.py

# Exemple : pipeline ETL multi-étapes
python scripts/example_pipeline.py
```

Exemple de sortie pour `example_analysis.py` :

```
2026-01-01 12:00:00 [INFO] ▶ Chargement de 2000 lignes de données …
2026-01-01 12:00:00 [INFO] ✓ load_data terminé en 0.01s
2026-01-01 12:00:00 [INFO] ▶ Nettoyage des données …
2026-01-01 12:00:00 [INFO] ▶ 4 valeur(s) aberrante(s) supprimée(s). 1996 lignes restantes.
2026-01-01 12:00:00 [INFO] ✓ clean_data terminé en 0.00s
...
========================================
  Rapport d'analyse
========================================
  Count   : 1 996
  Mean    : 100,12
  Std Dev :  14,87
  Median  : 100,34
========================================
```

---

## Qualité du code avec Ruff

[**Ruff**](https://docs.astral.sh/ruff/) est un linter et formateur Python extrêmement rapide (écrit en Rust). Il remplace `flake8`, `isort`, `pyupgrade` et `black` en un seul outil.

La configuration ruff du projet se trouve dans `pyproject.toml` sous `[tool.ruff]`.

### Formatage

Formater automatiquement tous les fichiers Python :

```bash
ruff format .
```

Vérifier ce qui *serait* modifié sans écrire les fichiers :

```bash
ruff format --check .
```

### Lint / Vérification

Exécuter toutes les règles de lint configurées et signaler les problèmes :

```bash
ruff check .
```

Corriger automatiquement les problèmes sûrs (imports, variables non utilisées, etc.) :

```bash
ruff check --fix .
```

### Checklist avant de pousser

Exécuter ces commandes avant chaque `git push` pour garder le code propre :

```bash
ruff format .       # 1. Formatage automatique
ruff check --fix .  # 2. Corrections automatiques de lint
ruff check .        # 3. Confirmer qu'il ne reste aucun problème
git add -u
git commit -m "style: ruff format & check"
git push
```

> **Automatisation :** ajoutez un hook [pre-commit](https://pre-commit.com/) ou une étape CI qui exécute `ruff format --check . && ruff check .` pour appliquer la qualité sur chaque pull request.

---

## Workflow de développement

```
┌─────────────────────────────────────────────────────────────────┐
│  git clone → cd projet → uv sync → source .venv/bin/activate   │
│                                                                  │
│  ┌──────────────┐     ┌─────────────┐     ┌──────────────────┐ │
│  │  Écrire le   │ ──▶ │  Lancer le  │ ──▶ │  ruff format .   │ │
│  │  code dans   │     │  script     │     │  ruff check .    │ │
│  │  scripts/    │     │  python     │     │                  │ │
│  │  ou src/     │     │  scripts/…  │     │                  │ │
│  └──────────────┘     └─────────────┘     └───────┬──────────┘ │
│                                                    │            │
│                                               git push          │
└────────────────────────────────────────────────────────────────-┘
```

1. **Créer une branche** – `git checkout -b feature/mon-analyse`
2. **Écrire / modifier le code** dans `scripts/` (nouveau job) ou `src/` (utilitaire réutilisable)
3. **Lancer le script** – `python scripts/mon_analyse.py`
4. **Formater et lint** – `ruff format . && ruff check --fix .`
5. **Commiter** – `git add . && git commit -m "feat: ajouter le script mon-analyse"`
6. **Pousser** – `git push origin feature/mon-analyse`
7. **Ouvrir une Pull Request**

---

## Ajouter de nouveaux scripts et utilitaires

### Nouveau script

```bash
touch scripts/mon_nouveau_script.py
```

Template minimal :

```python
"""Description en une ligne de ce que fait ce script."""

from src.utils import log_step, timer


@timer
def run() -> None:
    log_step("Démarrage …")
    # votre logique ici


if __name__ == "__main__":
    run()
```

### Nouveau module utilitaire

```bash
# Exemple : ajouter un module de chargement de données
touch src/data/__init__.py
touch src/data/loaders.py
```

Import dans n'importe quel script :

```python
from src.data.loaders import load_csv
```

### Ajouter une nouvelle dépendance

```bash
uv add <nom-du-paquet>          # ajoute dans pyproject.toml + met à jour uv.lock
uv add --dev <nom-du-paquet>    # dépendance de développement uniquement
```

Commitez toujours `pyproject.toml` **et** `uv.lock` ensemble pour que tous les membres de l'équipe aient exactement le même environnement.

---

## Docker

Le projet inclut un `Dockerfile` basé sur `python:3.12.9-slim` pour exécuter les scripts dans un environnement containerisé reproductible.

### Construire l'image

```bash
docker build -t analytics-template .
```

### Lancer un script dans le conteneur

```bash
# Script d'exemple — analyse
docker run --rm analytics-template python scripts/example_analysis.py

# Script d'exemple — pipeline
docker run --rm analytics-template python scripts/example_pipeline.py

# Shell interactif dans le conteneur
docker run --rm -it analytics-template bash
```

### Monter des données locales

```bash
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  analytics-template \
  python scripts/mon_script.py
```

---

## Documentation complémentaire

| Document | Description |
|---|---|
| [`docs/onboarding.md`](docs/onboarding.md) | Guide de prise en main pour les nouveaux membres de l'équipe |
| [`docs/bonnes_pratiques.md`](docs/bonnes_pratiques.md) | Bonnes pratiques de développement et conventions de code |
| [`docs/architecture.md`](docs/architecture.md) | Vue d'ensemble de l'architecture et des décisions techniques |
