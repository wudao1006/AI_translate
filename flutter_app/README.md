# AI Translation Assistant - Flutter App

Flutter mobile application for AI-powered Chinese to English translation with keyword extraction.

## Features

- Clean, intuitive UI for translation
- Real-time translation using backend API
- Keyword extraction and display
- Error handling with user-friendly messages
- Loading states and visual feedback

## Setup

1. Install Flutter (https://flutter.dev/docs/get-started/install)

2. Install dependencies:
```bash
cd flutter_app
flutter pub get
```

3. Configure API endpoint:
   - Edit `lib/main.dart`
   - Update `baseUrl` in ApiClient:
     - For Android emulator: `http://10.0.2.2:8000`
     - For iOS simulator: `http://localhost:8000`
     - For physical device: `http://YOUR_LOCAL_IP:8000`

4. Ensure backend is running on the configured URL

5. Run the app:
```bash
flutter run
```

## Project Structure

```
lib/
├── main.dart                      # App entry point
├── screens/
│   └── translate_screen.dart      # Main translation screen
├── services/
│   └── api_client.dart            # HTTP API client
└── models/
    └── translate_result.dart      # Data models
```

## API Configuration

The app connects to the backend API. Configure the base URL in `lib/main.dart`:

```dart
final apiClient = ApiClient(
  baseUrl: 'http://YOUR_BACKEND_URL:8000',
);
```

### Development URLs:
- **Android Emulator**: `http://10.0.2.2:8000`
- **iOS Simulator**: `http://localhost:8000`
- **Physical Device**: `http://YOUR_LOCAL_IP:8000`

## Building for Release

### Android
```bash
flutter build apk
# or for split APKs
flutter build apk --split-per-abi
```

### iOS
```bash
flutter build ios
```

## Usage

1. Launch the app
2. Enter Chinese text in the input field
3. Tap the "翻译" (Translate) button
4. View the English translation and extracted keywords
5. The keywords are displayed as chips below the translation

## Error Handling

The app handles various error scenarios:
- Empty input validation
- Network errors
- API errors
- Timeout errors

All errors are displayed with clear messages to the user.

## Dependencies

- `http`: ^1.1.0 - HTTP client for API calls
- `flutter_lints`: ^3.0.0 - Linting rules

## Testing

Run tests:
```bash
flutter test
```

## Platform Support

- Android (API 21+)
- iOS (11.0+)
- Web (with CORS configured on backend)
