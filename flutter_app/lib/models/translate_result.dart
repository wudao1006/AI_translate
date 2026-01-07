/// Data model for translation results.
class TranslateResult {
  final String translation;
  final List<String> keywords;

  TranslateResult({
    required this.translation,
    required this.keywords,
  });

  /// Create TranslateResult from JSON response
  factory TranslateResult.fromJson(Map<String, dynamic> json) {
    return TranslateResult(
      translation: json['translation'] as String,
      keywords: (json['keywords'] as List<dynamic>)
          .map((e) => e.toString())
          .toList(),
    );
  }

  /// Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'translation': translation,
      'keywords': keywords,
    };
  }
}

/// Error response model
class ApiError {
  final String code;
  final String message;

  ApiError({
    required this.code,
    required this.message,
  });

  factory ApiError.fromJson(Map<String, dynamic> json) {
    final errorData = json['error'] as Map<String, dynamic>;
    return ApiError(
      code: errorData['code'] as String,
      message: errorData['message'] as String,
    );
  }

  @override
  String toString() => message;
}
