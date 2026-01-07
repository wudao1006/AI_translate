import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/translate_result.dart';

/// Exception thrown when API call fails
class ApiException implements Exception {
  final String message;
  final int? statusCode;

  ApiException(this.message, {this.statusCode});

  @override
  String toString() => message;
}

/// API client for translation service
class ApiClient {
  final String baseUrl;
  final http.Client _client;

  ApiClient({
    required this.baseUrl,
    http.Client? client,
  }) : _client = client ?? http.Client();

  /// Translate Chinese text to English
  ///
  /// Returns [TranslateResult] with translation and keywords
  /// Throws [ApiException] on error
  Future<TranslateResult> translate(String text) async {
    if (text.trim().isEmpty) {
      throw ApiException('Text cannot be empty');
    }

    final url = Uri.parse('$baseUrl/api/translate');

    try {
      final response = await _client.post(
        url,
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'text': text,
        }),
      ).timeout(
        const Duration(seconds: 30),
        onTimeout: () {
          throw ApiException('Request timeout');
        },
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        return TranslateResult.fromJson(data);
      } else {
        // Try to parse error response
        try {
          final errorData = jsonDecode(response.body) as Map<String, dynamic>;
          final apiError = ApiError.fromJson(errorData);
          throw ApiException(
            apiError.message,
            statusCode: response.statusCode,
          );
        } catch (e) {
          throw ApiException(
            'Translation failed with status ${response.statusCode}',
            statusCode: response.statusCode,
          );
        }
      }
    } on ApiException {
      rethrow;
    } catch (e) {
      throw ApiException('Network error: ${e.toString()}');
    }
  }

  /// Close the HTTP client
  void dispose() {
    _client.close();
  }
}
