mulungwishi-webhook
===================
Webhook for the [Mulungwishi Fertilizer Project](https://www.youtube.com/watch?v=qkBsuUHCFWo)

Install dependencies
--------------------
Install flask and virtualenv (if you do not have one):  http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

Install also dependencies on requirements.txt.


Running
-------

### Run on Terminal: python run.py

Note: Default host is 127.0.0.1, run on fb server e.g. `python run.py 10.11.12.170`

### Running in local, visit: http://127.0.0.1:5000/
### Running through fb server, visit: http://10.11.12.170:5000/

Show travis build in github repo
--------------------------------

[![Build Status](https://travis-ci.org/admiral96/mulungwishi-webhook.svg?branch=master)](https://travis-ci.org/admiral96/mulungwishi-webhook)


Deploying on toys.engagespark.com
---------------------------------
You're gonna need a public key (`mulungwishi_rsa.pub`) and place it as `~/.ssh/mulungwishi_rsa.pub` to deploy.

```
make deploy
```
