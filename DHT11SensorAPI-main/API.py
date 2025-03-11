from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# MSSQL bağlantı ayarları
try:
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=104.247.167.130\\mssqlserver2022;"
        "DATABASE=huseyi98_DHT;"
        "UID=huseyi98_DHTadmin;"
        "PWD=55~6Vmo2b;"
    )
    db = pyodbc.connect(connection_string)
    print("MSSQL bağlantısı başarılı!")
except pyodbc.Error as e:
    print(f"MSSQL bağlantı hatası: {e}")
    db = None

# Home sayfası
@app.route('/', methods=['GET'])
def home():
    """Home sayfası."""
    return jsonify({
        "message": "Hoş geldiniz! Bu bir DHT veritabanı API'sidir.",
        "endpoints": {
            "POST /add_data": "Yeni bir veri eklemek için.",
            "GET /get_last_data": "Son eklenen veriyi almak için."
        }
    }), 200

# Session Operations
@app.route('/add_data', methods=['POST'])
def add_data():
    """Yeni bir veri ekler."""
    try:
        # JSON verisini al
        data = request.get_json()
        print("Gelen JSON:", data)  # JSON verisini yazdır

        # JSON'daki gerekli anahtarları kontrol et
        if not all(k in data for k in ('Sicaklik', 'Nem')):
            return jsonify({"error": "Gerekli anahtarlar eksik"}), 400

        Sicaklik = data['Sicaklik']
        Nem = data['Nem']

        # MSSQL sorgusu
        if db is None:
            return jsonify({"error": "Veritabanı bağlantısı mevcut değil."}), 500

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO Tbl_DHT (Sicaklik, Nem) VALUES (?, ?)",
            (Sicaklik, Nem)
        )
        db.commit()

        return jsonify({"message": "Veri başarıyla eklendi!"}), 200
    except KeyError as e:
        print(f"KeyError: {e}")
        return jsonify({"error": f"Eksik anahtar: {str(e)}"}), 400
    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500

# Son eklenen veriyi getirme
@app.route('/get_last_data', methods=['GET'])
def get_last_data():
    """Veritabanından son eklenen veriyi çeker."""
    try:
        # MSSQL sorgusu
        if db is None:
            return jsonify({"error": "Veritabanı bağlantısı mevcut değil."}), 500

        cursor = db.cursor()
        cursor.execute("SELECT TOP 1 * FROM Tbl_DHT ORDER BY ID DESC")  # ID sırasına göre en son eklenen veri
        row = cursor.fetchone()

        if row:
            # Sütun adlarını al
            columns = [column[0] for column in cursor.description]
            # Satırı bir sözlük olarak döndür
            result = dict(zip(columns, row))
            return jsonify(result), 200
        else:
            return jsonify({"message": "Veri bulunamadı."}), 404
    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
