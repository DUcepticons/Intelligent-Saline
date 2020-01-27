#include <HX711.h>

// Scale Settings
const int SCALE_DOUT_PIN = D6;
const int SCALE_SCK_PIN = D5;

HX711 scale;

void setup() {
  Serial.begin(115200);
  scale.begin(SCALE_DOUT_PIN, SCALE_SCK_PIN);
  scale.set_scale(45);// <- set here calibration factor!!!  45 works well
  scale.tare();
}

void loop() {
  float weight = scale.get_units(1);
  Serial.println(String(weight, 2));
  delay(200);
}
