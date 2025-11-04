using System.Collections;
using UnityEngine;
using System;
using System.Threading.Tasks;
using NativeWebSocket;

public class WebSocketClient : MonoBehaviour
{
    private WebSocket websocket;
    public string baseUrl = "ws://localhost:8000/ws/rooms/";

    public async void Connect(string roomId)
    {
        var url = baseUrl + roomId;
        websocket = new WebSocket(url);

        websocket.OnOpen += () => Debug.Log("WS Connected");
        websocket.OnError += (e) => Debug.LogError("WS Error: " + e);
        websocket.OnClose += (e) => Debug.Log("WS Closed");
        websocket.OnMessage += (bytes) => 
        {
            var message = System.Text.Encoding.UTF8.GetString(bytes);
            Debug.Log("WS Message: " + message);
        };

        await websocket.Connect();
    }

    void Update()
    {
        #if !UNITY_WEBGL || UNITY_EDITOR
            websocket?.DispatchMessageQueue();
        #endif
    }

    public async void SendMessage(string message)
    {
        if (websocket?.State == WebSocketState.Open)
            await websocket.SendText(message);
    }

    private async void OnDestroy()
    {
        await websocket?.Close();
    }
}