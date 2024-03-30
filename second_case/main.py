from fastapi import FastAPI

import json
from llamaapi import LlamaAPI


app = FastAPI(
    title="Генератор поздравлений",
)

data = []