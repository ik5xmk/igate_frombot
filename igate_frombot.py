# pip install telepot --break-system-packages
import telepot
import os
import re

# configurazione
TOKEN   = "YOUR-BOT-TOKEN" # token del bot
IP      = "1.1.1.1"        # ip/dns del TNC
PORT    = 8001             # porta del TNC
ORIGINE = "MYCALL-10"      # callsign del mittente del messaggio
PATH    = "WIDE1-1"        # path per APRS

# Funzione per gestire i messaggi ricevuti
def ricevi_messaggio(msg):
    contenuto = msg.get("text", "")
    
    if contenuto.startswith("/"): # ci interessa solo quello che inizia con /
        chat_id = msg["chat"]["id"]
        print (f"Messaggio ricevuto: {contenuto}")

        testo = contenuto[1:].split(' ', 1)
        destinatario = testo[0].upper()                     # Testo tra / e il primo spazio
        messaggio = testo[1] if len(testo) > 1 else 'TEST'  # Resto della stringa
        messaggio = re.sub(r'[^a-zA-Z0-9 ]', '', messaggio) # lascia solo lettere e numeri

        # assembla il comando ed invia il frame al tnc
        cmd = f"python3 igate_sender.py {IP} {str(PORT)} {ORIGINE} {destinatario} {PATH}  \"{messaggio}\""
        # print ("Eseguo:\n" + cmd)
        os.system (cmd)

        # risposta al bot
        bot.sendMessage (chat_id, f"Hai inviato a: {destinatario} il testo: {messaggio}")

# Crea il bot e imposta l'ascolto dei messaggi
bot = telepot.Bot(TOKEN)
bot.message_loop(ricevi_messaggio)

print ("Bot in ascolto...")

# Mantieni attivo il bot
import time
while True:
    time.sleep(10)
