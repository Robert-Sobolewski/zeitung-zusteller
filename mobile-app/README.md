# mobile-app — Faza 4

Aplikacja mobilna dla dostawcy (1 dostawca = 1 telefon).

## Stack (plan)
- **Expo** + expo-router + EAS Build (standard React Native w 2026)
- **expo-sqlite** — trasa dnia offline (praca w terenie bez zasięgu)
- **Voice**: Vosk (on-device, de-DE, w pełni offline) — "Müller, Hauptstr. 12, BILD, abgang" → NLU → zmiana do outboxa
- Sync z backendem: wzorzec outbox + wersjonowanie (konflikty rozstrzygane po updated_at/version)

## Funkcje docelowe
1. Trasa dnia offline — lista ulic i przystanków
2. Widok "bieżący klient" podczas jazdy: nazwisko, nr domu, lewa/prawa strona, gazeta (ME/OE/BILD/...)
3. Voice input zmian (Zugang/Abgang) bez internetu
4. Sync po powrocie do zasięgu

## Start (Faza 4)
```bash
npx create-expo-app . --template blank-typescript
npm install expo-sqlite react-native-maps
npx expo start
```
