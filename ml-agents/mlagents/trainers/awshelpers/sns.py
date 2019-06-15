import string
import requests
import json
from mlagents.envs.exception import UnityEnvironmentException

api_url = 'https://sw2hs7ufb5gevarvuyswhrndjm.appsync-api.eu-west-1.amazonaws.com/graphql'

headers = {"X-Api-Key": "da2-gpogt2u3kzbgpo54oikxxgg7am",
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

developmentStageUpdateQuery = string.Template(
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


@staticmethod
def post_episode_set(episode_uuid, created, step, mean_rewards, std_rewards):
    request = requests.post(api_url, json={
                            'query': episodeSetQuery.substitute(created=created, meanReward=mean_rewards, standardReward=std_rewards, step=step, summaryEpisodeId=episode_uuid)}, headers=headers)
    if request.status_code == 200:
        print(request.json())
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, episodeSetQuery.substitute(created=created, meanReward=mean_rewards, standardReward=std_rewards, step=step, summaryEpisodeId=episode_uuid)))

@staticmethod
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
                            json={'query': developmentStageUpdateQuery.substitute(id=brain_id, training=training)}, headers=headers)
    if request.status_code == 200:
        if "errors" in request.json():
            raise UnityEnvironmentException(request.json()["errors"])
        else:
            return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, episodePostQuery.substitute(id=brain_id, created=created, uuid=uuid)))
