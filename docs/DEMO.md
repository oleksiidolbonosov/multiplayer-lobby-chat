# Demo instructions

1. Start stack: docker-compose up --build
2. Open API docs: http://localhost:8000/docs
3. Create a room (POST /lobby/create) via Swagger or curl
4. Open Unity project, import UnityClient folder into Assets, attach scripts and call methods:
   - Create room using LobbyClient.CreateRoom coroutine
   - Start WebSocketClient.Connect(roomId) to see messages
   - Use ChatClient.SendMessage to send messages which are broadcast to websocket clients
