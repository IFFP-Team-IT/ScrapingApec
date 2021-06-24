Lorsque le programme se lance, il récupère le numero de page inscrit dans le fichier program_data
Ensuite, il va créé chaque jours un fichier au format apec_aaaammjj.xlsx dans le dossier BDD et créé aussi les feuilles main , compétences, lang, atouts, nb_moments_cles. Ce fichier récupère tous les éléments que le robot va scraper.

Il vérifie s'il est autorisé a utilisé un proxy ou pas(variable booléenne useproxy créé dans scr_hlp et initialiser dans Extrapec.py)
Ensuite, charge la page a scraper tout en vérifiant si une connexion internet est active
et vérifie si la page a été bien charger.(fonction load_page et load_page_helper dans la class scr_hlp)

Ouvre un fichier usernames.xlsx contenant les identifiant et mot de passe pour se connecter au site.
Il effectue une connexion vers le site avec le premier user et passe au suivant lorsque , lorsque ce dernier a atteint sa vistelimit(inscrit dans la variable visitlimits)

Ensuite, il vérifie le nombre de candidat à scraper sur une page puis vérifie aussi s'il existe encore des pages a scraper(fonction scr_hlp.is_next_page_exists).

Il recupère le lien vers chaque profil (ligne 93 à 96 dans Extrapec.py)

Avant de charger la page, il vérifie si l'id du profil existe déjà dans la bdd, si oui skip sinon charge la page et récupère tout.
Il répète l'action jusqu'à ce que tout les utilisateurs présents dans le fichier usernames.xlsx aient effectué leur nombre de visites requise. Sachant que chaque utilisateur effectue une pause entre chaque visite suivant la variable recupéré dans le champs Nombre de visite avant la pause du fichier Config.xlsx

Avant d'arrêter le programme il vérifie si tous les fichiers zippé ont été dézippé dans le dossier FILES et remet le nombre de visits des utilisateur a zero dans le fichier usernames.xlsx.

NB: Les dossiers LOG, BDD et FILES sont créé automatiquement

