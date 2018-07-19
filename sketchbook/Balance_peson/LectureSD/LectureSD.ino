//SPI   Uno Mega
//SS    10  53
//MOSI  11  51
//MISO  12  50
//SCK   13  52


#include <SPI.h>
#include <SD.h>

File monFichier;

void setup() {
  digitalRead(53);
    Serial.begin(9600);
  Serial.print("Initialisation de la carte SD...");

  if (!SD.begin(53)) {
    Serial.println("L'initialisation de la carte SD a echoue !");
    return;
  }
  Serial.println("L'initialisation de la carte SD a reussie !");

   monFichier = SD.open("test.csv");
  if (monFichier) {
    Serial.println("test.csv:");
    while (monFichier.available()) {
      Serial.write(monFichier.read());
    }
    // close the file:
    monFichier.close();
  } else {
    // if the file didn't open, print an error:
    Serial.println("Erreur lors de l'ouverture de test.txt");
  }
}

void loop() {
  // put your main code here, to run repeatedly:
}

