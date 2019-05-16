
echo "activating python3"
source /home/ubuntu/anaconda3/bin/activate  python3
echo "Initialize python environment"
mlagents-learn ./unity-volume/config/trainer_config.yaml --env=./unity-volume/newborn --train --newborn-id=10174714450863337318529 --no-graphics