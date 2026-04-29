from router.user import userRouter
from router.rag import ragRouter
from fastapi import FastAPI,WebSocket
import jwt
from dotenv import load_dotenv
import os
from WebSockets.main import RoomManager

app = FastAPI()

load_dotenv()

key = os.getenv('JWT_SECRET')

users = {}
rooms = {}

@app.get('/')
def home():
    return {"message":"Hi there"}

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.headers.get("Authorization", "").replace("Bearer ", "")
    print(token)
    try:
        payload = jwt.decode(token, key, algorithms=["HS256"])
        users[payload['name']]=websocket
        await websocket.accept()
        
        while True:
            response = await websocket.receive_json()
            
            if response['type']=='logout':
                users.pop(response['sender'])
                rooms[response['roomID']].members.pop(response['sender'])
            
            if response['type'] == 'send':
                room = rooms[response['roomID']]
                
                for user in room.members:
                    users[user].send_json({
                        'message':response['message'],
                        'roomID':response['roomID']
                    })
            
            if response['type'] == 'create-room':
                room = RoomManager(response['roomID'])
                room.members.append(response['sender'])
                
                rooms[room['id']] = room
            
            if response['type'] == 'invite':
                users[response['receiver']].send_json({
                    'message':f"{response['sender']} has invited you to join room {response['roomID']}",
                    'roomID':response['roomID']})
            
            if response['type'] == 'join-room':
                rooms[response['roomID']].members.append(response['sender'])
                
            
            await websocket.send_text("hi there")
        

    except Exception as e:
        # users.pop()
        print(e)
        #await websocket.close()


app.include_router(userRouter,prefix='/user')
app.include_router(ragRouter,prefix='/rag')