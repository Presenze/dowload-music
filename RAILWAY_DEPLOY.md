# 🚀 Deploy su Railway - Giglio Download Bot

## 📋 **Preparazione Pre-Deploy:**

### 1️⃣ **Rimuovi Token dal Codice:**
```bash
# Il token è già stato rimosso da config.py
# Ora usa solo variabili d'ambiente
```

### 2️⃣ **File Creati per Railway:**
- ✅ `railway.json` - Configurazione Railway
- ✅ `Procfile` - Comando di avvio
- ✅ `runtime.txt` - Versione Python
- ✅ `railway.toml` - Configurazione avanzata
- ✅ `.gitignore` - Esclude file sensibili

---

## 🚀 **Deploy su Railway:**

### **Metodo 1: Deploy da GitHub (Raccomandato)**

#### 1️⃣ **Prepara il Repository:**
```bash
# Inizializza git se non l'hai fatto
git init

# Aggiungi tutti i file
git add .

# Commit iniziale
git commit -m "Initial commit - Giglio Download Bot"

# Crea repository su GitHub
# Vai su github.com e crea un nuovo repository
# NON includere il token nel repository!
```

#### 2️⃣ **Deploy su Railway:**
1. Vai su [railway.app](https://railway.app)
2. Fai login con GitHub
3. Clicca "New Project"
4. Scegli "Deploy from GitHub repo"
5. Seleziona il tuo repository
6. Railway clonerà automaticamente il codice

#### 3️⃣ **Configura Variabili d'Ambiente:**
1. Vai nella dashboard del progetto
2. Clicca su "Variables"
3. Aggiungi le variabili:
   ```
   BOT_TOKEN = 7576082688:AAGJz-v5NG8QGKCezBA5qlhI3lYiatsgRd8
   DOWNLOAD_DIR = downloads
   MAX_FILE_SIZE = 52428800
   ```

#### 4️⃣ **Avvia il Deploy:**
1. Clicca "Deploy"
2. Railway installerà le dipendenze automaticamente
3. Il bot si avvierà automaticamente

---

### **Metodo 2: Deploy da File Locali**

#### 1️⃣ **Installa Railway CLI:**
```bash
# Windows (PowerShell)
iwr https://railway.app/install.ps1 -useb | iex

# Linux/Mac
curl -fsSL https://railway.app/install.sh | sh
```

#### 2️⃣ **Login e Deploy:**
```bash
# Login
railway login

# Inizializza progetto
railway init

# Aggiungi variabili d'ambiente
railway variables set BOT_TOKEN=7576082688:AAGJz-v5NG8QGKCezBA5qlhI3lYiatsgRd8
railway variables set DOWNLOAD_DIR=downloads
railway variables set MAX_FILE_SIZE=52428800

# Deploy
railway up
```

---

## ⚙️ **Configurazione Avanzata:**

### **Variabili d'Ambiente Necessarie:**
```bash
BOT_TOKEN=7576082688:AAGJz-v5NG8QGKCezBA5qlhI3lYiatsgRd8
DOWNLOAD_DIR=downloads
MAX_FILE_SIZE=52428800
PORT=8000
```

### **Configurazione Nixpacks:**
Railway userà automaticamente `requirements.txt` per installare le dipendenze Python.

### **Logs e Monitoraggio:**
```bash
# Vedi logs in tempo reale
railway logs

# Vedi status del servizio
railway status
```

---

## 🔧 **Risoluzione Problemi:**

### **Problema: Bot non si avvia**
```bash
# Controlla logs
railway logs

# Verifica variabili d'ambiente
railway variables

# Riavvia il servizio
railway redeploy
```

### **Problema: Dipendenze non installate**
```bash
# Verifica requirements.txt
cat requirements.txt

# Forza reinstallazione
railway redeploy --detach
```

### **Problema: Token non valido**
```bash
# Verifica token
railway variables get BOT_TOKEN

# Aggiorna token
railway variables set BOT_TOKEN=NUOVO_TOKEN
```

---

## 📊 **Monitoraggio:**

### **Dashboard Railway:**
- Vai su [railway.app/dashboard](https://railway.app/dashboard)
- Seleziona il tuo progetto
- Monitora CPU, RAM, e logs

### **Metriche Importanti:**
- **CPU Usage** - Dovrebbe essere basso
- **Memory Usage** - Dovrebbe essere stabile
- **Uptime** - Dovrebbe essere 100%
- **Logs** - Controlla errori

---

## 💰 **Costi Railway:**

### **Piano Gratuito:**
- ✅ 500 ore di esecuzione/mese
- ✅ 1GB RAM
- ✅ 1GB storage
- ✅ Deploy illimitati

### **Piano Pro ($5/mese):**
- ✅ Esecuzione illimitata
- ✅ 8GB RAM
- ✅ 100GB storage
- ✅ Supporto prioritario

---

## 🔄 **Aggiornamenti:**

### **Aggiorna Codice:**
```bash
# Fai modifiche al codice
git add .
git commit -m "Update bot"
git push origin main

# Railway aggiornerà automaticamente
```

### **Aggiorna Dipendenze:**
```bash
# Modifica requirements.txt
# Push su GitHub
# Railway reinstallerà automaticamente
```

---

## 🎯 **Checklist Pre-Deploy:**

- [ ] Token rimosso dal codice
- [ ] Repository GitHub creato
- [ ] File Railway creati
- [ ] .gitignore configurato
- [ ] Variabili d'ambiente preparate
- [ ] Test locale funzionante

---

## 🚀 **Deploy Completo:**

1. **Prepara Repository:**
   ```bash
   git init
   git add .
   git commit -m "Giglio Download Bot ready for Railway"
   git remote add origin https://github.com/TUO_USERNAME/giglio-download-bot.git
   git push -u origin main
   ```

2. **Deploy su Railway:**
   - Vai su railway.app
   - Crea nuovo progetto
   - Connetti GitHub repository
   - Aggiungi variabili d'ambiente
   - Deploy!

3. **Test:**
   - Cerca il bot su Telegram
   - Invia `/start`
   - Testa un download

---

## 🎉 **Completato!**

Il tuo bot sarà disponibile 24/7 su Railway con:
- ✅ **Uptime garantito**
- ✅ **Scalabilità automatica**
- ✅ **Logs in tempo reale**
- ✅ **Deploy automatici**
- ✅ **Sicurezza massima**

**URL del bot:** `https://TUO_PROGETTO.railway.app`
**Bot Telegram:** `@giglio_download_unlimited_bot`
