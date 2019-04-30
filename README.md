# Newborn ML agent

This is a Python package that provides a Python API that allows direct interaction with the Unity
game engine. It performs reinforcement learning within Unity to train newborn agents.

The ML-Agents toolkit conducts training using an external Python training process. During training, this external process communicates with the Academy object in the Unity scene to generate a block of agent experiences. These experiences become the training set for a neural network used to optimize the agent's policy (which is essentially a mathematical function mapping observations to actions). In reinforcement learning, the neural network optimizes the policy by maximizing the expected rewards. In imitation learning, the neural network optimizes the policy to achieve the smallest difference between the actions chosen by the agent trainee and the actions chosen by the expert in the same situation.

The output of the training process is a model file containing the optimized policy. This model file is a TensorFlow data graph containing the mathematical operations and the optimized weights selected during the training process. You can use the generated model file with the Learning Brain type in your Unity project to decide the best course of action for an agent.

## Installation

The UnitySDK subdirectory contains the Unity Assets to add to your projects. It also contains many example environments to help you get started.

The ml-agents subdirectory contains a Python package which provides deep reinforcement learning trainers to use with Unity environments.

### Install Python and mlagents Package

In order to use ML-Agents toolkit, you need Python 3.6 along with the
dependencies listed in the [setup.py file](../ml-agents/setup.py).
Some of the primary dependencies include:

- [TensorFlow](Background-TensorFlow.md) (Requires a CPU w/ AVX support)
- [Jupyter](Background-Jupyter.md)

[Download](https://www.python.org/downloads/) and install Python 3.6 if you do not
already have it.

If your Python environment doesn't include `pip3`, see these
[instructions](https://packaging.python.org/guides/installing-using-linux-tools/#installing-pip-setuptools-wheel-with-linux-package-managers)
on installing it.

To install the dependencies and `mlagents` Python package, run from the command line:

```sh
pip3 install mlagents
```

Note that this will install `ml-agents` from PyPi, _not_ from the cloned repo.
If you installed this correctly, you should be able to run
`mlagents-learn --help`, after which you will see the Unity logo and the command line
parameters you can use with `mlagents-learn`.

**Notes:**

- We do not currently support Python 3.7 or Python 3.5.
- If you are using Anaconda and are having trouble with TensorFlow, please see
  the following
  [link](https://www.tensorflow.org/install/pip)
  on how to install TensorFlow in an Anaconda environment.

### Installing for Development

If you intend to make modifications to `ml-agents` or `ml-agents-envs`, you should install
the packages from the cloned repo rather than from PyPi. To do this, you will need to install
`ml-agents` and `ml-agents-envs` separately. From the repo's root directory, run:

```sh
cd ml-agents-envs
pip3 install -e ./
cd ..
cd ml-agents
pip3 install -e ./
```

Running pip with the `-e` flag will let you make changes to the Python files directly and have those
reflected when you run `mlagents-learn`. It is important to install these packages in this order as the
`mlagents` package depends on `mlagents_envs`, and installing it in the other
order will download `mlagents_envs` from PyPi.

## Train an agent.

Use the command mlagents-learn to train your agents. This command is installed with the mlagents package and its implementation can be found at ml-agents/mlagents/trainers/learn.py. The configuration file, like config/trainer_config.yaml specifies the hyperparameters used during training. You can edit this file with a text editor to add a specific configuration for each Brain.

`mlagents-learn <trainer-config-file> --env=<env_name> --run-id=<run-identifier> --train --newborn-id=<newborn-id> --api-connection`

where

- `<trainer-config-file>` is the file path of the trainer configuration yaml.
- `<env_name>`**(Optional)** is the name (including path) of your Unity
  executable containing the agents to be trained. If `<env_name>` is not passed,
  the training will happen in the Editor. Press the :arrow*forward: button in
  Unity when the message *"Start training by pressing the Play button in the
  Unity Editor"\_ is displayed on the screen.
- `<run-identifier>` is an optional identifier you can use to identify the
  results of individual training runs.

For example, suppose you have a project in Unity named "CatsOnBicycles" which
contains agents ready to train. To perform the training:

1. [Build the project](Learning-Environment-Executable.md), making sure that you
   only include the training scene.
2. Open a terminal or console window.
3. Navigate to the directory where you installed the ML-Agents Toolkit.
4. Run the following to launch the training process using the path to the Unity
   environment you built in step 1:

```sh
mlagents-learn config/trainer_config.yaml --env=../../projects/Cats/CatsOnBicycles.app --run-id=cob_1 --train
```

During a training session, the training program prints out and saves updates at
regular intervals (specified by the `summary_freq` option). The saved statistics
are grouped by the `run-id` value so you should assign a unique id to each
training run if you plan to view the statistics. You can view these statistics
using TensorBoard during or after training by running the following command:

```sh
tensorboard --logdir=summaries
```

And then opening the URL: [localhost:6006](http://localhost:6006).

When training is finished, you can find the saved model in the `models` folder
under the assigned run-id — in the cats example, the path to the model would be
`models/cob_1/CatsOnBicycles_cob_1.nn`.

While this example used the default training hyperparameters, you can edit the
[training_config.yaml file](#training-config-file) with a text editor to set
different values.

### Command line training options

In addition to passing the path of the Unity executable containing your training
environment, you can set the following command line options when invoking
`mlagents-learn`:

- `--env=<env>` - Specify an executable environment to train.
- `--curriculum=<file>` – Specify a curriculum JSON file for defining the
  lessons for curriculum training. See [Curriculum
  Training](Training-Curriculum-Learning.md) for more information.
- `--keep-checkpoints=<n>` – Specify the maximum number of model checkpoints to
  keep. Checkpoints are saved after the number of steps specified by the
  `save-freq` option. Once the maximum number of checkpoints has been reached,
  the oldest checkpoint is deleted when saving a new checkpoint. Defaults to 5.
- `--lesson=<n>` – Specify which lesson to start with when performing curriculum
  training. Defaults to 0.
- `--load` – If set, the training code loads an already trained model to
  initialize the neural network before training. The learning code looks for the
  model in `models/<run-id>/` (which is also where it saves models at the end of
  training). When not set (the default), the neural network weights are randomly
  initialized and an existing model is not loaded.
- `--num-runs=<n>` - Sets the number of concurrent training sessions to perform.
  Default is set to 1. Set to higher values when benchmarking performance and
  multiple training sessions is desired. Training sessions are independent, and
  do not improve learning performance.
- `--run-id=<path>` – Specifies an identifier for each training run. This
  identifier is used to name the subdirectories in which the trained model and
  summary statistics are saved as well as the saved model itself. The default id
  is "ppo". If you use TensorBoard to view the training statistics, always set a
  unique run-id for each training run. (The statistics for all runs with the
  same id are combined as if they were produced by a the same session.)
- `--save-freq=<n>` Specifies how often (in steps) to save the model during
  training. Defaults to 50000.
- `--seed=<n>` – Specifies a number to use as a seed for the random number
  generator used by the training code.
- `--slow` – Specify this option to run the Unity environment at normal, game
  speed. The `--slow` mode uses the **Time Scale** and **Target Frame Rate**
  specified in the Academy's **Inference Configuration**. By default, training
  runs using the speeds specified in your Academy's **Training Configuration**.
  See
  [Academy Properties](Learning-Environment-Design-Academy.md#academy-properties).
- `--train` – Specifies whether to train model or only run in inference mode.
  When training, **always** use the `--train` option.
- `--num-envs=<n>` - Specifies the number of concurrent Unity environment instances to collect
  experiences from when training. Defaults to 1.
- `--base-port` - Specifies the starting port. Each concurrent Unity environment instance will get assigned a port sequentially, starting from the `base-port`. Each instance will use the port `(base_port + worker_id)`, where the `worker_id` is sequential IDs given to each instance from 0 to `num_envs - 1`. Default is 5005.
- `--docker-target-name=<dt>` – The Docker Volume on which to store curriculum,
  executable and model files. See [Using Docker](Using-Docker.md).
- `--no-graphics` - Specify this option to run the Unity executable in
  `-batchmode` and doesn't initialize the graphics driver. Use this only if your
  training doesn't involve visual observations (reading from Pixels). See
  [here](https://docs.unity3d.com/Manual/CommandLineArguments.html) for more
  details.
- `--debug` - Specify this option to run ML-Agents in debug mode and log Trainer
  Metrics to a CSV stored in the `summaries` directory. The metrics stored are:
  brain name, time to update policy, time since start of training, time for last experience collection, number of experiences used for training, mean return. This
  option is not available currently for Imitation Learning.

### Training config file

The training config files `config/trainer_config.yaml`,
`config/online_bc_config.yaml` and `config/offline_bc_config.yaml` specifies the
training method, the hyperparameters, and a few additional values to use during
training with PPO, online and offline BC. These files are divided into sections.
The **default** section defines the default values for all the available
settings. You can also add new sections to override these defaults to train
specific Brains. Name each of these override sections after the GameObject
containing the Brain component that should use these settings. (This GameObject
will be a child of the Academy in your scene.) Sections for the example
environments are included in the provided config file.

| **Setting**        | **Description**                                                                                                                                                                         | **Applies To Trainer\*** |
| :----------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------- |
| batch_size         | The number of experiences in each iteration of gradient descent.                                                                                                                        | PPO, BC                  |
| batches_per_epoch  | In imitation learning, the number of batches of training examples to collect before training the model.                                                                                 | BC                       |
| beta               | The strength of entropy regularization.                                                                                                                                                 | PPO                      |
| brain_to_imitate   | For online imitation learning, the name of the GameObject containing the Brain component to imitate.                                                                                    | (online)BC               |
| demo_path          | For offline imitation learning, the file path of the recorded demonstration file                                                                                                        | (offline)BC              |
| buffer_size        | The number of experiences to collect before updating the policy model.                                                                                                                  | PPO                      |
| curiosity_enc_size | The size of the encoding to use in the forward and inverse models in the Curiosity module.                                                                                              | PPO                      |
| curiosity_strength | Magnitude of intrinsic reward generated by Intrinsic Curiosity Module.                                                                                                                  | PPO                      |
| epsilon            | Influences how rapidly the policy can evolve during training.                                                                                                                           | PPO                      |
| gamma              | The reward discount rate for the Generalized Advantage Estimator (GAE).                                                                                                                 | PPO                      |
| hidden_units       | The number of units in the hidden layers of the neural network.                                                                                                                         | PPO, BC                  |
| lambd              | The regularization parameter.                                                                                                                                                           | PPO                      |
| learning_rate      | The initial learning rate for gradient descent.                                                                                                                                         | PPO, BC                  |
| max_steps          | The maximum number of simulation steps to run during a training session.                                                                                                                | PPO, BC                  |
| memory_size        | The size of the memory an agent must keep. Used for training with a recurrent neural network. See [Using Recurrent Neural Networks](Feature-Memory.md).                                 | PPO, BC                  |
| normalize          | Whether to automatically normalize observations.                                                                                                                                        | PPO                      |
| num_epoch          | The number of passes to make through the experience buffer when performing gradient descent optimization.                                                                               | PPO                      |
| num_layers         | The number of hidden layers in the neural network.                                                                                                                                      | PPO, BC                  |
| sequence_length    | Defines how long the sequences of experiences must be while training. Only used for training with a recurrent neural network. See [Using Recurrent Neural Networks](Feature-Memory.md). | PPO, BC                  |
| summary_freq       | How often, in steps, to save training statistics. This determines the number of data points shown by TensorBoard.                                                                       | PPO, BC                  |
| time_horizon       | How many steps of experience to collect per-agent before adding it to the experience buffer.                                                                                            | PPO, (online)BC          |
| trainer            | The type of training to perform: "ppo" or "imitation".                                                                                                                                  | PPO, BC                  |
| use_curiosity      | Train using an additional intrinsic reward signal generated from Intrinsic Curiosity Module.                                                                                            | PPO                      |
| use_recurrent      | Train using a recurrent neural network. See [Using Recurrent Neural Networks](Feature-Memory.md).                                                                                       | PPO, BC                  |

\*PPO = Proximal Policy Optimization, BC = Behavioral Cloning (Imitation)

For specific advice on setting hyperparameters based on the type of training you
are conducting, see:

- [Training with PPO](Training-PPO.md)
- [Using Recurrent Neural Networks](Feature-Memory.md)
- [Training with Curriculum Learning](Training-Curriculum-Learning.md)
- [Training with Imitation Learning](Training-Imitation-Learning.md)

You can also compare the
[example environments](Learning-Environment-Examples.md)
to the corresponding sections of the `config/trainer_config.yaml` file for each
example to see how the hyperparameters and other configuration variables have
been changed from the defaults.
