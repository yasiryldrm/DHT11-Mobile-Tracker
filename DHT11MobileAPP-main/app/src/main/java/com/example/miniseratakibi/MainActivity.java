package com.example.miniseratakibi;

import android.os.Bundle;
import android.os.Handler;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import org.json.JSONObject;
import java.io.IOException;
import java.util.concurrent.TimeUnit;

public class MainActivity extends AppCompatActivity {

    private TextView temperatureTextView;
    private TextView humidityTextView;
    private OkHttpClient client;
    private final Handler handler = new Handler();
    private final int REFRESH_INTERVAL = 5000; // 5 saniye

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // View'leri tanımlıyoruz
        temperatureTextView = findViewById(R.id.temperatureTextView);
        humidityTextView = findViewById(R.id.humidityTextView);
        initHttpClient();

        // Veriyi periyodik olarak yenile
        startDataRefresh();
    }

    private void initHttpClient() {
        client = new OkHttpClient.Builder()
                .connectTimeout(30, TimeUnit.SECONDS)
                .writeTimeout(30, TimeUnit.SECONDS)
                .readTimeout(30, TimeUnit.SECONDS)
                .build();
    }

    private void fetchDataFromAPI() {
        // Flask API'nin URL'si
        String url = "http://192.168.27.1:8000/get_last_data";

        // İstek oluştur
        Request request = new Request.Builder()
                .url(url)
                .get()
                .addHeader("Content-Type", "application/json")
                .build();

        // API çağrısı yap
        client.newCall(request).enqueue(new Callback() {

            @Override
            public void onFailure(Call call, IOException e) {
                // Hata durumunda
                e.printStackTrace();
                runOnUiThread(() -> {
                    temperatureTextView.setText("Hata: API'ye ulaşılamadı");
                    humidityTextView.setText("Lütfen bağlantınızı kontrol edin.");
                });
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    // Başarılı yanıt durumunda
                    final String responseData = response.body().string();
                    runOnUiThread(() -> {
                        try {
                            // JSON verisini ayrıştır
                            JSONObject json = new JSONObject(responseData);
                            double temperature = json.getDouble("Sicaklik");
                            int humidity = json.getInt("Nem");

                            // Ekrana yazdır
                            temperatureTextView.setText("Sıcaklık: " + temperature + "°C");
                            humidityTextView.setText("Nem: " + humidity + "%");
                        } catch (Exception e) {
                            // JSON ayrıştırma hatası
                            e.printStackTrace();
                            temperatureTextView.setText("Hata: Veriler işlenemedi.");
                            humidityTextView.setText("JSON hatası oluştu.");
                        }
                    });
                } else {
                    // Yanıt başarısızsa
                    runOnUiThread(() -> {
                        temperatureTextView.setText("Hata: " + response.code());
                        humidityTextView.setText("Sunucu yanıt vermiyor.");
                    });
                }
            }
        });
    }

    private void startDataRefresh() {
        // 5 saniyede bir API'den veri çeker
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                fetchDataFromAPI();
                handler.postDelayed(this, REFRESH_INTERVAL); // Tekrar çağır
            }
        }, 0); // Hemen başlasın
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        handler.removeCallbacksAndMessages(null); // Handler'ı durdur
    }
}
