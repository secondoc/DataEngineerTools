
#Importations pour scrapy 
import scrapy
import pandas as pd
import numpy as np
import os
#Importations pour mongo
import pymongo
import unicodedata




def scrap():
    """
    Procédure permettant de lancer le scrap du site allociné.fr et boxofficemojo.com
    """
    os.system("scrapy crawl moviesv1 -o rsltmoviesv1.csv")
    return None

def deletecsv():
    """
    Procédure afin de supprimer le fichiers csv généré par le scrap afin d'éviter les doublons si le programme se relance.
    """
    os.remove("rsltmoviesv1.csv")
    return None

def mongo():
    """
    Procédure qui récupère le contenu du fichier csv du scrap, la nettoie, la met en forme et la rentre dans la base de donnée Mongo
    """
    #Initialisation du Mongo
    client = pymongo.MongoClient("mongo")
    database = client['projet']
    collection = database['movies']
    
    #Récupération des données du fichier csv
    df_movies = pd.read_csv("rsltmoviesv1.csv")
    
        #Nettoyage de la base de donnée
    #Nettoyage de la partie allociné
    for i in range (df_movies.shape[0]):
        if (df_movies["catinfo"][i] != ' Titre original '):
            df_movies["titleint"][i] = unicodedata.normalize('NFD', df_movies["title"][i]).encode('ascii', 'ignore').decode('utf-8')
    df_movies = df_movies.drop(columns=['catinfo'])

    #Nettoyage de la partie boxofficemojo
    for i in range (df_movies.shape[0]): 
        if ((df_movies['boxint'][i] == df_movies['boxtot'][i]) and ('$' not in df_movies['boxdom'][i][0])):
            df_movies['boxdom'][i] = np.NaN
        if ((type(df_movies['boxint'][i]) == float) and ('$' not in df_movies['boxdom'][i])):
            df_movies['boxdom'][i] = df_movies['boxtot'][i]
            df_movies['boxint'][i] = np.NaN
        
    #Mise en forme
    df_movies['rent'] = pd.Series(np.NaN, index=df_movies.index)
    for i in range (df_movies.shape[0]):
        #Mise en place de la colonne rentabilité
        if (type(df_movies['boxtot'][i]) == float or type(df_movies['budget'][i]) == float):
            df_movies['rent'][i] = np.NaN
        else:
            df_movies['rent'][i] = float(df_movies['boxtot'][i][1:].replace(',','')) - float(df_movies['budget'][i][1:].replace(',',''))

        #Séparation des genres en liste de genre et non une string de genre
        df_movies['genre'][i] = df_movies['genre'][i].split(',')  
        
        #Mise en place du format date pour la colonne date
        df_movies['date'][i] = df_movies['date'][i].replace(' ', '-')
        if ('janvier' in df_movies['date'][i]): df_movies['date'][i] = df_movies['date'][i].replace('janvier', '01')
        elif ('février' in df_movies['date'][i]): df_movies['date'][i] = df_movies['date'][i].replace('février', '02')
        elif ('mars' in df_movies['date'][i]): df_movies['date'][i] = df_movies['date'][i].replace('mars', '03')
        elif ('avril' in df_movies['date'][i]): df_movies['date'][i] = df_movies['date'][i].replace('avril', '04')
        elif ('mai' in df_movies['date'][i]): df_movies['date'][i] = df_movies['date'][i].replace('mai', '05')
        elif ('juin' in df_movies['date'][i]): df_movies['date'][i] = df_movies['date'][i].replace('juin', '06')
        elif ('juillet' in df_movies['date'][i]): df_movies['date'][i] = df_movies['date'][i].replace('juillet', '07')
        elif ('août' in df_movies['date'][i]): df_movies['date'][i] = df_movies['date'][i].replace('août', '08')
        elif ('septembre' in df_movies['date'][i]): df_movies['date'][i] = df_movies['date'][i].replace('septembre', '09')
        elif ('octobre' in df_movies['date'][i]): df_movies['date'][i] = df_movies['date'][i].replace('octobre', '10')
        elif ('novembre' in df_movies['date'][i]): df_movies['date'][i] = df_movies['date'][i].replace('novembre', '11')
        elif ('décembre' in df_movies['date'][i]): df_movies['date'][i] = df_movies['date'][i].replace('décembre', '12')
    df_movies['date'] = pd.to_datetime(df_movies['date'], format='%d-%m-%Y')

    #Mise en place dans mongo
    collection.delete_many({})
    collection.insert_many(df_movies.to_dict(orient='records'))
    
    return None


def main():
    scrap()
    mongo()
    deletecsv()
    return None



if __name__ == '__main__':
    main()
    