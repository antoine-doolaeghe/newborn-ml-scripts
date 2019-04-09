from flask import Flask
from flask import request
from mlagents.trainers.learn import run_training
from multiprocessing import Process, Queue
import subprocess
import shlex
import urllib.parse
app = Flask(__name__)


@app.route("/run/", methods=['GET'])
def execute():
    if request.method == 'GET':
        print('Started executing command')
        options = {
            '--api-connection': True,
            '--curriculum': 'None',
            '--docker-target-name': 'None',
            '--env': 'None',
            '--help': False,
            '--keep-checkpoints': '5',
            '--lesson': '0',
            '--load': False,
            '--no-graphics': True,
            '--num-runs': '1',
            '--run-id': 'ppo',
            '--save-freq': '50000',
            '--seed': '-1',
            '--slow': False,
            '--train': True,
            '--worker-id': '0',
            '<trainer-config-path>': '../config/trainer_config.yaml'
        }
        run_training(0, 4445, options, Queue())
    return "not executed"


if __name__ == "__main__":
    app.run()
