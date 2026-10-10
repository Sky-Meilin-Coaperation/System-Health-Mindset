import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

/// Exception class for SkyOS API errors.
class SkyOSApiException implements Exception {
  final int statusCode;
  final String message;

  SkyOSApiException(this.statusCode, this.message);

  @override
  String toString() => 'SkyOSApiException [$statusCode]: $message';
}

/// Model for Telemetry and System Metrics.
class SystemTelemetry {
  final String timestamp;
  final String metrics;
  final double errorRate;
  final String status;

  SystemTelemetry({
    required this.timestamp,
    required this.metrics,
    required this.errorRate,
    required this.status,
  });

  factory SystemTelemetry.fromJson(Map<String, dynamic> json) {
    return SystemTelemetry(
      timestamp: json['timestamp'] ?? '',
      metrics: json['metrics'] ?? '',
      errorRate: (json['error_rate'] ?? 0.0).toDouble(),
      status: json['status'] ?? 'unknown',
    );
  }
}

/// Model for SkyAI Knowledge Base queries (L0-L4 Context Tiers).
class KnowledgeQueryResponse {
  final String tier;
  final String query;
  final List<dynamic> results;

  KnowledgeQueryResponse({
    required this.tier,
    required this.query,
    required this.results,
  });

  factory KnowledgeQueryResponse.fromJson(Map<String, dynamic> json) {
    return KnowledgeQueryResponse(
      tier: json['tier'] ?? 'L0_Raw',
      query: json['query'] ?? '',
      results: json['results'] ?? [],
    );
  }
}

/// Main Service Client for communicating with the SkyOS FastAPI Backend (Port 8000).
class SkyOSFastApiClient {
  final String baseUrl;
  final http.Client _httpClient;
  String? _authToken;

  SkyOSFastApiClient({
    this.baseUrl = 'http://localhost:8000',
    http.Client? httpClient,
  }) : _httpClient = httpClient ?? http.Client();

  /// Set Auth Token securely (e.g. retrieved from FlutterSecureStorage)
  void setAuthToken(String token) {
    _authToken = token;
  }

  /// Helper to construct standard headers
  Map<String, String> _buildHeaders() {
    final headers = <String, String>{
      HttpHeaders.contentTypeHeader: 'application/json',
      HttpHeaders.acceptHeader: 'application/json',
    };
    if (_authToken != null && _authToken!.isNotEmpty) {
      headers[HttpHeaders.authorizationHeader] = 'Bearer $_authToken';
    }
    return headers;
  }

  /// 1. Fetch System Telemetry & Health Status
  Future<SystemTelemetry> getSystemTelemetry() async {
    final url = Uri.parse('$baseUrl/api/v1/telemetry');
    final response = await _httpClient.get(url, headers: _buildHeaders());

    if (response.statusCode == 200) {
      final jsonBody = jsonDecode(response.body) as Map<String, dynamic>;
      return SystemTelemetry.fromJson(jsonBody);
    } else {
      throw SkyOSApiException(
        response.statusCode,
        'Fehler beim Abrufen der Telemetriedaten: ${response.body}',
      );
    }
  }

  /// 2. Query SkyAI Knowledge System across L0-L4 Tiers
  Future<KnowledgeQueryResponse> queryKnowledgeBase({
    required String query,
    String tier = 'L4_Organized',
  }) async {
    final url = Uri.parse('$baseUrl/api/v1/knowledge/query');
    final body = jsonEncode({
      'query': query,
      'tier': tier,
    });

    final response = await _httpClient.post(
      url,
      headers: _buildHeaders(),
      body: body,
    );

    if (response.statusCode == 200) {
      final jsonBody = jsonDecode(response.body) as Map<String, dynamic>;
      return KnowledgeQueryResponse.fromJson(jsonBody);
    } else {
      throw SkyOSApiException(
        response.statusCode,
        'Fehler bei der Knowledge-Base-Anfrage: ${response.body}',
      );
    }
  }

  /// 3. Trigger n8n Automation Webhook via FastAPI Relay
  Future<bool> triggerWorkflow(String workflowId, Map<String, dynamic> payload) async {
    final url = Uri.parse('$baseUrl/api/v1/workflows/$workflowId/trigger');
    final response = await _httpClient.post(
      url,
      headers: _buildHeaders(),
      body: jsonEncode(payload),
    );

    if (response.statusCode == 200 || response.statusCode == 202) {
      return true;
    } else {
      throw SkyOSApiException(
        response.statusCode,
        'Fehler beim Auslösen des Workflows $workflowId: ${response.body}',
      );
    }
  }

  /// Close HTTP client session
  void dispose() {
    _httpClient.close();
  }
}

