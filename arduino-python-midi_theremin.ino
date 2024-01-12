#include <NewPing.h>

#define X_PING_PIN      8 // Arduino pin tied to trigger and echopin on x ping sensor.
#define Y_PING_PIN      9 // Arduino pin tied to trigger and echopin on y ping sensor.
#define MAX_DISTANCE 60 // Maximum distance (in cm) to ping.

NewPing xsonar(X_PING_PIN, X_PING_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
NewPing ysonar(Y_PING_PIN, Y_PING_PIN, 30); // NewPing setup of pins and maximum distance.

int xping;
int yping;

void setup() {
  Serial.begin(9600);
}

void loop() {
  xping = xsonar.ping_cm();
  yping = ysonar.ping_cm();
  Serial.print(xping);
  Serial.print(" ");
  Serial.print(yping);
  Serial.println();
}
