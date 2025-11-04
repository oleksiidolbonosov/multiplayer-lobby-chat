using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using System.Text;

public class ChatClient : MonoBehaviour
{
    public string baseUrl = "http://localhost:8000";

    public IEnumerator SendMessage(string roomId, string sender, string message, System.Action<string> onComplete = null)
    {
        var payload = JsonUtility.ToJson(new { room_id = roomId, sender = sender, message = message });
        using (var req = new UnityWebRequest($"{baseUrl}/chat/send", "POST"))
        {
            byte[] body = Encoding.UTF8.GetBytes(payload);
            req.uploadHandler = new UploadHandlerRaw(body);
            req.downloadHandler = new DownloadHandlerBuffer();
            req.SetRequestHeader("Content-Type", "application/json");
            yield return req.SendWebRequest();
            if (req.result == UnityWebRequest.Result.Success)
            {
                onComplete?.Invoke(req.downloadHandler.text);
            }
            else
            {
                Debug.LogError(req.error);
                onComplete?.Invoke(null);
            }
        }
    }
}
