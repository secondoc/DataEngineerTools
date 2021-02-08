USER GUIDE
L'ensemble des éléments à installer pour la partie des conteneurs seront automatiquement installés au lancement de docker.
Si scrapy n'est pas installé : pip install scrapy

Les packages suivants sont automatiquement importés pour le bon fonctionnement du code:
os : Pour la manipulation de fichier;
pandas, numpy et unicodedata : Pour la manipulation de dataframe;
scrapy : Pour la réalisation des scraps pour notre base de donnée

Afin de lancer les conteneurs et application il est nécessaire d'effectuer, à la racine du projet, la commande : $ docker-compose up -d 
De se connecter à l'adresse suivante : http://localhost:8888/
Afin de lancer le scrap et l'utilisation des applications il est nécessaire d'ouvrir le fichier ProjetDataEngineering.ipynb dans le dossier Projet
Une fois le programme terminé vous pouvez accéder à l'interface sur le lien suivant : http://127.0.0.1/

Le programme va récupérer en direct la liste des 300 meilleurs films du site https://www.allocine.fr/ ainsi que ses informations. 
Il va également aller chercher des informations complémentaires sur le site de https://www.boxofficemojo.com/ concernant le résultat au boxoffice et le budget du film.
Le tout sera stocké dans une base de donnée mongodb avant d'être affiché sur le site de manière intéractive.

Sur la première page du site, vous avez deux options : Recherche et Top film.
La fonctionnalité recherche va vous permettre de chercher un film présent dans les 300 meilleurs films d’Allociné avec son titre exact ! Vous pourrez revenir à la page principale avec le bouton retour. 
Si le titre n’est pas exact, vous allez pouvoir revenir à la page principal avec un bouton retour également. 
La fonctionnalité top film va quant à elle vous permettre de chercher les meilleurs films selon le public, la presse ou même la durée du film : vous n’avez qu’à sélectionner le top qui vous intéresse dans le genre souhaité puis à insérer le nombre de films que vous voulez voir apparaître. 
Une fois le top consulté, retour au menu principal avec le bouton retour en bas de page. 

DEVELOPPER GUIDE

Le code est structuré sous la forme de différents fichiers écrits en python et en HTML.
Le notebook ProjetDataEngineering.ipynb contient le code afin de lancer le programme ProjectDataEngineering.py dans un conteneur afin d’avoir accès aux applications des conteneurs.
Le fichier ProjectDataEngineering.py est composé d’une fonction main et de plusieurs fonctions et procédures :
scrap() : Procédure afin de lancer le scraping du site de allociné avec une ligne de commande. La classe du spider se trouve dans le dossier newscrawler/spider/moviesv1.py. Et est constitué de 4 parses et de fonctions pour traiter les données. 
deletecsv() : Procédure afin de supprimer le fichier csv après l’avoir placé dans mongo afin de continuer à avoir des données à jour
mongo() : Procédure qui traite les données scrappées, et qui les place dans mongo.


Pour la partie Flask, nous avons un fichier app.py placé dans le conteneur flask qui permet de faire tourner notre site web. Nous avons également un dossier template contenant toutes les templates html. 

app.py contient toutes les importations Flask nécessaires.
Il est constitué d’une fonction main() et de différentes fonctions afin de définir les routes entre les pages internets. Mais également de deux fonctions permettant de récupérer les informations dans la base de données mongodb.

Dans la ligne 6, template_folder='template' nous pouvons changer l’emplacement des templates. ‘template’ nous ramène vers le dossier du même nom.

Nous important ensuite mongo et notre database.

Nous retrouvons après les 2 fonctions sortfilm(collection, condition,genre,nbr) et selectmovie(collection,moviename) avec lesquelles nous allons chercher les informations que l’on souhaite dans notre collection :
sortfilm(....) : Fonction qui prend en paramètre la base de données mongo, la conditions de sélection des données, un filtre sur une colonne et le nombre de films à afficher. Il permet de retourner les informations de la page top film.
selectmovie(..) : Fonction qui prend en paramètre la base de données et le titre du film recherché. Il retourne toutes les informations que possède la base de données sur le film.

Nous avons créer des routes différentes qui nous amènent vers des templates différents. 

ligne 76 : route 404  pour avoir une page d’erreur personnalisée 

ligne 84 : première utilisation de la méthode Post qui nous permet de récupérer des informations laissées sur le site par l'utilisateur : le titre d’un film qu’il recherche

On utilise cette information ligne 89 en récupérant le titre dans l’url du site. On utilise cette donnée dans la fonction selectmovie précédente.

On récupère les informations (lignes 95 à 111) pour pouvoir les afficher correctement dans film.html.


ligne 118 : seconde utilisation de la méthode Post : on récupère 3 informations différentes  dans l’url encore une fois qu’on utilise ligne 126.

fonction top_film(top, genre, n) : on vient créer la variable top1 pour pouvoir afficher quelque chose de plus lisible qui a du sens
ligne 144 : on modifie le genre si “All” en None. Ça nous permet d’afficher quelque chose de plus lisible encore une fois. 

 
ligne 150 : ligne classique de flask pour que l’application s’exécute. 

accueil.html : Design de la page web d’accueil
erreur.html : Design de la page d’erreur 404, bouton ramenant à la page d’accueil
recherche.html : Design de la page de recherche de film, form permettant de récupérer l’information donnée par l’utilisateur
film.html : Design de la page de présentation d’un film avec toutes ses caractéristiques
filmnotfound.html : Design de la page lorsque l’information récupérée ne se connecte pas à la base (quand le film n’est pas dans la base ou quand le titre n’est pas exact)
top.html : Design de la page de top de films, form permettant de récupérer les informations données par l’utilisateur
topfilm.html : Design de la page affichant le nombre de films donnés par l’utilisateur (utilisation de boucle for) sous forme de tableau avec le top choisi ainsi que le genre de film choisi. 

