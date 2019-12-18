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

* Deploy with ./deploy.sh {complete} script (change uberspace when it changes)

* Upgrade old setuptools form uberspace `pip install --upgrade setuptools`

* Install requirements.txt with `pip install -r requirements.txt`

```
tensorflow
numpy
keras
jupyter
pandas
matplotlib
flask

```

* Install jass-kit `cd `

* Get a Port
    ```cmd
    uberspace port add
    ````
* Route to Service
    ```cmd
    uberspace web backend set / --http --port {PORT_FROM_ABOVE}
    ```
* Create Service -> https://manual.uberspace.de/en/daemons-supervisord.html?highlight=service
    ```cmd
    [tschinu2@holmes dl4g]$ cat ~/etc/services.d/jass-service.ini
    [program:jass-service]
    command=/home/tschinu2/dl4g/run_service.sh
    autostart=yes
    autorestart=yes
    [tschinu2@holmes dl4g]$
    ```

### Infos 'tschinux' Uberspace

* Port -> 49960 (automatically by 'uberspace port add')
* Url -> http://tschinu2.uber.space:49960/deep_learning_player
* Service steuern:
```bash
supervisorctl status
supervisorctl stop jass-service
supervisorctl start jass-service
```
* Check Port
```bash
uberspace web backend list
```


## EnterpriseLab Server

### Infos

```
Hostname: dl4g-h19-tjineich.el.eee.intern
Username with SUDO-Rights: tjineich
Password: same as the uberspace one...
Network: Internal
```

````
sudo apt install virtualenv
virtualenv -p python3 dl4g-env
source dl4g-env/bin/activate
echo "source dl4g-env/bin/activate" >> .bashrc

--> run our `deploy.sh complete` script

testing `python arena.py
```


## ToDo

# Remo
* Train Play Card Model with all Data

# Steve
* Check which Trump Selection Model performs better (V2 or V0)
* Setup Server



## AWS

IP: 3.122.231.89
ssh -i "DL4G.pem" ubuntu@ec2-3-122-231-89.eu-central-1.compute.amazonaws.com


Player: http://3.122.231.89:5005/deep_learning_player

started with tmux

Start game: tmux ./~/dl4g/run_service_aws.sh -> cntr+b d
Session killen: tmux kill-ses -t <session>
