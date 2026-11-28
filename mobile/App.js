import React, { useEffect, useMemo, useRef, useState } from "react";
import { SafeAreaView, StatusBar, StyleSheet, Text, View, Pressable, TextInput, ScrollView, Linking } from "react-native";
import { WebView } from "react-native-webview";
import AsyncStorage from "@react-native-async-storage/async-storage";
import PROJECT_CATALOG from "./project_catalog.json";

const PORTAL = process.env.EXPO_PUBLIC_APP_URL || "https://ultima-central-45ne.onrender.com/";
const QUICK = PROJECT_CATALOG;
const CATS = ["ALLE", "ZENTRAL", "KI", "SICHERHEIT", "KREATIV", "MEDIA", "FINANZEN", "GAMES", "SHOPS", "PROJEKTE", "CODE"];
const COLORS = { bg: "#080B14", panel: "#121A2B", line: "#27334A", gold: "#E8C783", cyan: "#66DED8", muted: "#9DAAC0", white: "#F5F4F0" };

export default function App() {
  const [tab, setTab] = useState("home");
  const [activeUrl, setActiveUrl] = useState(PORTAL);
  const [activeTitle, setActiveTitle] = useState("ULTIMA Central");
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("ALLE");
  const [loading, setLoading] = useState(false);
  const [favorites, setFavorites] = useState([]);
  const [recentUrls, setRecentUrls] = useState([]);
  const [storageReady, setStorageReady] = useState(false);
  const web = useRef(null);
  useEffect(() => { AsyncStorage.multiGet(["ultima-one:favorites", "ultima-one:recent"]).then(values => { const f = values[0][1]; const r = values[1][1]; if (f) setFavorites(JSON.parse(f)); if (r) setRecentUrls(JSON.parse(r)); }).catch(() => {}).finally(() => setStorageReady(true)); }, []);
  useEffect(() => { if (storageReady) AsyncStorage.multiSet([["ultima-one:favorites", JSON.stringify(favorites)], ["ultima-one:recent", JSON.stringify(recentUrls)]]).catch(() => {}); }, [favorites, recentUrls, storageReady]);
  const toggleFavorite = (url) => setFavorites(current => current.includes(url) ? current.filter(item => item !== url) : [...current, url]);
  const projects = useMemo(() => QUICK.filter(p => (category === "ALLE" || p.group === category) && (p.title + p.subtitle).toLowerCase().includes(query.toLowerCase())), [category, query]);
  const favoriteProjects = useMemo(() => QUICK.filter(p => favorites.includes(p.url)), [favorites]);
  const recentProjects = useMemo(() => recentUrls.map(url => QUICK.find(p => p.url === url)).filter(Boolean), [recentUrls]);
  const openProject = (p) => { setActiveTitle(p.title); setActiveUrl(p.url); setRecentUrls(current => [p.url, ...current.filter(url => url !== p.url)].slice(0, 8)); setTab("web"); };
  const openPortal = () => { setActiveTitle("ULTIMA Central"); setActiveUrl(PORTAL); setTab("web"); };
  const openExternal = async (url) => { try { await Linking.openURL(url); } catch (_) {} };

  return (
    <SafeAreaView style={s.root}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.bg} />
      <View style={s.header}>
        <View><Text style={s.brand}>✧ ULTIMA ONE</Text><Text style={s.tagline}>ONE ENTRY POINT · MANY PROJECTS</Text></View>
        <View style={s.live}><View style={s.dot}/><Text style={s.liveText}>HUB</Text></View>
      </View>
      {tab === "web" ? (
        <View style={s.webWrap}>
          <View style={s.webBar}><Pressable onPress={() => setTab("home")} style={s.back}><Text style={s.backText}>‹  HUB</Text></Pressable><Text numberOfLines={1} style={s.webTitle}>{activeTitle}</Text><Pressable onPress={() => web.current?.reload()}><Text style={s.openText}>↻</Text></Pressable><Pressable onPress={() => openExternal(activeUrl)}><Text style={s.openText}>↗</Text></Pressable></View>
          {loading && <View style={s.loading}><Text style={s.loadingText}>ULTIMA wird geladen …</Text></View>}
          <WebView ref={web} source={{ uri: activeUrl }} style={s.webview} javaScriptEnabled domStorageEnabled sharedCookiesEnabled thirdPartyCookiesEnabled setSupportMultipleWindows={false} onLoadStart={() => setLoading(true)} onLoadEnd={() => setLoading(false)} onError={() => setLoading(false)} onShouldStartLoadWithRequest={(request) => { if (request.url.startsWith("https://") || request.url.startsWith("http://")) return true; return false; }} pullToRefreshEnabled />
        </View>
      ) : (
        <ScrollView contentContainerStyle={s.content}>
          <View style={s.hero}><Text style={s.eyebrow}>DEIN DIGITALES KONTROLLZENTRUM</Text><Text style={s.heroTitle}>Was möchtest du{"\n"}heute verwalten?</Text><Text style={s.heroCopy}>Websites, Apps, KI-Systeme und Projekte – zentral erreichbar in einer iOS-App.</Text><Pressable onPress={openPortal} style={s.heroButton}><Text style={s.heroButtonText}>ULTIMA CENTRAL ÖFFNEN  ↗</Text></Pressable></View>
          <View style={s.stats}><View style={s.stat}><Text style={s.statNumber}>76</Text><Text style={s.statLabel}>Render-Services laut Inventar</Text></View><View style={s.stat}><Text style={s.statNumber}>44</Text><Text style={s.statLabel}>GitHub-Repositories im Inventar</Text></View></View>
          {favoriteProjects.length > 0 && <><View style={s.sectionHead}><Text style={s.sectionTitle}>Deine Favoriten</Text><Text style={s.sectionHint}>Lokal auf diesem Gerät gespeichert</Text></View>{favoriteProjects.map(p => <View key={"fav-"+p.url} style={s.projectRow}><Pressable style={s.projectMain} onPress={() => openProject(p)}><Text style={s.projectName}>{p.title}</Text><Text style={s.projectDesc}>{p.subtitle}</Text></Pressable><Pressable onPress={() => toggleFavorite(p.url)} style={s.favoriteButton}><Text style={s.favoriteOn}>★</Text></Pressable></View>)}</>}
          {recentProjects.length > 0 && <><View style={s.sectionHead}><Text style={s.sectionTitle}>Zuletzt geöffnet</Text></View>{recentProjects.slice(0,4).map(p => <Pressable key={"recent-"+p.url} onPress={() => openProject(p)} style={s.projectRow}><View style={s.projectInfo}><Text style={s.projectName}>{p.title}</Text><Text style={s.projectDesc}>{p.subtitle}</Text></View><Text style={s.chevron}>›</Text></Pressable>)}</>}
          <View style={s.sectionHead}><Text style={s.sectionTitle}>Schnellzugriff</Text><Text style={s.sectionHint}>Ausgewählte zentrale Dienste</Text></View>
          <View style={s.quickGrid}>{QUICK.slice(0,4).map(p => <Pressable key={p.title} onPress={() => openProject(p)} style={s.quickCard}><Text style={s.cardIcon}>{p.group === "KI" ? "✦" : p.group === "FINANZEN" ? "₿" : p.group === "MEDIA" ? "▣" : "◈"}</Text><Text style={s.cardTitle}>{p.title}</Text><Text style={s.cardSub}>{p.subtitle}</Text><Text style={s.cardLink}>ÖFFNEN ↗</Text></Pressable>)}</View>
          <View style={s.sectionHead}><Text style={s.sectionTitle}>Alle Programme & Repositories</Text><Text style={s.sectionHint}>Katalog durchsuchen</Text></View>
          <TextInput value={query} onChangeText={setQuery} placeholder="Projekt suchen …" placeholderTextColor="#71809B" style={s.search} autoCapitalize="none" />
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={s.chips}>{CATS.map(c => <Pressable key={c} onPress={() => setCategory(c)} style={[s.chip, category === c && s.chipActive]}><Text style={[s.chipText, category === c && s.chipTextActive]}>{c}</Text></Pressable>)}</ScrollView>
          {projects.map(p => <View key={p.url} style={s.projectRow}><Pressable onPress={() => openProject(p)} style={s.projectMain}><View style={s.projectGlyph}><Text style={s.projectGlyphText}>{p.type === "repository" ? "⌘" : "✧"}</Text></View><View style={s.projectInfo}><Text style={s.projectName}>{p.title}</Text><Text style={s.projectDesc}>{p.subtitle}</Text></View></Pressable><Pressable onPress={() => toggleFavorite(p.url)} style={s.favoriteButton}><Text style={favorites.includes(p.url) ? s.favoriteOn : s.favoriteOff}>{favorites.includes(p.url) ? "★" : "☆"}</Text></Pressable></View>)}
          <View style={s.notice}><Text style={s.noticeTitle}>Sicherer Zugang</Text><Text style={s.noticeCopy}>Die App öffnet die bestehenden Dienste über ihre jeweiligen sicheren Anmeldungen. Shop-Systeme und Rothshild bleiben getrennt. Zahlungen, Wallet-Transaktionen und administrative Änderungen werden nicht ohne Bestätigung ausgeführt.</Text></View>
          <Text style={s.footer}>ULTIMA ONE · iOS COMMAND CENTER · v1.2</Text>
        </ScrollView>
      )}
      <View style={s.tabbar}>
        <Pressable onPress={() => setTab("home")} style={s.tab}><Text style={[s.tabIcon, tab === "home" && s.tabSelected]}>⌂</Text><Text style={[s.tabLabel, tab === "home" && s.tabSelected]}>Start</Text></Pressable>
        <Pressable onPress={openPortal} style={s.tab}><Text style={s.tabIcon}>◈</Text><Text style={s.tabLabel}>Central</Text></Pressable>
        <Pressable onPress={() => {setTab("home");setCategory("KI");}} style={s.tab}><Text style={s.tabIcon}>✦</Text><Text style={s.tabLabel}>KI-Center</Text></Pressable>
        <Pressable onPress={() => openExternal("https://github.com/gaussa72-boop/Unify-App")} style={s.tab}><Text style={s.tabIcon}>⌘</Text><Text style={s.tabLabel}>GitHub</Text></Pressable>
      </View>
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
 root:{flex:1,backgroundColor:COLORS.bg},header:{height:68,paddingHorizontal:20,flexDirection:"row",alignItems:"center",justifyContent:"space-between",borderBottomWidth:1,borderColor:COLORS.line},brand:{color:COLORS.gold,fontSize:19,fontWeight:"800",letterSpacing:2},tagline:{color:COLORS.muted,fontSize:8,letterSpacing:2,marginTop:4},live:{flexDirection:"row",alignItems:"center",gap:6,borderWidth:1,borderColor:"#3D8D79",borderRadius:20,paddingHorizontal:10,paddingVertical:6},dot:{width:6,height:6,borderRadius:4,backgroundColor:"#54D69B"},liveText:{color:"#A4E8C7",fontSize:9,letterSpacing:1},content:{padding:18,paddingBottom:30},hero:{paddingVertical:28},eyebrow:{color:COLORS.cyan,fontSize:9,letterSpacing:2.5,fontWeight:"700"},heroTitle:{color:COLORS.white,fontSize:34,lineHeight:40,fontWeight:"800",marginTop:15},heroCopy:{color:COLORS.muted,fontSize:14,lineHeight:22,marginTop:12},heroButton:{alignSelf:"flex-start",backgroundColor:COLORS.gold,paddingHorizontal:17,paddingVertical:13,borderRadius:9,marginTop:20},heroButtonText:{color:"#17131A",fontSize:10,fontWeight:"900",letterSpacing:1},stats:{flexDirection:"row",gap:10,marginBottom:30},stat:{flex:1,backgroundColor:COLORS.panel,borderWidth:1,borderColor:COLORS.line,borderRadius:12,padding:15},statNumber:{color:COLORS.gold,fontSize:24,fontWeight:"800"},statLabel:{color:COLORS.muted,fontSize:10,marginTop:5},sectionHead:{marginBottom:13,marginTop:8},sectionTitle:{color:COLORS.white,fontSize:19,fontWeight:"700"},sectionHint:{color:COLORS.muted,fontSize:10,marginTop:4},quickGrid:{flexDirection:"row",flexWrap:"wrap",gap:10,marginBottom:27},quickCard:{width:"48%",flexGrow:1,backgroundColor:COLORS.panel,borderWidth:1,borderColor:COLORS.line,borderRadius:12,padding:14,minHeight:140},cardIcon:{color:COLORS.cyan,fontSize:20},cardTitle:{color:COLORS.white,fontSize:13,fontWeight:"700",marginTop:10},cardSub:{color:COLORS.muted,fontSize:10,marginTop:5},cardLink:{color:COLORS.gold,fontSize:9,fontWeight:"800",marginTop:13,letterSpacing:1},search:{backgroundColor:COLORS.panel,borderColor:COLORS.line,borderWidth:1,borderRadius:9,padding:12,color:COLORS.white,marginBottom:10},chips:{gap:7,paddingBottom:12},chip:{paddingHorizontal:12,paddingVertical:8,borderRadius:20,borderWidth:1,borderColor:COLORS.line},chipActive:{borderColor:COLORS.gold,backgroundColor:"#E8C78318"},chipText:{color:COLORS.muted,fontSize:9,fontWeight:"700"},chipTextActive:{color:COLORS.gold},projectRow:{flexDirection:"row",alignItems:"center",paddingVertical:13,borderBottomWidth:1,borderColor:COLORS.line},projectMain:{flex:1,flexDirection:"row",alignItems:"center"},favoriteButton:{paddingHorizontal:12,paddingVertical:8},favoriteOn:{color:COLORS.gold,fontSize:19},favoriteOff:{color:COLORS.muted,fontSize:19},projectGlyph:{width:36,height:36,borderRadius:10,backgroundColor:"#66DED817",alignItems:"center",justifyContent:"center"},projectGlyphText:{color:COLORS.cyan,fontSize:17},projectInfo:{flex:1,marginLeft:12},projectName:{color:COLORS.white,fontSize:12,fontWeight:"700"},projectDesc:{color:COLORS.muted,fontSize:10,marginTop:4},chevron:{color:COLORS.gold,fontSize:24,paddingHorizontal:8},notice:{borderWidth:1,borderColor:"#D6B66C55",backgroundColor:"#D6B66C0D",borderRadius:11,padding:14,marginTop:24},noticeTitle:{color:COLORS.gold,fontSize:12,fontWeight:"800"},noticeCopy:{color:COLORS.muted,fontSize:10,lineHeight:16,marginTop:6},footer:{color:"#68758E",fontSize:8,letterSpacing:1,textAlign:"center",marginTop:24},tabbar:{height:62,backgroundColor:"#0C1220",borderTopWidth:1,borderColor:COLORS.line,flexDirection:"row",justifyContent:"space-around",alignItems:"center"},tab:{alignItems:"center",justifyContent:"center",minWidth:55},tabIcon:{color:COLORS.muted,fontSize:20},tabLabel:{color:COLORS.muted,fontSize:8,marginTop:2},tabSelected:{color:COLORS.gold},webWrap:{flex:1},webBar:{height:44,flexDirection:"row",alignItems:"center",paddingHorizontal:15,borderBottomWidth:1,borderColor:COLORS.line},back:{padding:5},backText:{color:COLORS.gold,fontWeight:"700",fontSize:11},webTitle:{color:COLORS.white,flex:1,textAlign:"center",fontSize:12},openText:{color:COLORS.cyan,fontSize:18,padding:5},webview:{flex:1,backgroundColor:COLORS.bg},loading:{padding:8,backgroundColor:COLORS.panel},loadingText:{color:COLORS.gold,fontSize:10,textAlign:"center"}
});
