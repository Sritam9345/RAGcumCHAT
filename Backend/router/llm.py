from fastapi import FastAPI, APIRouter, Request


llmRouter = APIRouter()


@llmRouter.post('/chat')
def handleChat(user_input):
    return 'hi'


