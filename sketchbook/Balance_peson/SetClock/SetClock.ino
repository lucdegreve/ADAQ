// Arduino Mega:
// ----------------------
// DS3231:  SDA pin   -> Arduino Digital 20 (SDA) 
//          SCL pin   -> Arduino Digital 21 (SCL)

#include <DS3231.h>

// Init the DS3231 using the hardware interface
DS3231  rtc(SDA, SCL);

void setup()
{
  // Setup Serial connection
  Serial.begin(9600);

  
  // Initialize the rtc object
  rtc.begin();
  
  // The following lines can be uncommented to set the date and time
  rtc.setDOW(THURSDAY);     // Set Day-of-Week to SUNDAY
  rtc.setTime(11, 40, 30);     // Set the time to 12:00:00 (24hr format)
  rtc.setDate(19, 7, 2018);   // Set the date to January 1st, 2014
}

void loop()
{

}
