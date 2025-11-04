using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using System.Text;

public class LobbyClient : MonoBehaviour
{
    public string baseUrl = "http://localhost:8000";

    public IEnumerator CreateRoom(string name, int maxPlayers, System.Action<string> onComplete)
    {
        var payload = JsonUtility.ToJson(new { name = name, max_players = maxPlayers });
        using (var req = new UnityWebRequest($"{baseUrl}/lobby/create", "POST"))
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
