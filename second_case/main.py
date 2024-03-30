import uvicorn
from fastapi import FastAPI, Form
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

import json
from llamaapi import LlamaAPI
from config import TOKEN

from googletrans import Translator

translator = Translator()

app = FastAPI(
    title="Генератор поздравлений",
)

templates = Jinja2Templates(directory='templates')

llama = LlamaAPI(TOKEN)


def make_congratulation(person_name: str):

    name = person_name
    print(name)
    name = translator.translate(f'{name}', dest='en').text
    print(name)
    content = f"Congratulate me on my birthday and wish something, my name is {name}"

    api_request_json = {
        'model': 'llama-13b-chat',
        'functions': [
            {
                "name": "congratulation",
                "description": "Get congratulation with Happy Birthday",
                "parameters": {
                              "type": "object",
                              "properties": {
                                  "question": {
                                      "type": "string",
                                      'description': 'Congratulate with birthday'
                                  },
                              },
                },
            }
        ],
        'function_call': {'name': 'congratulation'},
        "stream": False,
        'messages': [
            {'role': 'user', 'content': content}],
    }
    try:
        response = llama.run(api_request_json)
        print(response.json()['choices'][0]['message'])
        try:
            answer = response.json()['choices'][0]['message']['function_call']['arguments']['question']
        except:
            answer = response.json()['choices'][0]['message']['function_call']['arguments']['question']["description"]
        result = translator.translate(f'{answer}', src='en', dest='ru').text
        print(result)
        return result
    except Exception as e:
        return False


@app.get('/', tags=['Main'])
def index(request: Request):
    return templates.TemplateResponse('base.html', {'request': request, 'result': ''})


@app.post('/', tags=['Main'])
def index(request: Request, name: str = Form()):
    result = make_congratulation(name)
    return templates.TemplateResponse('base.html', {'request': request, 'result': result})


if __name__ == '__main__':
    uvicorn.run('main:app')

