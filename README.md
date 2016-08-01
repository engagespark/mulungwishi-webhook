Public Webhook
===============
Webhook for:
* [Mulungwishi Fertilizer Project](https://www.youtube.com/watch?v=qkBsuUHCFWo)
* Weather Forecast


Install dependencies
--------------------
Install flask and virtualenv (if you do not have one):  http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

Install also dependencies on requirements.txt:
```
$ pip install -r requirements.txt
```


Running
-------
### Run on Terminal: `$ python run.py`

#### To visit mulungwishi webhook index: http://127.0.0.1:5000
#### To visit mulungwishi webhook: http://127.0.0.1:5000/query
#### To visit weather-forecast webhook: http://127.0.0.1:500/weather_forecast


Show travis build in github repo
--------------------------------

[![Build Status](https://travis-ci.org/engagespark/public-webhooks.svg?branch=master)](https://travis-ci.org/admiral96/mulungwishi-webhook)


Deploying
---------
You're gonna need a public key (`mulungwishi_rsa.pub`) and place it as `~/.ssh/mulungwishi_rsa.pub` to deploy.

```
$ make deploy
```
