from flask import Flask
from flask import request
import subprocess
import shlex
import urllib.parse
app = Flask(__name__)


@app.route("/run/", methods=['GET'])
def execute():
    if request.method == 'GET':
        print('Started executing command')
        command = shlex.split("docker run -d --mount type=bind,source=/Users/antoine.doolaeghe/Documents/NewBorn/NewBorn-ml/api/unity-volume,target=/unity-volume -p 5005:5005 ml-agent:latest --docker-target-name=unity-volume ./trainer_config.yaml --env=newborn-lin.x86_64 --train --run-id=1 --no-graphics")
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        print("Run successfully")
        output, err = process.communicate()
        return str(err)
    return "not executed"


if __name__ == "__main__":
    app.run()
