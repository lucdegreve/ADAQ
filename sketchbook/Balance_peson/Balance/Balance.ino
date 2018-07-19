// Library
#include "QuickStats.h"
#include <SPI.h>
#include <SD.h>
#include <Wire.h>
#include "RTClib.h"

// Call
QuickStats stats;
File monFichier;
RTC_DS3231 rtc;

// Variable 
int analogPin = 3;
int val = 0;
float valtab[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};


void setup() 
{
  Serial.begin(9600);

  Serial.print("Initialisation de la carte SD...");
  if (!SD.begin(53)) {
    Serial.println("L'initialisation de la carte SD a echoue !");
    return;
  }
  Serial.println("L'initialisation de la carte SD a reussie !");
  SD.remove("test.csv");                                                          // delete test.csv file
  monFichier = SD.open("test.csv", FILE_WRITE);                                   // create or open the file
  if (monFichier) {                                                               // if the file is open :
    Serial.println("En train d ecrire l'entête dans le fichier test.csv");
    monFichier.println("Hour;Median;Standard_Error;BalanceID");
    monFichier.close();
}
  if (! rtc.begin()) {                                                            //Clock opening 
    Serial.println("Couldn't find RTC");
    while (1);
  }
}



void loop() {
  for (int i=0; i < 10; i++){
    val = analogRead(analogPin);    
    Serial.println(val);
    valtab[i] = val;                                                              // fill in the list with ten values
    delay(100);
  }
  Serial.print("Median: ");
  Serial.println(stats.median(valtab,10));                                        //print median
  Serial.print("Standard Error: ");
  Serial.println(stats.stderror(valtab,10));                                      //print standard error


  if((stats.median(valtab,10))>35){                                               // Write if median > 35 Kg
    monFichier = SD.open("test.csv", FILE_WRITE);
  
    if (monFichier) {                                                             // if the file is open :
      DateTime now = rtc.now();
      Serial.println("Sauvegarde d'une pesée dans le fichier test.csv");
      monFichier.print(now.year(), DEC);monFichier.print('/');monFichier.print(now.month(), DEC);monFichier.print('/');// Date and Hour
      monFichier.print(now.day(), DEC);monFichier.print(" ");monFichier.print(now.hour(), DEC);monFichier.print(':');
      monFichier.print(now.minute(), DEC);monFichier.print(':');monFichier.print(now.second(), DEC);monFichier.print(";");
      monFichier.print(stats.median(valtab,10));monFichier.print(";"); // Median 
      monFichier.print(stats.stderror(valtab,10));monFichier.print(";"); // Standard Error 
      monFichier.println(1); // BalanceID
      monFichier.close();
    }
  }
}
