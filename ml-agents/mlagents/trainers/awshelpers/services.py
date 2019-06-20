import string
import requests
import json
from mlagents.envs.exception import UnityEnvironmentException

api_url = 'https://sw2hs7ufb5gevarvuyswhrndjm.appsync-api.eu-west-1.amazonaws.com/graphql'

headers = {"X-Api-Key": "da2-ynslao5bqbacfdarorkwrwc7ni",
           "Content-Type": "application/json"}

episodeSetQuery = string.Template(
    """
  mutation {
  createSummary(input: {
        meanReward: $meanReward, created: "$created", standardReward: $standardReward, step: $step, summaryEpisodeId: "$summaryEpisodeId"
    }) {
      meanReward
      standardReward
      created
      step
    }
  }
"""
)

episodePostQuery = string.Template(
    """
  mutation {
  createEpisode(input: {
        id: "$uuid", created: "$created", episodeModelId: "$id"
      }) {
        id
        }
    }
"""
)

trainingUpdateQuery = string.Template(
    """
  mutation {
  updateNewborn(input: {
        id: "$id", training: $training
      }) {
        id
        }
    }
"""
)

stepsUpdateQuery = string.Template(
    """
  mutation {
  updateNewborn(input: {
        id: "$id", steps: $steps
      }) {
        id
        models {
            items {
                episodes {
                    items {
                        steps(limit: 10000) { 
                            items {
                                meanReward
                                created
                                standardReward
                                step
                            }
                        }
                    }
                }
            }
        }
        }
    }
"""
)


def post_episode_set(episode_uuid, created, step, mean_rewards, std_rewards):
    request = requests.post(api_url, json={
                            'query': episodeSetQuery.substitute(created=created, meanReward=mean_rewards, standardReward=std_rewards, step=step, summaryEpisodeId=episode_uuid)}, headers=headers)
    if request.status_code == 200:
        print(request.json())
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, episodeSetQuery.substitute(created=created, meanReward=mean_rewards, standardReward=std_rewards, step=step, summaryEpisodeId=episode_uuid)))


def post_episode(created, brain_id, uuid):
    request = requests.post(api_url,
                            json={'query': episodePostQuery.substitute(id=brain_id, created=created, uuid=uuid)}, headers=headers)
    if request.status_code == 200:
        if "errors" in request.json():
            raise UnityEnvironmentException(request.json()["errors"])
        else:
            return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, episodePostQuery.substitute(id=brain_id, created=created, uuid=uuid)))


def update_training_status(brain_id, training):
    request = requests.post(api_url,
                            json={'query': trainingUpdateQuery.substitute(id=brain_id, training=training)}, headers=headers)
    if request.status_code == 200:
        if "errors" in request.json():
            raise UnityEnvironmentException(request.json()["errors"])
        else:
            return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, trainingUpdateQuery.substitute(id=brain_id, training=training)))


def update_steps(brain_id, steps):
    request = requests.post(api_url,
                            json={'query': stepsUpdateQuery.substitute(id=brain_id, steps=steps)}, headers=headers)
    if request.status_code == 200:
        if "errors" in request.json():
            raise UnityEnvironmentException(request.json()["errors"])
        else:
            return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, stepsUpdateQuery.substitute(id=brain_id, steps=steps)))
