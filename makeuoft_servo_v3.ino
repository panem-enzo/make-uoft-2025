#include <Servo.h>

const int trigPin = 8;
const int echoPin = 9;
const int servoPin = 7;
const int buzzerPin = 5;
const int ledPin = 10;
Servo myServo;

// Distance thresholds
const int detectionThreshold = 4000;  // Max reliable range for HC-SR04
const int alertThreshold = 30;       // Alert if object is within 40 cm

void setup() {
    Serial.begin(9600);
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
    pinMode(buzzerPin, OUTPUT);
    pinMode(ledPin, OUTPUT);
    myServo.attach(servoPin);
}

void loop() {
    static int angle = 0;
    static int direction = 1; // 1 for increasing, -1 for decreasing

    // Move the servo
    myServo.write(angle);
    delay(50);  // Allow time for servo movement


    // Measure distance
    int distance = getDistance();
    
    // Print distance to Serial Monitor
    /*Serial.print("Measured Distance: ");
    Serial.print(distance);
    Serial.println(" cm");*/
    delay(15);
  //calculateDistance();
  Serial.print(angle);
  //Serial.println('\n');
  Serial.print(",");
  Serial.println(distance);

    // Log detection if within range
    /*if (distance > 0 && distance < detectionThreshold) {
        Serial.print("Object detected at ");
        Serial.print(angle);
        Serial.print("° - Distance: ");
        Serial.print(distance);
        Serial.println(" cm");
    }*/

    // Alert if object is too close
    if (distance > 0 && distance < alertThreshold) {
        //Serial.println("🚨 ALERT: Object too close! 🚨");
        
        for (int i = 0; i < 3; i++) {  // Flash LED 5 times
            digitalWrite(ledPin, HIGH);
            tone(buzzerPin, 1000);
            delay(20);
            digitalWrite(ledPin, LOW);
            noTone(buzzerPin);
            //delay(50);
        }
    }

    // Adjust servo angle for continuous movement
    angle += direction * 5;

    // Reverse direction at limits
    if (angle >= 180 || angle <= 0) {
        direction *= -1;
    }
}

int getDistance() {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    long duration = pulseIn(echoPin, HIGH);
    int distance = duration * 0.034 / 2;  // Convert to cm

    // Ensure we return a valid distance within sensor limits
    return (distance > 0 && distance < 4000) ? distance : -1;
}