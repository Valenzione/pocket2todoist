import os
from . import requests
import json
import random

def lambda_handler(event, context):
   
    pocket_token = os.getenv("POCKET_ACCESS_TOKEN")
    pocket_key = os.getenv("POCKET_CONSUMER_KEY")
    todoist_token = os.getenv("TODOIST_TOKEN")
    number_of_articles = int(os.getenv("NUMBER_OF_ARTICLES"))

    pocket_json_body = {"consumer_key":pocket_key,
                "access_token":pocket_token,
                "count":"50",
                "detailType":"simple"}

    todoist_headers = {"Authorization":f"Bearer {todoist_token}"}
    todoist_task = {"content" : "NULL",
                            "due_string" : "today",
                            "due_lang": "en", 
                            "project_id" : 2199444839}

    get_articles = requests.get("https://getpocket.com/v3/get", json = pocket_json_body)

    if get_articles.status_code == 200:
        titles = []
        articles = get_articles.json()['list']
        articles_ids = list(articles.keys())
        random.shuffle(articles_ids)
        articles_ids = articles_ids[:number_of_articles]
        for aid in articles_ids:
            title = articles[aid]['resolved_title']
            if title == "":
                title = articles[aid]['given_title']
            todoist_task['content'] = f"Read \"{title}\""
            todoist_request = requests.post("https://beta.todoist.com/API/v8/tasks",
                                json = todoist_task, headers = todoist_headers)

        return {
            'statusCode': 200,
            'body': json.dumps('Finished updating!')
        }
    else:
        return {
            'statusCode': get_articles.status_code,
            'body': json.dumps(get_articles.content())
        }

