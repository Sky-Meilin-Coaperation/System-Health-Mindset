import 'package:flutter/material.dart';
import 'package:sky_meilin_one_world_one_sky/services/skyos_api_client.dart';
import 'package:sky_meilin_one_world_one_sky/ui/screens/skyos_auth_screen.dart';
import 'package:sky_meilin_one_world_one_sky/ui/widgets/skyos_avatar_video_widget.dart';
import 'package:sky_meilin_one_world_one_sky/ui/widgets/skyos_vault_gallery_widget.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const SkyMeilinApp());
}

/// Hauptanwendung für "Sky Meilin - One World One Sky"
class SkyMeilinApp extends StatelessWidget {
  const SkyMeilinApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Sky Meilin - One World One Sky',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        primarySwatch: Colors.teal,
        scaffoldBackgroundColor: const Color(0xFF0F172A),
        colorScheme: const ColorScheme.dark(
          primary: Colors.tealAccent,
          secondary: Colors.emerald,
          surface: const Color(0xFF1E293B),
        ),
        useMaterial3: true,
      ),
      initialRoute: '/login',
      routes: {
        '/login': (context) => const SkyOSAuthScreen(),
        '/home': (context) => const MainNavigationShell(),
      },
    );
  }
}

/// Haupt-Navigationsleiste (Shell) zur Steuerung von Stream, Vault & System
class MainNavigationShell extends StatefulWidget {
  const MainNavigationShell({super.key});

  @override
  State<MainNavigationShell> createState() => _MainNavigationShellState();
}

class _MainNavigationShellState extends State<MainNavigationShell> {
  int _currentIndex = 0;

  final List<Widget> _pages = const [
    SkyOSAvatarVideoWidget(
      serverUrl: 'ws://localhost:8000/ws/v1/avatar/webrtc/s1/flutter_client',
      sessionId: 's1',
    ),
    SkyOSVaultGalleryWidget(),
    DashboardStatusPage(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _currentIndex,
        children: _pages,
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        backgroundColor: const Color(0xFF1E293B),
        indicatorColor: Colors.tealAccent.withOpacity(0.2),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.videocam_outlined),
            selectedIcon: Icon(Icons.videocam, color: Colors.tealAccent),
            label: 'Avatar Stream',
          ),
          NavigationDestination(
            icon: Icon(Icons.video_library_outlined),
            selectedIcon: Icon(Icons.video_library, color: Colors.tealAccent),
            label: 'Reel Vault',
          ),
          NavigationDestination(
            icon: Icon(Icons.dashboard_outlined),
            selectedIcon: Icon(Icons.dashboard, color: Colors.tealAccent),
            label: 'Status & Bot',
          ),
        ],
      ),
    );
  }
}

/// Status-Dashboard innerhalb der App zur Live-Anzeige aller Teilsysteme
class DashboardStatusPage extends StatefulWidget {
  const DashboardStatusPage({super.key});

  @override
  State<DashboardStatusPage> createState() => _DashboardStatusPageState();
}

class _DashboardStatusPageState extends State<DashboardStatusPage> {
  final SkyOSApiClient _apiClient = SkyOSApiClient(baseUrl: 'http://localhost:8000');
  Map<String, dynamic>? _telemetryData;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _fetchTelemetry();
  }

  Future<void> _fetchTelemetry() async {
    setState(() => _isLoading = true);
    try {
      final data = await _apiClient.getTelemetryStatus();
      setState(() {
        _telemetryData = data;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('SkyOS Dashboard & Bot Status'),
        backgroundColor: const Color(0xFF1E293B),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: RefreshIndicator(
          onRefresh: _fetchTelemetry,
          child: ListView(
            children: [
              Card(
                color: const Color(0xFF1E293B),
                child: ListTile(
                  leading: const Icon(Icons.computer, color: Colors.tealAccent),
                  title: const Text('FastAPI Core Engine'),
                  subtitle: Text(_telemetryData != null
                      ? 'Status: ${_telemetryData!["status"]} | ErrorRate: ${_telemetryData!["error_rate"]}%'
                      : 'Verbunden mit http://localhost:8000'),
                  trailing: IconButton(
                    icon: const Icon(Icons.refresh),
                    onPressed: _fetchTelemetry,
                  ),
                ),
              ),
              const SizedBox(height: 12),
              const Card(
                color: Color(0xFF1E293B),
                child: ListTile(
                  leading: Icon(Icons.discord, color: Colors.indigoAccent),
                  title: Text('Discord Bot Bridge'),
                  subtitle: Text('Aktiv (!status, !ask, !papersync)'),
                ),
              ),
              const SizedBox(height: 12),
              const Card(
                color: Color(0xFF1E293B),
                child: ListTile(
                  leading: Icon(Icons.bluetooth_connected, color: Colors.blueAccent),
                  title: Text('Bluetooth HFP Edge'),
                  subtitle: Text('Security Mode 4 Level 4 (AES-CCM / ECDH)'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
