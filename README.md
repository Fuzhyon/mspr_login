# mspr_login
MSPR d'architecture web avec fonctionnalités d'inscription et login avancées.

### Pré-requis

Il est nécessaire de configurer un interpréteur Python valide (> 2.7).

Pour ce faire, vous aurez besoin :

- Python installé et accessible depuis la ligne de commande `py` (Windows) ou `python` (macOS/Linux)
- Pip, gestionnaire de paquet Python aussi accessible via la command `pip`

A la racine du projet, exécuter la commande : 

```bash
# Windows
> py -3 -m venv venv

# macOS/Linux
$ python3 -m venv venv
```
### Installation
Les dépendances du projet sont spécifié à l'aide d'un fichier (`./requirements.txt`)

Pour les installer, il vous suffit d'éxecuter la commande pip suivante : 

```shell
$ pip install -r requirements.txt
```

Si vous souhaitez ajouter des dépendances au projet, des exemples sont présent dans le fichier `./requirements.txt` pour vous aider à les écrires


### Utilisation

Pour faire fonctionner l'application, vous aurez besoin d'un conteneur docker :

```shell
$ docker run -p 389:389 -p 636:636 --name ldap-mspr --detach osixia/openldap:1.2.4
```

Ensuite lancer le projet :

```bash
# cmd
> start ./venv/Scripts/python.exe app.py

# bash
$ ./venv/bin/python app.py
```