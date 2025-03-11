# DHT11 Sıcaklık ve Nem Takip Sistemi / DHT11 Temperature and Humidity Tracking System

## Türkçe

Bu proje, DHT11 sensörü ile ölçülen sıcaklık ve nem değerlerini izlemek için geliştirilmiş bir sistemdir. Raspberry Pi ile alınan sensör verileri, bir API aracılığıyla mobil uygulamaya aktarılır.

### Proje Bileşenleri

- *RaspberryPi-DHT11-Code*: Raspberry Pi üzerinde çalışan DHT11 sensör kodları
- *DHT11SensorAPI-main*: Sensör verilerini alıp işleyen API
- *DHT11MobileAPP-main*: Verileri görüntüleyen mobil uygulama

### Kurulum

#### Raspberry Pi Kurulumu

1. Repoyu klonlayın: git clone https://github.com/yasiryldrm/DHT11-Mobile-Tracker.git
2. Python sanal ortamı oluşturun: python -m venv venv
3. Sanal ortamı aktifleştirin: source venv/bin/activate
4. Gerekli kütüphaneleri yükleyin: pip install Adafruit-DHT RPi.GPIO
5. DHT11 sensörünü Raspberry Pi'ye bağlayın (GPIO pin bağlantıları için kod içindeki açıklamalara bakın)

#### API Kurulumu

DHT11SensorAPI-main klasörü içindeki talimatları takip edin.

#### Mobil Uygulama Kurulumu

DHT11MobileAPP-main klasörü içindeki talimatları takip edin.

### Kullanım

1. Raspberry Pi kodunu çalıştırın: python dht11_test1.py
2. API'yi başlatın
3. Mobil uygulamayı açın ve verileri görüntüleyin

---

## English

This project is a system developed to monitor temperature and humidity values measured with the DHT11 sensor. Sensor data collected by the Raspberry Pi is transferred to a mobile application via an API.

### Project Components

- *RaspberryPi-DHT11-Code*: DHT11 sensor code running on Raspberry Pi
- *DHT11SensorAPI-main*: API that processes sensor data
- *DHT11MobileAPP-main*: Mobile application displaying the data

### Installation

#### Raspberry Pi Setup

1. Clone the repository: git clone https://github.com/yasiryldrm/DHT11-Mobile-Tracker.git
2. Create a Python virtual environment: python -m venv venv
3. Activate the virtual environment: source venv/bin/activate
4. Install required libraries: pip install Adafruit-DHT RPi.GPIO
5. Connect the DHT11 sensor to your Raspberry Pi (see code comments for GPIO pin connections)

#### API Setup

Follow the instructions in the DHT11SensorAPI-main folder.

#### Mobile App Setup

Follow the instructions in the DHT11MobileAPP-main folder.

### Usage

1. Run the Raspberry Pi code: python dht11_test1.py
2. Start the API
3. Open the mobile app and view the data

---

## Project Developer / Proje Geliştirici

- Yasir Yıldırım
