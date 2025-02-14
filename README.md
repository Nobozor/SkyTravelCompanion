# Projet CICD : SkyTravelCompanion

## Présentation du projet
SkyTravelCompanion est une web app qui permet de récupérer les informations d'un vol avec son numéro de vol et de proposer des divertissements pour la durée du vol.
En renseignant un numéro de vol, les utilisateurs peuvent accéder aux informations en temps réel de leur avion et découvrir des suggestions de divertissements adaptés à la durée du trajet, comme des films et de la musique. 
L'application permet également aux voyageurs et à leurs proches de suivre le vol en direct.

## Features du projet
- Feature 1 :  
La première feature de l'application est d'afficher les informations d'un vol en direct. Notamment la position de l'avion sur une carte du monde en temps réel, la latitude/longitude de l'avion, ...

- Feature 2 :
La deuxième feature de l'application est de proposer des films en fonction du genre souhaité et renseigné par l'utilisateur en fonction de la durée totale du vol.

- Feature 3 :
La troisième feature de l'application est de proposer des musiques (spotify) en fonction du genre souhaité et renseigné par l'utilisateur en fonction de la durée totale.


## Informations techniques sur le projet :
Pour la réalisation de notre application, nous avons utilisé différentes API externes : 
- OpenSky Network API : API pour récupérer des informations sur les vols
- The Movie DataBase (TMDB) : API pour récupérer les films
- Web API Spotify : API pour récupérer les musiques de spotify

Pour la partie build, elle est crée au niveau de la CI dans GitHub Actions ce qui permet que cette partie soit automatisée. Lien DockerHbub de l'image Docker :
```
https://hub.docker.com/r/nobozor/skytravelcompanion
```

Pour la partie run, il est nécessaire de taper la commande suivante afin de lancer en local l'application : 
```
docker run IMAGES_DOCKER
```

Pour se connecter à l'application, il suffit de taper l'adresse suivante :

```
http://localhost:8080
```

# Utlisation de l'application

Une fois sur le page web de l'application, vous disposerez de 3 onglets situé en haut à droite de la page.

## Informations de Vol

Vous pouvez rentrer le numéro d'un vol en cours dans la barre de recherche et les informations correspondantes seront affichées (emplacement sur la carte en temps réel, heure de départ, heure d'arrivée, etc.)

## Films

Vous pouvez entrer la durée de votre prochain vol ainsi que le genre de film que vous souhaitez regarder et l'application vous retournera une liste de films qui rempliera la durée totale du vol (entre 90 et 100% de la durée).

## Musique

Vous pouvez entrer la durée de votre prochain vol ainsi que le style de musique que vous souhaitez écouter et l'application vous retournera une playsit qui rempliera la durée totale du vol (entre 90 et 100% de la durée).
