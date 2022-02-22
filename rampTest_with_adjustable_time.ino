// Changable Settings
const int period_m = 200;  // in milliseconds
const int aRes = 12; // anologWrite resolution in bits.    (I am not sure on this, but I believe it needs to be an even number


// Pin numbers
const int rampPin = A6;


// Interprettig the settings
const int maxStep = pow( 2 , aRes ) - 1 ;
const int period_u = 1000 * period_m; // period in micro seconds



void setup() {
  pinMode( rampPin, OUTPUT );
  analogWriteResolution(aRes);

}


// Ramp
void loop() {
 int rampStep = map(micros()%period_u, 0, period_u, 0, maxStep); // Converts current time to a ramp value
 analogWrite( rampPin, rampStep );
 }
