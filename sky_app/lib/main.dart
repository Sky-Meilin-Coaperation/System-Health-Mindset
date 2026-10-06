import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const SkyApp());
}

class SkyApp extends StatelessWidget {
  const SkyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Sky Studio',
      theme: ThemeData.dark(useMaterial3: true),
      home: const SkyHomeScreen(),
    );
  }
}

class SkyHomeScreen extends StatefulWidget {
  const SkyHomeScreen({super.key});

  @override
  State<SkyHomeScreen> createState() => _SkyHomeScreenState();
}

class _SkyHomeScreenState extends State<SkyHomeScreen> {
  final TextEditingController _controller = TextEditingController();
  String _response = 'Bereit für Eingaben...';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Sky Studio Interface'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              decoration: const InputDecoration(
                labelText: 'Prompt / Befehl eingeben...',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: () async {
                setState(() {
                  _response = 'Sende Anfrage an LM Studio...';
                });

                try {
                  final response = await http.post(
                    Uri.parse('http://localhost:1234/v1/chat/completions'),
                    headers: {'Content-Type': 'application/json'},
                    body: jsonEncode({
                      "model": "mistralai/ministral-3-3b",
                      "messages": [
                        {"role": "user", "content": _controller.text}
                      ],
                      "temperature": 0.7
                    }),
                  );

                  if (response.statusCode == 200) {
                    final data = jsonDecode(response.body);
                    setState(() {
                      _response = data['choices'][0]['message']['content'];
                    });
                  } else {
                    setState(() {
                      _response = 'Fehler: ${response.statusCode}';
                    });
                  }
                } catch (e) {
                  setState(() {
                    _response = 'Verbindungsfehler: $e\n(Läuft LM Studio?)';
                  });
                }
              },
              child: const Text('Anfragen'),
            ),
            const SizedBox(height: 24),
            Expanded(
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.black26,
                  border: Border.all(color: Colors.white24),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: SingleChildScrollView(
                  child: Text(_response),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}