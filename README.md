# DL4G (Deep Learning for Games)
HSLU - Lucerne University of Applied Sciences and Arts / Modul: DL4G (Deep Learning for Games)

## Infos

* Tournaments -> https://jass-server.abiz.ch/tournaments

## Input Koller

* Round from PlayerRound
    * round_factory.get_round_from_player_round -> braucht hand array von Spielern -> simulieren!
    * round.action_play_card()
    * Nach jeder runde eine neue Round!

## Example Repo

* https://github.com/amh38/DL4G/tree/master/jass-demo/my_jass

## Uberspace

### Setup

* Deploy with ./deploy.sh script (change uberspace when it changes)

* Get a Port
    ```cmd
    uberspace port add
    ````
* Route to Service
    ```
    uberspace web backend set / --http --port {PORT_FROM_ABOVE}
    ```
* Create Service -> https://manual.uberspace.de/en/daemons-supervisord.html?highlight=service

### Infos 'tschinux' Uberspace

* Port -> 46960 (automatically by 'uberspace port add')
* Url -> https://tschinux.uber.space:46960/rule_based_player

## EnterpriseLab Server

### Infos

```
Hostname: dl4g-h19-tjineich.el.eee.intern
Username with SUDO-Rights: tjineich
Network: Internal
```

## ToDo

# Remo
* Train Play Card Model with all Data

# Steve
* Check which Trump Selection Model performs better (V2 or V0)
* Setup Server
