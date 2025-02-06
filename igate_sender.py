import socket
import argparse

def ax25_encode_callsign(callsign, ssid=0):
    callsign = callsign.ljust(6)[:6]    # Assicura che sia esattamente 6 caratteri
    encoded = bytearray()
    for char in callsign:
        encoded.append(ord(char) << 1)
    encoded.append((ssid << 1) | 0x60)  # SSID con bit di estensione impostato
    return encoded

def create_aprs_frame(source, destination, path, message):
    frame = bytearray()
    
    frame.extend(ax25_encode_callsign("APBOT1")) # per formattare il path
    frame.extend(ax25_encode_callsign(source.split('-')[0], int(source.split('-')[1]) if '-' in source else 0))

    for digi in path.split(','):
        frame.extend(ax25_encode_callsign(digi.split('-')[0], int(digi.split('-')[1]) if '-' in digi else 0))
    

    frame[-1] |= 0x01   # Imposta l'ultima estensione a 1
    frame.append(0x03)  # Control field UI frame
    frame.append(0xF0)  # PID per APRS

    message = f":{destination.ljust(9)[0:9]}:" + message # formattazione per messaggi
    frame.extend(message.encode('ascii'))

    return frame

def send_kiss_frame(ip, port, frame):
    kiss_frame = bytearray([0xC0, 0x00])  # Inizio frame KISS, comando 0x00 (Data)
    kiss_frame.extend(frame)
    kiss_frame.append(0xC0)               # Fine frame KISS
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        print (f"TNC connesso: {ip}:{port}")
        s.sendall(kiss_frame)
    print(f"Frame inviato: {kiss_frame}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Invia un messaggio APRS via KISS a un TNC IP.")
    parser.add_argument("tnc_ip", type=str, help="Indirizzo IP del TNC")
    parser.add_argument("tnc_port", type=int, help="Porta KISS del TNC")
    parser.add_argument("source", type=str, help="Callsign sorgente (es. MYCALL-10)")
    parser.add_argument("destination", type=str, help="Callsign di destinazione (es. APRS)")
    parser.add_argument("path", type=str, help="Path APRS (es. WIDE1-1)")
    parser.add_argument("message", type=str, help="Messaggio da inviare")
    
    args = parser.parse_args()
    
    frame = create_aprs_frame(args.source, args.destination, args.path, args.message)
    send_kiss_frame(args.tnc_ip, args.tnc_port, frame)
