import json
from src.core.response import return_success


def index(event, context):
    params = event.get('body', 'hello')

    print(event)
    print(context)
    return return_success(params)
