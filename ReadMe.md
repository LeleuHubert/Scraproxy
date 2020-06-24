Sujet: Scrappeur et testeur de proxy ouvert socks4/socks5/HTTPS

Objectif 1: Il vous est demandé d'écrire un scrappeur qui va récupérer
            une liste de proxy socks4/socks5/HTTPS. Il existe des sites
            qui listent les proxy ouverts :
              https://hidemy.name/en/proxy-list
              https://proxyscrape.com/free-proxy-list
              http://free-proxy.cz/en/proxylist

            La liste des proxy doit être écrite dans un fichier "list.csv"
            au format: TYPE_PROXY;IP;PORT
            par exemple: "socks4;1.1.1.1;4578"


Objectif 2: Une fois cette liste de proxy construite, il vous est demandé de
            les tester et de construire une deuxième liste dans un fichier
            "working.csv" ayant le même format que le fichier "list.csv".

            Le fichier "working.csv" ne contiendra donc que des proxy fonctionnels.
            Par exemple en bash "curl --socks4 IP:PORT https://ipinfo.io" doit
            retourner l'IP du proxy testé.

Prérequis:

* Utiliser le langage de votre choix (Java/Python/Go/C/C++/C#/Rust)

* Utiliser docker ou podman

* Bonus: Penser au principe du moindre privilège qui s'applique aux conteneurs.

Livrables:

* Un Dockerfile avec le(s) script(s)/source(s)/programme(s) qui rempli les
  objectifs (dans un zip ou un tar.gz)

* Compte rendu expliquant votre cheminement, les points bloquants et les points
  forts de votre réalisation (en PDF)

Vérification:

Pour vérifier nous ferons les commandes suivantes:

    docker build ... && docker run ...
    OU
    podman build ... && podman run ...

Et nous irons exécuter un "cat working.csv" à l'endroit où vous
aurez sauvegardé le fichier dans le conteneur.

Deadline:
29/06/2020 à 09h00
