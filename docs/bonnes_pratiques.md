# Bonnes pratiques de développement

Ce document rassemble les conventions et bonnes pratiques à respecter sur ce projet. L'objectif est de produire un code lisible, maintenable et reproductible.

---

## Table des matières

1. [Organisation du code](#organisation-du-code)
2. [Conventions de nommage](#conventions-de-nommage)
3. [Style et formatage](#style-et-formatage)
4. [Gestion des dépendances](#gestion-des-dépendances)
5. [Logging](#logging)
6. [Gestion des erreurs](#gestion-des-erreurs)
7. [Documentation du code](#documentation-du-code)
8. [Git et branches](#git-et-branches)
9. [Reproductibilité](#reproductibilité)
10. [Sécurité](#sécurité)

---

## Organisation du code

### Règle fondamentale : un script = un job

Chaque fichier dans `scripts/` doit correspondre à une tâche clairement définie et exécutable de façon autonome.

```
✅ scripts/export_rapport_mensuel.py   ← une tâche, un fichier
✅ scripts/calcul_kpi_ventes.py        ← une tâche, un fichier

❌ scripts/tout_faire.py               ← trop vague, trop large
```

### Séparer la logique métier des scripts

Toute fonction réutilisable dans plusieurs scripts **doit** être déplacée dans `src/` :

```
✅ src/utils/helpers.py       ← helpers génériques
✅ src/data/loaders.py        ← fonctions de chargement de données
✅ src/models/features.py     ← feature engineering

❌ scripts/mon_script.py contenant 500 lignes de helpers
```

### Structure d'un script

Tout script doit suivre ce patron :

```python
"""Description courte du script."""

# 1. Imports stdlib
import logging

# 2. Imports tiers
import pandas as pd

# 3. Imports internes
from src.utils import log_step, timer

# 4. Constantes au niveau module (si nécessaire)
OUTPUT_DIR = "data/output"


# 5. Fonctions métier (chaque étape = une fonction)
@timer
def load_data() -> pd.DataFrame:
    ...


@timer
def transform(df: pd.DataFrame) -> pd.DataFrame:
    ...


# 6. Fonction main()
def main() -> None:
    df = load_data()
    df = transform(df)
    ...


# 7. Guard
if __name__ == "__main__":
    main()
```

---

## Conventions de nommage

Suivre [PEP 8](https://peps.python.org/pep-0008/) :

| Élément | Convention | Exemple |
|---|---|---|
| Variables / fonctions | `snake_case` | `load_data`, `row_count` |
| Classes | `PascalCase` | `DataPipeline`, `SalesReport` |
| Constantes | `UPPER_SNAKE_CASE` | `MAX_RETRIES`, `OUTPUT_DIR` |
| Modules / fichiers | `snake_case` | `data_loader.py`, `helpers.py` |
| Packages | `snake_case` court | `utils`, `data`, `models` |

### Nommage des scripts

Préférez des noms descriptifs et stables :

```
✅ export_ventes_mensuelles.py
✅ calcul_taux_retention.py
✅ pipeline_feature_engineering.py

❌ script1.py
❌ test.py
❌ temp_analyse.py
```

---

## Style et formatage

### Utiliser ruff — toujours

Avant chaque commit, exécuter :

```bash
ruff format .       # Formatage automatique
ruff check --fix .  # Corrections de lint automatiques
ruff check .        # Vérification finale
```

### Longueur des lignes

Maximum **100 caractères** (configuré dans `pyproject.toml`). Les lignes trop longues nuisent à la lisibilité, surtout lors des revues de code.

### Imports

Respecter l'ordre imposé par isort (géré par ruff) :

```python
# 1. Bibliothèque standard
import json
import os
from pathlib import Path

# 2. Bibliothèques tierces
import pandas as pd
import numpy as np

# 3. Imports internes au projet
from src.utils import log_step, timer
```

### Type hints

Annoter systématiquement les signatures de fonctions :

```python
# ✅ Bien
def compute_mean(values: list[float]) -> float:
    return sum(values) / len(values)

# ❌ À éviter
def compute_mean(values):
    return sum(values) / len(values)
```

---

## Gestion des dépendances

### Toujours utiliser uv

```bash
uv add pandas          # Dépendance de production
uv add --dev pytest    # Dépendance de développement uniquement
uv remove pandas       # Supprimer une dépendance
```

### Commiter uv.lock

Le fichier `uv.lock` **doit être commité** dans git. Il garantit que tous les membres de l'équipe et les environnements CI travaillent avec exactement les mêmes versions de paquets.

```bash
# ✅ Commiter les deux
git add pyproject.toml uv.lock
git commit -m "chore: ajouter pandas"
```

### Ne jamais modifier pyproject.toml manuellement pour les dépendances

Utilisez toujours `uv add` / `uv remove` pour éviter les incohérences avec `uv.lock`.

---

## Logging

### Utiliser le helper `log_step`

Pour les messages d'étape dans un pipeline :

```python
from src.utils import log_step

log_step("Chargement des données …")   # ✅
print("Chargement des données …")      # ❌ éviter print() dans les pipelines
```

### Niveaux de log

| Niveau | Quand l'utiliser |
|---|---|
| `DEBUG` | Informations détaillées, utiles uniquement en développement |
| `INFO` | Étapes normales du pipeline, état courant |
| `WARNING` | Situation anormale mais non bloquante (données manquantes, fallback, etc.) |
| `ERROR` | Erreur bloquante nécessitant une attention immédiate |
| `CRITICAL` | Erreur système grave |

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Valeur intermédiaire : %s", value)
logger.info("Traitement de %d lignes", row_count)
logger.warning("Colonne 'age' absente — valeur par défaut utilisée")
logger.error("Impossible de se connecter à la base de données : %s", err)
```

### Ne pas logger d'informations sensibles

```python
# ❌ Danger
logger.info("Connexion avec le mot de passe : %s", password)

# ✅ Correct
logger.info("Connexion réussie pour l'utilisateur : %s", username)
```

---

## Gestion des erreurs

### Être explicite sur les exceptions

```python
# ✅ Spécifier le type d'exception
try:
    data = load_config("config.json")
except FileNotFoundError as err:
    logger.error("Fichier de configuration introuvable : %s", err)
    raise

# ❌ Attraper toutes les exceptions sans raison
try:
    data = load_config("config.json")
except Exception:
    pass  # Silencieusement ignorer toutes les erreurs
```

### Fail fast

Vérifiez les préconditions en début de fonction plutôt qu'à mi-chemin :

```python
def process(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        raise ValueError("Le DataFrame d'entrée est vide.")
    # ... logique métier
```

---

## Documentation du code

### Docstrings

Toutes les fonctions publiques doivent avoir une docstring :

```python
def format_number(value: float, decimals: int = 2) -> str:
    """Retourne une chaîne lisible pour *value* avec séparateurs de milliers.

    Parameters
    ----------
    value:
        La valeur numérique à formater.
    decimals:
        Nombre de décimales (défaut : 2).

    Returns
    -------
    str
        Chaîne formatée, ex : ``'1,234,567.89'``.

    Examples
    --------
    >>> format_number(1234567.891)
    '1,234,567.89'
    """
    return f"{value:,.{decimals}f}"
```

### Commentaires inline

Réservez les commentaires aux parties non évidentes. Un bon code se lit sans commentaires :

```python
# ✅ Commentaire utile : explique le POURQUOI
# µ ± 3σ couvre 99.7% d'une distribution normale
lower, upper = mean - 3 * std, mean + 3 * std

# ❌ Commentaire inutile : répète le QUOI
# Calculer la moyenne
mean = sum(values) / len(values)
```

---

## Git et branches

### Nommer les branches

```
feature/<description>     Nouvelle fonctionnalité
fix/<description>         Correction de bug
docs/<description>        Documentation
chore/<description>       Maintenance (deps, CI, config)
refactor/<description>    Refactoring
```

### Convention de messages de commit

Format : `<type>(<scope optionnel>): <description courte>`

```bash
git commit -m "feat: ajouter le calcul du taux de churn"
git commit -m "fix(pipeline): corriger la gestion des valeurs nulles"
git commit -m "docs: mettre à jour le guide d'onboarding"
git commit -m "chore: mettre à jour ruff vers 0.16"
git commit -m "style: ruff format & check"
```

### Ne jamais commiter directement sur `main`

Toujours travailler sur une branche et passer par une Pull Request.

### Taille des commits

Faites des commits petits et focalisés. Un commit = un changement logique.

---

## Reproductibilité

### Graines aléatoires

Toujours fixer la graine quand vous utilisez des fonctions aléatoires pour garantir des résultats reproductibles :

```python
import random
random.seed(42)

import numpy as np
np.random.seed(42)
```

### Pas de chemins absolus en dur

```python
# ❌ Non reproductible sur une autre machine
path = "/home/abraham/data/ventes.csv"

# ✅ Chemin relatif depuis la racine du projet
from pathlib import Path
path = Path("data") / "ventes.csv"
```

### Variables d'environnement pour les secrets

Ne jamais stocker des clés d'API, mots de passe ou tokens dans le code source :

```python
import os

# ✅ Correct
api_key = os.environ["API_KEY"]

# ❌ Danger
api_key = "sk-1234567890abcdef"
```

---

## Sécurité

- Ne jamais commiter de secrets (clés API, mots de passe, tokens)
- Vérifier le `.gitignore` avant de commiter (il exclut déjà `.venv/`)
- Utiliser des variables d'environnement ou un fichier `.env` (non commité) pour les configurations sensibles
- Maintenir les dépendances à jour (`uv add <paquet>@latest`)
