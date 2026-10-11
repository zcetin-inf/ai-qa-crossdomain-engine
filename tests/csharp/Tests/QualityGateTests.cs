using System.Net;
using System.Threading.Tasks;
using csharp.ApiClients;
using Newtonsoft.Json.Linq;
using Xunit;

namespace csharp.Tests
{
    /// <summary>
    /// Integration tests for Quality Gates (Model Drift & Catastrophic Forgetting).
    /// Integrationstests für Quality Gates (Modell-Drift & Catastrophic Forgetting).
    /// </summary>
    public class QualityGateTests
    {
        private readonly AiQaApiClient _apiClient;

        public QualityGateTests()
        {
            _apiClient = new AiQaApiClient();
        }

        [Fact]
        public async Task TestModelDrift_ShouldReturnStable_WhenDataIsSimilar()
        {
           // 1. Fetching current test data from the central API / Aktuelle Testdaten von der zentralen API abrufen
            var configResponse = await _apiClient.GetLatestMetricsAsync();
            Assert.Equal(HttpStatusCode.OK, configResponse.StatusCode);
            
            var configJson = JObject.Parse(configResponse.Content!);
            var driftTestCfg = configJson["data"]?["drift_test"];

            // 2. Dynamically mapping central data into the payload / Zentrale Daten dynamisch in das Payload übertragen
            var payload = new
            {
                baseline_data = driftTestCfg!["baseline_data"]!.ToObject<double[]>(),
                current_data = driftTestCfg!["current_data"]!.ToObject<double[]>(),
                threshold = driftTestCfg!["threshold"]!.Value<double>()
            };

            var response = await _apiClient.EvaluateDriftAsync(payload);

            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
            
            var jsonResponse = JObject.Parse(response.Content!);
            Assert.Equal("STABLE", jsonResponse["status"]?.ToString());
            Assert.False((bool)jsonResponse["drift_detected"]!);
        }

        [Fact]
        public async Task TestCatastrophicForgetting_ShouldPass_WhenDropIsWithinLimits()
        {
           // 1. Fetching current test data from the central API / Aktuelle Testdaten von der zentralen API abrufen
            var configResponse = await _apiClient.GetLatestMetricsAsync();
            Assert.Equal(HttpStatusCode.OK, configResponse.StatusCode);
            
            var configJson = JObject.Parse(configResponse.Content!);
            var forgettingTestCfg = configJson["data"]?["forgetting_test"];

            // 2. Dynamically mapping central data into the payload / Zentrale Daten dynamisch in das Payload übertragen
            var payload = new
            {
                baseline_accuracy = forgettingTestCfg!["baseline_accuracy"]!.Value<double>(),
                current_accuracy = forgettingTestCfg!["current_accuracy"]!.Value<double>(),
                max_allowed_drop = forgettingTestCfg!["max_allowed_drop"]!.Value<double>()
            };

            var response = await _apiClient.EvaluateForgettingAsync(payload);

            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
            
            var jsonResponse = JObject.Parse(response.Content!);
            Assert.Equal("PASSED", jsonResponse["status"]?.ToString());
            Assert.False((bool)jsonResponse["catastrophic_forgetting_detected"]!);
        }
    }
}