# paa1382_crc_decoder
Décode le CRC des trames FFSK émises par l'ATR 425 DIAMANT, utilisant une variante "maison" du standard PAA 1382.

Ce code a été généré par ChatGPT, puis validé avec un lot de 80 captures de trames.

# Utilité
Ce programme permet de vérifier la validité du CRC d'une trame FFSK  destination ou provenant d'un poste ATR 425 DIAMANT.

![Picture of the ATR 425 DIAMANT logic board with logic analyzer probes attached to it](https://github.com/DevSHIBBY/paa1382_crc_decoder/blob/main/doc/probes_on_board.jpg)

Dans l'exemple ci-dessus, les données sont capturées directement sur les signaux Donnée (pin 6) et Horloge (pin 6) du FX419J.

La trame capturée est décodée à l'aide d'un décodeur synchrone :

![Logic analyzer captured data](https://github.com/DevSHIBBY/paa1382_crc_decoder/blob/main/doc/logic_analyzer_capture.png)

Les deux octets 0xAA représentent le préambule, et non une donnée utile.

# Utilisation

Ouvrir le décodeur avec la commande suivante :
```
python check_crc.py
```

Entrer la trame à vérifier dans la zone de saisie (supprimer préalablement l'exemple) puis appuyer sur  le bouton **Valider** : 

![Decoder screenshot](https://github.com/DevSHIBBY/paa1382_crc_decoder/blob/main/doc/decoder.png)

Si le CRC est correct, la zone de résultat en bas s'affiche sur fond vert. Dans le cas contraire, cette zone s'affiche sur fond rouge et indique le CRC attendu selon son calcul.

# Plus d'infos

Consulter cette page : [SHIBBY's Blog (FR)](https://blog.shibby.fr/2017/10/alcatel-atr42x-la-resurrection/)
