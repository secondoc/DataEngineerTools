from flask import Flask

app=Flask(__name__, template_folder='template')

from flask import request
from flask import render_template, render_template_string
from flask import redirect

import pymongo

client = pymongo.MongoClient("mongo")
database = client['projet']
collection = database['movies']

def sortfilm(collection, condition, genre, nbr):
    """
    Fonction permettant de faire intéragir la page Flask top film.
    Args:
        Str : Condition de sélection du top film
        Str : Filtre des films par genre
        Int : Nombre de film à afficher
    Return:
        Liste : Liste des films en fonction du top et du genre
    """
    genrefilter = ['Action', 'Animation', 'Aventure', 'Biopic', 'Comédie', 'Comédie dramatique', 'Comédie musicale', 'Documentaire', 'Drame', 'Epouvante-horreur', 'Famille', 'Fantastique', 'Guerre', 'Historique', 'Musical', 'Policier', 'Romance', 'Science fiction', 'Thriller', 'Western', 'Divers']
    #On trie en fonction de la condition
    if (condition == "bestpub"): 
        trie = [('notepub',-1), ('nbrnote',-1)]
        info = {'title':1, 'notepub':1, 'nbrnote':1, 'genre':1}
        legend = ['Titre', 'Genre(s)', 'Nombre de note', 'Note']
    elif (condition == "bestpre"):
        trie = [('notepre',-1), ('nbrnote',-1)]
        info = {'title':1, 'notepre':1, 'nbrnote':1, 'genre':1}
        legend = ['Titre', 'Genre(s)', 'Nombre de note', 'Note']
    elif (condition == "recent"):
        trie = [('date',-1)]
        info = {'title':1, 'date':1, 'genre':1}
        legend = ['Titre', 'Genre(s)', 'Date (Y-m-d)']
    elif (condition == "ancien"):
        trie = [('date',1)]
        info = {'title':1, 'date':1, 'genre':1}
        legend = ['Titre', 'Genre(s)', 'Date (Y-m-d)']
    elif (condition == "rent"):
        trie = [('rent',-1)]
        info = {'title':1, 'rent':1, 'genre':1}
        legend = ['Titre', 'Genre(s)', 'Rentabilité']
    elif (condition == "long"):
        trie = [('duree',-1)]
        info = {'title':1, 'duree':1, 'genre':1}
        legend = ['Titre', 'Genre(s)', 'Durée']
    elif (condition == "court"):
        trie = [('duree',1)]
        info = {'title':1, 'duree':1, 'genre':1}
        legend = ['Titre', 'Genre(s)', 'Durée']
    
    #On ajoute le filtre pour le genre
    if (genre != 'All') : genrefilter = [genre]
    
    #On récupère
    movielist = collection.find({'genre': {'$in' : genrefilter}}, info).sort(trie)
    
    data=[]
    data.append(legend)
    for k in (list(movielist)[:nbr]):
        data.append(list(k.values())[1:])
    if ('Date (Y-m-d)' in data[0]):
        for l in data[1:]: l[-1]=str(l[-1]).split()[0]
        
    #On affiche le résultat
    return(data)

def selectmovie(collection, moviename):
    """
    Fonction permettant d'avoir toutes les informations sur un film
    Args: 
        Str: Nom du film
    Returns:
        Liste : Toutes les informations sur le film
    """
    movieinfo = collection.aggregate([{'$match': {'title' : moviename}}])
    if (list(collection.aggregate([{'$match': {'title' : moviename}}])) == []):
        return("Movie not found")
    else:
        data = []
        data.append(list(list(movieinfo)[0].values())[1:])
        return(data)

@app.route('/')
def hello():
    return render_template('accueil.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('erreur.html')

@app.route('/recherche/')
def recherche():
    return render_template('recherche.html')

@app.route('/recherche/', methods=['POST'])
def recherche_post():
    title = request.form['C']
    return redirect('/recherche/'+title)

@app.route('/recherche/<title>')
def film(title):
    data=selectmovie(collection, title)
    if(data=="Movie not found"):
        return render_template('filmnotfound.html')
    else :
        title=data[0][0]
        titleint=data[0][1]
        synop=data[0][2]
        genre=data[0][3]
        date=data[0][4]
        duree=data[0][5]
        cast=data[0][6]
        real=data[0][7]
        nbrnote=data[0][8]
        nbrcrit=data[0][9]
        notepub=data[0][10]
        notepre=data[0][11]
        budget=data[0][13]
        boxdom=data[0][14]
        boxint=data[0][15]
        boxtot=data[0][16]
        rent=data[0][17]
        return render_template('film.html', title=title, titleint=titleint, synop=synop, genre=genre, date=date, duree=duree, cast=cast, real=real, nbrnote=nbrnote, nbrcrit=nbrcrit, notepub=notepub, notepre=notepre, budget=budget, boxdom=boxdom, boxint=boxint, boxtot=boxtot, rent=rent)

@app.route('/top/')
def top():
    return render_template('top.html')

@app.route('/top/', methods=['POST'])
def top_post():
    top = request.form['tops']
    genre = request.form['genres']
    n = request.form['nb']
    return redirect('/top/'+top+'/'+genre+'/'+n)

@app.route('/top/<top>/<genre>/<n>')
def top_film(top,genre,n):
    t=sortfilm(collection, top, genre, int(n))
    if top=="bestpub":
        top1="des films les mieux notés par le public"
    elif top=="bestpre":
        top1="des films les mieux notés par la presse"
    elif top=="rent":
        top1="des films les plus rentables"
    elif top=="recent":
        top1="des films les plus récents"
    elif top=="ancien":
        top1="des films les plus anciens"
    elif top=="long":
        top1="des plus longs films"
    elif top=="court":
        top1="des films les plus courts"
    else:
        top1="des films"
    if genre == "All":
        genre = None
    indice=t[0]
    data=t[1:]
    return render_template('topfilm.html', top1=top1, genre=genre, n=n, indice=indice, data=data)
   
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)