import 'package:flutter/material.dart';
import 'screens/translate_screen.dart';
import 'services/api_client.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // Configure API base URL
    // For development: use your local IP or localhost
    // For production: use your deployed backend URL
    final apiClient = ApiClient(
      baseUrl: 'http://localhost:8000',
      // Or use: 'http://10.0.2.2:8000' for Android emulator
      // Or use: 'http://YOUR_IP:8000' for physical device
    );

    return MaterialApp(
      title: 'AI翻译助手',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
        appBarTheme: const AppBarTheme(
          centerTitle: true,
          elevation: 2,
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            elevation: 2,
          ),
        ),
      ),
      home: TranslateScreen(apiClient: apiClient),
    );
  }
}
