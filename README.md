![image](https://user-images.githubusercontent.com/49156499/115967379-9e6fb180-a532-11eb-8142-428a455a6454.png)

# Objectifs  

Dans cette session pratique, nous allons: 
- comprendre le fonctionnement de Kafka et ses différentes terminologies
- déployer et configurer un cluster Kafka
- mettre en oeuvre une application de traitement de données en Python
- ...


# Pré-requis
_A faire avant la session pratique._

## PyCharm
[PyCharm](https://www.jetbrains.com/pycharm/download/) est un IDE permettant de développer des applications en Python.
Nous allons l'utiliser lors de cette session pratique car il intègre plusieurs outils qui facilitent et accélèrent le développement des applications.  
  
La version PyCharm Community est disponible [ici](https://www.jetbrains.com/pycharm/download/).  
Téléchargez et installez la version compatible avec votre machine.
Commande spéciale pour Ubuntu 16.04 ou plus:
```
sudo snap install pycharm-community --classic
```
Note: votre compte étudiant de Dauphine vous donne accès gratuitement à la version Ultimate. Pour cela, il suffit de vous enregistrer avec votre adresse mail de Dauphine et de valider l'inscription.

Je vous invite à prendre en main PyCharm avec ce [tutoriel](https://www.jetbrains.com/help/pycharm/creating-and-running-your-first-python-project.html#create-file).
  

### Docker
Dans cette session, pour des raisons pratiques, nous allons utiliser des [dockers](https://www.docker.com/) ([conteneurs d'applications](https://fr.wikipedia.org/wiki/Docker_\(logiciel\))) pour exécuter nos applications.  
Un docker est un conteneur d'applications permettant d'exécuter une application indépendamment du système d'exploitation et de ses dépendances.  
L'application est packagée d'une façon autonome (avec toutes ses dépendances) pour être exécutée sur n'importe quel système.  
Les liens ci-dessous vous guident dans l'installation de Docker sur votre machine locale:  
[Windows](https://docs.docker.com/docker-for-windows/install/) | [Ubuntu](https://docs.docker.com/engine/install/ubuntu/) | [Mac](https://docs.docker.com/docker-for-mac/install/).  
Veuillez réaliser l'installation avant la session.

### Docker-compose
Les utilisateurs de Linux ont besoin d'installer [docker-compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04). Pour les autres (Mac et Windows), cet utilitaire est déjà inclus dans Docker Desktop (installé plus haut). 

# Lab Session
Le code source de cette partie est disponible dans ce [repository](https://github.com/osekoo/hands-on-kafka).  
Vous pouvez le récupérer en utilisant [git](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git) ou en téléchargeant l'archive https://github.com/osekoo/hands-on-kafka/archive/refs/heads/develop.zip.  
![image](https://user-images.githubusercontent.com/49156499/115967302-3325df80-a532-11eb-825c-58343a02118b.png)

Nous allons étudier deux cas:
- <b>get_started</b>: une application simple d'écriture et de lecture de données. Il permet de comprendre les différents mécanismes de Kafka (producers, consumers, consumer group, etc).
- <b>dico</b>: une application asynchrone de recherche de définition des mots sur internet (dictionnaire).  

## Cluster Kafka
Nous allons utiliser les images bitnami de [Kafka](https://github.com/bitnami/bitnami-docker-kafka) pour exécuter Kafka sur notre machine locale.  

### Les étapes pour lancer le cluster
1. extrayez l'archive dans un répertoire
2. ouvrez le répertoire `hands-on-kafka` avec `PyCharm`
3. si l'interpréteur python n'est pas reconnu, 
    1. sélectionnez un interpréteur qui vous sera proposé 
    2. ou allez dans `File > Settings > Project: hands-on-kafka`
    3. cliquez ensuite sur Add interpreter et Add local interpreter. 
    4. cochez la case New et sélection un Base interpreter
    5. ensuite validez tout en cliquant sur OK
4. installez les dépendances python avec la commande `pip install -r requirements.txt`
5. **exécution du broker kafka**: dans un terminal exécutez la commande `docker-compose up`
    - allez visiter le `dashboard kafka` à l'adresse `http://localhost:9094`. Nous verrons ensemble les informations disponibles sur ce dashboard.  


## Le module `get_started`
Le module `get_started` permet de publier et de lire des messages. Il contient 3 fichiers:
- `config.py`: contient les variables/constantes globales.
- `producer.py`: permet de publier une série de messages dans le bus Kafka. Dans Pycharm.
- `consumer.py`: permet de lire les messages publiés par le consumer.

![image](https://user-images.githubusercontent.com/49156499/115967255-da564700-a531-11eb-9a5d-de7ac64d5e67.png)

### Les étapes à suivre pour exécuter le module get_started:

1. **exécution du producer**: dans un autre terminal exécuter la commande  `python ./get_started/producer.py`
    1. le producer envoie sur le broker une série de nombres de 0 à 99
2. **exécution du consumer**: dans un autre terminal exécuter la commande  `python ./get_started/consumer.py`
    1. le consumer lit les nombres envoyés par le producer et affiche un message sur la console
    2. allez sur le `dashboard`, cliquez sur `my-topic` ensuite sur la `partition 0` pour voir les messages envoyés


## Le module `dico`

![image](https://user-images.githubusercontent.com/49156499/115967493-2f468d00-a533-11eb-86c4-fa82c7ec9f3d.png)

Le module `dico` permet de chercher la définition d'un mot sur Internet. Il supporte le français (lerobert.com) et l'anglais (dictionary.com). Ce module contient 5 fichiers:
- `config.py`: contient les variables globales (noms des topics, noms des dictionnaires, etc.).
- `crawler.py`: permet de chercher la définition des mots sur Internet en français (`CrawlerFR`) et en anglais (`CrawlerEN`). Cette classe extrait la définition des en parsant la source HTML du résultat de recherche. Le parsing peut parfois échoué si la structure HTML de la page change.
- `worker.py`: contient une class (`Worker`) qui permet de lire les requêtes de recherche postées dans le bus Kafka (en mode `consumer`), effectue la recherche en utilisant le crawler (`data processing`) et republie le résultat dans Kafka (en mode `producer`). Il faut cliquer sur la flèche verte à côté de `if __name__ == "__main__":` pour exécuter le worker. Vous devez spécifier la langue de recherche (`fr` pour français ou `en` pour anglais) à l'invite commande.
- `client.py`: publie dans Kafka la requête de recherche de définition (en mode `producer`) et lit au retour la réponse (en mode `consumer`). Il faut cliquer sur la flèche verte à côté de `if __name__ == "__main__":` pour exécuter le client. Vous devez spécifier votre pseudonyme (utilisé pour créer le topic qui servira à lire les réponses) et la langue de recherche (`fr` pour français ou `en` pour anglais).
- `kafka_data.py`: implémente les structures de données (`KafkaRequest`, `KafkaResponse`) échanger entre les clients et les workers à travers Kafka.

### Mise en œuvre du module dico:
1. cluster kafka: dans un terminal, exécutez la commande docker-compose up
2. lancement du client, dans un autre terminal, exécutez le script python dico/client.py
    1. entrez votre pseudonyme
    2. choisissez le dictionnaire, par exemple 'fr'
    3. entrez un mot en français par exemple
    4. allez sur le dashboard de kafka, ouvrez le topic topic-dictionary-fr, naviguez dans les partitions pour trouver le message avec le mot que vous venez d'entrer
    5. vous devez voir également sur le dashboard un topic nommé topic-dictionary-fr-<pseudonyme>
3. lancement du worker: dans un autre terminal, exécutez le script python dico/worker.py
    1. le worker lit les mots à définir de puis kafka
    2. crawl un site internet (Larousse pour le français)
    3. republie le résultat sur le broker kafka dans le topic  topic-dictionary-fr-<pseudonyme> pour qu'il puisse être lu par le client
    4. dans le même temps, le worker publie dans le topic spark-streaming-dico le mot et sa définition
    5. ce topic sera lu par Spark Streaming pour réaliser d'autres opérations (e.g WordCount)



## Pour aller plus loin
_à faire chez vous_  

Implémentez une application de data pipeline ayant les fonctionnalités suivantes:
- un utilisateur envoie sur un topic Kafka une URL d'un site Internet contenant du texte,
- un premier groupe de consumers lit l'URL, récupère le contenu de l'URL et réalise un WordCount sur ce contenu. Il publie ensuite le résultat de wordCount (liste de mots et leur occurrence) dans Kafka,
- un deuxième groupe de consumers lit le résultat de wordCount et cherche la définition de chaque mot. Il renvoie ensuite au client la liste des mots avec leur occurrence et leur définition.
- l'utilisateur lit ce résultat et... l'enregistre dans une base de données!
- Vous pouvez rajoutez d'autres langues (espagnol, allemand, chinois, etc.)

L'application doit supporter au moins deux langues.

Quelles sont les applications possibles d'un tel programme?

![image](https://user-images.githubusercontent.com/49156499/119236199-6ad67600-bb36-11eb-8078-44b68e7dfcdb.png)
