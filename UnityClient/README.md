# Unity Client - Lobby + Chat Demo

Import `UnityClient` folder into your Unity project's `Assets/` directory.

Demo scripts included:
- LobbyClient.cs — create/list/join/leave rooms
- ChatClient.cs — send chat messages via REST
- WebSocketClient.cs — subscribe to room WebSocket and receive live messages

Usage:
1. Create an empty GameObject and attach these scripts.
2. Set Base Url (default http://localhost:8000)
3. Call coroutines from another MonoBehaviour (examples included)

See example usage snippets in each script's header.
