import time
import adafruit_dht
import requests
import json
from adafruit_blinka.microcontroller.bcm2711 import pin

# Hedef URL
API_URL = "http://192.168.27.1:8000/add_data"

# GPIO17 pini için
dht = adafruit_dht.DHT11(pin.D17)

def send_sensor_data(temperature, humidity):
    """
    Sıcaklık ve nem verilerini API'ye gönder
    """
    # JSON formatında veri gönder
    data = {
        "Sicaklik": f"{temperature:.1f}",
        "Nem": f"{humidity:.1f}"
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(API_URL, json=data, headers=headers)
        if response.status_code == 200:
            print("Veriler başarıyla gönderildi")
        else:
            print(f"Veri gönderimi başarısız. Durum kodu: {response.status_code}")
            print(f"Sunucu yanıtı: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Bağlantı hatası: {e}")

try:
    print("DHT11 sensör okuma ve veri gönderme başlatılıyor...")
    print(f"Hedef API: {API_URL}")
    
    while True:
        try:
            # Sensör verilerini oku
            temperature = dht.temperature
            humidity = dht.humidity
            
            if temperature is not None and humidity is not None:
                print(f"\nSıcaklık: {temperature:.1f}°C")
                print(f"Nem: {humidity:.1f}%")
                
                # Verileri API'ye gönder
                send_sensor_data(temperature, humidity)
            else:
                print("Veri alınamadı, tekrar deneniyor...")
                
        except RuntimeError as error:
            print(f"Runtime hatası: {error.args[0]}")
            time.sleep(2.0)
            continue
            
        except Exception as error:
            print(f"Hata oluştu: {error}")
            time.sleep(2.0)
            continue
            
        time.sleep(5.0)  # Her 5 saniyede bir veri gönder

except KeyboardInterrupt:
    print("\nProgram kullanıcı tarafından durduruldu.")
    
finally:
    print("Sensör kapatılıyor...")
    dht.exit()
    print("Program sonlandırıldı.")
