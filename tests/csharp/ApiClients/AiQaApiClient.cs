using System.Threading.Tasks;
using RestSharp;

namespace csharp.ApiClients
{
    /// <summary>
    /// API Client for communicating with the AI-QA Python REST API.
    /// API-Client für die Kommunikation mit der AI-QA Python REST-API.
    /// </summary>
    public class AiQaApiClient
    {
        private readonly RestClient _client;
        private const string BaseUrl = "http://127.0.0.1:8000";

        public AiQaApiClient()
        {
            _client = new RestClient(BaseUrl);
        }

        public async Task<RestResponse> GetLatestMetricsAsync()
        {
            var request = new RestRequest("/metrics/latest", Method.Get);
            return await _client.ExecuteAsync(request);
    }

        public async Task<RestResponse> EvaluateDriftAsync(object payload)
        {
            var request = new RestRequest("/evaluate/drift", Method.Post);
            request.AddJsonBody(payload);
            return await _client.ExecuteAsync(request);
        }

        public async Task<RestResponse> EvaluateForgettingAsync(object payload)
        {
            var request = new RestRequest("/evaluate/forgetting", Method.Post);
            request.AddJsonBody(payload);
            return await _client.ExecuteAsync(request);
        }
    }
}