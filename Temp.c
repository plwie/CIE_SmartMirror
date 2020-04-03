#include "DHT.h"

DHT dht;

void setup() {
    Serial.begin(9600);
    Serial.println();
    Serial.println("Status\tHumidity (%)\tTemperature (C)");

    dht.setup(2)
}

void loop(){
    delay(dht.getMinimumSamplingPeriod());

    float humidity = dht.getHumidity();
    float temperature = dht.getTemperature();

    Serial.println(dht.getStatusString());
    Serial.println(\t);
    Serial.println(humidity, 1);
    Serial.println(\t\t);
    Serial.println(temperature, 1);
}
