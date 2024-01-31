# GNS3_Projet

## Comment faire fonctionner?
1. Cloner le projet avec `git clone https://github.com/duckduckxuan/GNS3_Projet`.
2. Se placer dans le répértoire projet_finale avec `cd projet_finale`.
3. Pour le drag and drop bot, utiliser `python3 main.py`.
4. Pour le script telnet, ouvrir gns3_final avec gns3 puis utiliser `python3 telnet.py`.

Attention: Le routeur ne doit pas avoir le message: "Would you like to enter the initial configuration dialog?".

Attention: Chaque routeur doit avoir 3 slot PA-GE.

Attention: Le projet GNS3 doit être nommé "gns3_final"


## Description des fichiers:

### Dans Projet_finale:

router_infos_TBD.json -> Le json contenant les informations sur le réseau.

allocate_addres.py -> Assigne les addresses IP automatiquement et contient les classes Router et AS.

configuration.py -> Contient les fonctions pour le drag & drop bot.

main.py -> Script exécutable du drag & drop bot.

telnet_configuration.py -> Equivalent de configuration.py mais pour telnet.

telnet.py -> Script exécutable de Telnet.

gns_final -> Contient le projet gns3 qu'il faut ouvrir.
