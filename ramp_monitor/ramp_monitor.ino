/**
 * @file ramp_monitor.ino
 * @author Jonathan Fuzaro Alencar (jfuzaroa@outlook.com)
 * @brief Arduino program that serves to ramp piezo actuator voltage and
 * transmit signals from the Fabry-Perot and saturated absorption photodiodes.
 * @version 0.1
 * @date 2022-02-22
 * 
 */


// TODO

// define Arduino pins for photodiode (PD) data acquisition and voltage ramp
int constexpr kSatAbsPin     = A0; // analog input pin for saturated absorption PD
int constexpr kErrorPin      = A1; // analog input pin for error signal
int constexpr kFabPerPin     = A2; // analog input pin for Fabry-Perot PD
int constexpr kRampPin       = A6; // analog output pin for voltage ramp

// define serial baud (bit) rate
int constexpr kBaud = 9600;

void flash_LED(unsigned long ms = 100) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(ms);
    digitalWrite(LED_BUILTIN, LOW);
    delay(ms);
}

void setup() {
    // configure pins for input and output
    pinMode(kSatAbsPin, INPUT);
    pinMode(kErrorPin, INPUT);
    pinMode(kFabPerPin, INPUT);
    pinMode(kRampPin, OUTPUT);
    pinMode(LED_BUILTIN, OUTPUT);

    Serial.begin(kBaud); // begin serial communication via USB
}

void loop() {

    // while (!Serial) { flash_LED(500); } // wait for USB serial port to connect

    while (!Serial.available()) {
        Serial.print('R');
        delay(300);
        if (Serial.read() == 'b') { flash_LED(200); }
        else { Serial.flush(); }
    }

    if (Serial.available()) {
        
        // Serial.write();
    }
}