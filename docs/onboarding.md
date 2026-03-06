# Guide d'onboarding — Analytics Template Project

Bienvenue dans l'équipe ! Ce guide vous accompagne pas à pas pour configurer votre environnement de développement et comprendre le fonctionnement du projet.

---

## Table des matières

1. [Vue d'ensemble du projet](#vue-densemble-du-projet)
2. [Étape 1 — Prérequis](#étape-1--prérequis)
3. [Étape 2 — Récupérer le projet](#étape-2--récupérer-le-projet)
4. [Étape 3 — Configurer l'environnement](#étape-3--configurer-lenvironnement)
5. [Étape 4 — Vérifier l'installation](#étape-4--vérifier-linstallation)
6. [Étape 5 — Lancer un premier script](#étape-5--lancer-un-premier-script)
7. [Étape 6 — Comprendre la structure](#étape-6--comprendre-la-structure)
8. [Étape 7 — Contribuer au projet](#étape-7--contribuer-au-projet)
9. [Ressources et liens utiles](#ressources-et-liens-utiles)

---

## Vue d'ensemble du projet

Ce template est conçu pour démarrer rapidement un projet d'analyse de données en Python. Il impose des conventions claires sur :

- **l'organisation des fichiers** (`scripts/` vs `src/`)
- **la gestion des dépendances** (via `uv`)
- **la qualité du code** (via `ruff`)
- **la reproductibilité** (via `uv.lock` et `Dockerfile`)

L'objectif est que n'importe quel membre de l'équipe puisse cloner le dépôt et être opérationnel en moins de 5 minutes.

---

## Étape 1 — Prérequis

Assurez-vous d'avoir installé les outils suivants avant de commencer :

### Git

```bash
# Vérifier
git --version
```

Si git n'est pas installé : [https://git-scm.com/downloads](https://git-scm.com/downloads)

### uv (gestionnaire Python)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Via pip (si Python est déjà installé)
pip install uv

# Vérifier
uv --version
```

> **Pourquoi uv ?** `uv` est un gestionnaire de paquets Python 10 à 100× plus rapide que `pip`. Il gère à la fois l'installation de Python, la création de l'environnement virtuel et la résolution des dépendances. Tout est capturé dans `uv.lock` pour garantir la reproductibilité.

### Docker (optionnel)

Utile pour exécuter le projet sans polluer votre machine locale. Voir [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/).

---

## Étape 2 — Récupérer le projet

```bash
# Cloner le dépôt
git clone https://github.com/<votre-org>/analytics-template-project.git

# Se placer dans le répertoire
cd analytics-template-project
```

---

## Étape 3 — Configurer l'environnement

### Installer les dépendances et créer le `.venv`

```bash
uv sync
```

Cette commande fait tout en une seule fois :
1. Télécharge la version de Python spécifiée dans `.python-version` si nécessaire
2. Crée le répertoire `.venv/` avec l'environnement virtuel
3. Installe toutes les dépendances épinglées dans `uv.lock`
4. Installe le projet lui-même (package `src`) en mode éditable

### Activer l'environnement virtuel

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (cmd)
.venv\Scripts\activate.bat

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Votre invite de commande affiche désormais `(gozem-analytics-template)` — vous êtes dans le bon environnement.

> **Astuce :** si vous préférez ne pas activer l'environnement, préfixez chaque commande par `uv run` :
> ```bash
> uv run python scripts/main.py
> ```

---

## Étape 4 — Vérifier l'installation

```bash
# Vérifier que ruff est disponible
ruff --version

# Vérifier que Python pointe vers le bon interpréteur
python --version   # doit afficher Python 3.12.x
which python       # doit pointer vers .venv/bin/python
```

---

## Étape 5 — Lancer un premier script

```bash
# Script de bienvenue
python scripts/main.py

# Exemple complet : analyse statistique
python scripts/example_analysis.py

# Exemple complet : pipeline ETL
python scripts/example_pipeline.py
```

Si les trois scripts s'exécutent sans erreur, votre environnement est prêt ! ✅

---

## Étape 6 — Comprendre la structure

```
analytics-template-project/
│
├── scripts/              Vos scripts d'analyse (un fichier = un job)
│   ├── main.py           Point d'entrée minimal
│   ├── example_analysis.py
│   └── example_pipeline.py
│
├── src/                  Code Python réutilisable (importable dans les scripts)
│   └── utils/
│       ├── __init__.py
│       └── helpers.py    log_step, @timer, format_number, load_config
│
├── docs/                 Documentation pour les développeurs
│   ├── onboarding.md     ← vous êtes ici
│   ├── bonnes_pratiques.md
│   └── architecture.md
│
├── pyproject.toml        Dépendances + configuration ruff
├── uv.lock               Dépendances épinglées (à commiter)
├── .python-version       Version Python imposée (3.12.9)
└── Dockerfile            Image Docker pour la reproductibilité
```

### Règle d'or

- **`scripts/`** → code qui s'exécute directement (`python scripts/mon_script.py`)
- **`src/`** → code qui est importé par d'autres modules (`from src.utils import log_step`)

---

## Étape 7 — Contribuer au projet

### Créer une branche

```bash
git checkout -b feature/mon-analyse
```

Nommez vos branches selon la convention : `feature/`, `fix/`, `docs/`, `chore/`.

### Écrire votre code

1. Créez votre script dans `scripts/mon_analyse.py`
2. Ajoutez vos helpers réutilisables dans `src/utils/` ou un nouveau sous-module `src/mon_domaine/`

### Vérifier la qualité avant de commiter

```bash
ruff format .       # Formater le code
ruff check --fix .  # Corriger les problèmes de lint automatiquement
ruff check .        # Vérifier qu'il ne reste aucun problème
```

### Commiter et pousser

```bash
git add .
git commit -m "feat: ajouter l'analyse des ventes"
git push origin feature/mon-analyse
```

### Convention de messages de commit

Suivez la convention [Conventional Commits](https://www.conventionalcommits.org/) :

| Préfixe | Usage |
|---|---|
| `feat:` | Nouvelle fonctionnalité |
| `fix:` | Correction de bug |
| `docs:` | Modification de documentation uniquement |
| `style:` | Formatage, pas de changement de logique |
| `refactor:` | Refactoring sans ajout de fonctionnalité ni correction de bug |
| `chore:` | Tâches de maintenance (dépendances, CI, etc.) |

### Ouvrir une Pull Request

Rendez-vous sur GitHub, poussez votre branche et ouvrez une Pull Request vers `main`. Décrivez :
- Ce que fait votre changement
- Comment le tester
- Les éventuelles dépendances ajoutées

---

## Ressources et liens utiles

| Ressource | Lien |
|---|---|
| Documentation uv | [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/) |
| Documentation ruff | [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/) |
| Conventional Commits | [https://www.conventionalcommits.org/](https://www.conventionalcommits.org/) |
| Bonnes pratiques | [`docs/bonnes_pratiques.md`](bonnes_pratiques.md) |
| Architecture | [`docs/architecture.md`](architecture.md) |
