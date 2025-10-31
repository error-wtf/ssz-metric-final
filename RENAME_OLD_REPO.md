# Altes Repo auf Privat schalten & Neues erstellen

## Schritt 1: Altes Repo auf Privat schalten

1. Gehe zu: https://github.com/error-wtf/ssz-full-metric
2. Klicke: **Settings** (oben rechts)
3. Scrolle nach unten zu: **Danger Zone**
4. Klicke: **Change visibility**
5. Wähle: **Make private**
6. Bestätige

## Schritt 2: Neues Repo erstellen

1. Gehe zu: https://github.com/new
2. Name: **perfect-ssz-metric**
3. Description: **Perfect SSZ Metric Implementation - 100% Validated**
4. **Public** ✓
5. NICHTS anhaken!
6. Create repository

## Schritt 3: Push zu neuem Repo

Dann führe aus:
```powershell
cd E:\clone\ssz-full-metric
git remote remove origin
git remote add origin https://github.com/error-wtf/perfect-ssz-metric.git
git push -u origin master
git tag -a v1.0.0 -m "Perfect SSZ Metric v1.0.0"
git push origin v1.0.0
```

FERTIG!
