import React from "react";
import { SafeAreaView, StatusBar, StyleSheet, Text, View } from "react-native";
import { WebView } from "react-native-webview";

const APP_URL = process.env.EXPO_PUBLIC_APP_URL;

export default function App() {
  return (
    <SafeAreaView style={styles.root}>
      <StatusBar barStyle="light-content" backgroundColor="#080B14" />
      {APP_URL ? (
        <WebView source={{ uri: APP_URL }} style={styles.webview} javaScriptEnabled domStorageEnabled />
      ) : (
        <View style={styles.center}>
          <Text style={styles.eyebrow}>ULTIMA · UNIFY</Text>
          <Text style={styles.title}>Dein zentraler Workspace</Text>
          <Text style={styles.copy}>Die App-Oberfläche ist vorbereitet. Sobald die sichere Render-Adresse eingerichtet ist, wird sie hier verbunden.</Text>
        </View>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: "#080B14" },
  webview: { flex: 1, backgroundColor: "#080B14" },
  center: { flex: 1, padding: 28, justifyContent: "center" },
  eyebrow: { color: "#D7B76A", letterSpacing: 4, fontSize: 12, marginBottom: 18 },
  title: { color: "#F5F2EA", fontSize: 30, fontWeight: "700", marginBottom: 14 },
  copy: { color: "#A8B0C0", fontSize: 16, lineHeight: 24 }
});
