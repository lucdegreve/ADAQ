
//MesureTemperature Dalle de stockage


// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*-----( Import needed libraries )-----*/
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//-------- Popur general

// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*-----( Declare Constants )-----*/
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*-----( Declare objects )-----*/
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*-----( Declare Variables )-----*/
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


//-------- Lectures analogiques
int pinsAnalogicRead[5] = {0,1,2,3,4};
int NAnalogicRead = (int) sizeof(pinsAnalogicRead)/ sizeof(pinsAnalogicRead[0]);

//-------- Relais
const int TableRelaisDispo[5][8]={{2,3,4,5,6,7,8,9},{10,11,12,13,22,23,24,25},{26,27,28,29,30,31,32,33},{34,35,36,37,38,39,40,41},{42,43,44,45,46,47,48,49}};
const int NRelais = (int) sizeof(TableRelaisDispo)/ sizeof(TableRelaisDispo[0]);
const int NSondeTot = (int) sizeof(TableRelaisDispo)/sizeof(TableRelaisDispo[0][0]);
const int NDalle = (int) sizeof(TableRelaisDispo[0])/sizeof(TableRelaisDispo[0][0]);

//-------- Temperature

float resRef[]= {10000.0,10000.0,10000.0,10000.0,10000.0,10000.0}; // Valeur de resistance des résitances de référence 10000 ohm 6 valeurs car potentielleme 6 sondes par cellules
int delai_cycle = 30000;

//-------- Communication

int state;
const byte buffSize = 40;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromPC = false;
int newValue = 0;

// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void setup()   /*----( SETUP: RUNS ONCE )----*/
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
{

  // Check
  Serial.print("NRelais");
  Serial.println(NRelais);
  Serial.print("NDalle");
  Serial.println(NDalle);
  Serial.print("NSondeTot");
  Serial.println(NSondeTot);
  Serial.print("NAnalogicRead");
  Serial.println(NAnalogicRead);

  //-------- Relais 
  for (int it_relais=0; it_relais < NRelais; it_relais++){
    for (int it_dalle=0; it_dalle < NDalle; it_dalle++){   
      pinMode(TableRelaisDispo[it_relais][it_dalle],OUTPUT);
      digitalWrite(TableRelaisDispo[it_relais][it_dalle],HIGH);
    }
  }

  Serial.begin(9600);  // Used to type in characters
  delay(30000);

}//--(fin setup )---*/

// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void loop()   /*----( LOOP: RUNS CONSTANTLY )----*/
// ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
{

  /*  
  getDataFromPC();

  if (not readInProgress and newDataFromPC){
  
    state = newValue;
    newDataFromPC = false;

    if (state == 1) {
      Serial.println("<Running>");
    }
    else if (state == 0) {
      Serial.println("<Ready>");
    }
    else {
      Serial.println("<Stopped>");
    }
  }
  */

  state = 1;
  
  if (not readInProgress and state == 1) {
    // loop over the NDalles
    for (int it_dalle = 0; it_dalle < NDalle; it_dalle++){
      for (int it_relais = 0; it_relais < NRelais; it_relais++){
        digitalWrite(TableRelaisDispo[it_relais][it_dalle],LOW);
      }
      delay(1000);
  
      float resMeas;
      int values [10];
      
      for (int it_relais = 0; it_relais < NRelais; it_relais++){
      
        for (int it = 0; it < 10; it++){
          delay(50);
          resMeas = (float) (1024.0/ (float) analogRead(pinsAnalogicRead[it_relais])-1)*resRef[it_relais]; 
          values[it] = (1/(1.129336*pow(10,-3)+2.341350*pow(10,-4)*log(resMeas)+8.758753*pow(10,-8)*pow(log(resMeas),3))-273.15);
        }
  
        float sum = 0.0, mean, standardDeviation = 0.0;
  
        int i;
        for(i = 0; i < 10; ++i)
        {
          sum += values[i];
        }
  
        mean = sum/10;
   
        for(i = 0; i < 10; ++i)
          standardDeviation += pow(values[i] - mean, 2);
  
        standardDeviation = sqrt(standardDeviation / 10);
        
        delay(500);
        Serial.print("<");
        Serial.print(millis());
        Serial.print(", ");
        Serial.print(it_dalle);
        Serial.print(", ");
        Serial.print(it_relais);
        Serial.print(", ");
        Serial.print(mean);
        Serial.print(", ");
        Serial.print(standardDeviation);
        Serial.println(">");
      }
    
      for (int it_relais = 0; it_relais < NRelais; it_relais++){
        digitalWrite(TableRelaisDispo[it_relais][it_dalle],HIGH);
      }
    }
    delay(delai_cycle);

  }

}/* --(end main loop )-- */


void getDataFromPC() {

    // receive data from PC and save it into inputBuffer
    
  if(Serial.available() > 0) {

    char x = Serial.read();

      // the order of these IF clauses is significant
      
    if (x == endMarker) {
      readInProgress = false;
      newDataFromPC = true;
      inputBuffer[bytesRecvd] = 0;
      parseData();
    }
    
    if(readInProgress) {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    if (x == startMarker) { 
      bytesRecvd = 0; 
      readInProgress = true;
    }
  }
}

//=============
 
void parseData() {

  newValue = atoi(inputBuffer);     // convert to an integer

}

/* ( THE END ) */
