#include <DHT.h>

#define DHTPIN 2       // Pino de dados conectado ao Arduino
#define DHTTYPE DHT11  // Tipo do sensor

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  Serial.println("Iniciando leitura do DHT11...");
  dht.begin();
}

void loop() {
  delay(2000);
  float temp = dht.readTemperature();

  if (isnan(temp)) {
    Serial.println("❌ Sensor não detectado ou leitura falhou.");
  } else {
    Serial.print("🌡️ Temperatura: ");
    Serial.print(temp);
    Serial.println(" °C");
  }
}
