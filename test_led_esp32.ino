// GHOST-PROTOCOL: TEST DE VIDA ESP32-C3
// Este codigo hace parpadear el LED interno del SuperMini

// El LED interno del ESP32-C3 SuperMini suele estar en el pin 8
const int LED_PIN = 8; 

void setup() {
  // Configuramos el pin como salida
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
  Serial.println(">>> ESP32-C3 INICIADO - GHOST PROTOCOL TEST");
}

void loop() {
  // Prendemos el LED
  digitalWrite(LED_PIN, HIGH);
  Serial.println("LED ENCENDIDO");
  delay(1000); // Esperamos 1 segundo
  
  // Apagamos el LED
  digitalWrite(LED_PIN, LOW);
  Serial.println("LED APAGADO");
  delay(1000); // Esperamos 1 segundo
}