// Simple NeoPixel test.  Lights just a few pixels at a time so a
// 1m strip can safely be powered from Arduino 5V pin.  Arduino
// may nonetheless hiccup when LEDs are first connected and not
// accept code.  So upload code first, unplug USB, connect pixels
// to GND FIRST, then +5V and digital pin 6, then re-plug USB.
// A working strip will show a few pixels moving down the line,
// cycling between red, green and blue.  If you get no response,
// might be connected to wrong end of strip (the end wires, if
// any, are no indication -- look instead for the data direction
// arrows printed on the strip).
 
#include <Adafruit_NeoPixel.h>
 
#define PIN      6
#define N_LEDS 144
double current_date = 5.26;
double payment_date= 5.26;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(N_LEDS, PIN, NEO_GRB + NEO_KHZ800);
 
void setup() {
  strip.begin();
  strip.show();
  Serial.begin(9600);
}
 
void loop() {
  char startDemo;
    if(Serial.available() > 0){
    startDemo = Serial.read();
    }
  
  //Green
  changeColor(payment_date, 5.26, 0);
  //Red
  changeColor(payment_date, 5.25, 1);
  //Yellow
  changeColor(payment_date, 5.31, 2);
  //Blue
  changeColor(payment_date, 6.1, 3);
  
  strip.show();
  if(startDemo == 'y'|| startDemo=='Y'){
    Serial.println("in start demo");
    int bill = 3;
    delay(10*1000);
    changeColor(payment_date, 5.31, bill);
    strip.show();
    delay(10*1000);
    changeColor(payment_date, 5.25, bill);
    strip.show();
    delay(10*1000);
    changeColor(payment_date, 5.26, bill);
    strip.show();
    delay(10*1000);    
  }
}
static void changeColor(double payment_date, double upcoming_date, double numBill){
    //called from NESSIE API 
    //int payment_date = 15;
   //int upcoming_date = 1;
    
    //hardcoded
    double current_date = 5.26; 
    
    //bill is paid  
    if (payment_date == upcoming_date){
        //green 
        
        strip.setPixelColor(numBill, 0, 102, 0, 50);
    }
    
    //payment_date < upcoming_date  
    else if ((upcoming_date - current_date) <= 0){
        //red 
        
        strip.setPixelColor(numBill, 255, 0, 0, 50);
    }
     
    //
    else if ((upcoming_date - current_date) <= .07){
        //yellow 
        
        strip.setPixelColor(numBill, 255, 255, 0, 50); 
    }
    
    //
    else {
        //blue 

        strip.setPixelColor(numBill, 0, 0, 204, 50);
    }
      
}

