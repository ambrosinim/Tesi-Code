/* Arduino Application to parse an input string such as "s/3*206/f" and actuate a robot arm with 3 Servos to reach a selected station
 *  Complete project:
 *  URL github reference: https://github.com/ma-tesi/Tesi-Code
*/

#include <Servo.h> //Inserire la libreria Servo

/* /// Servo INSTANCES ///*/
Servo Servo1; 
Servo Servo2;
Servo Servo3;




/* /// VARIABLES /// */

int current_position=0;
String parsed, parsed_substr, crc_src;
uint8_t parsed4crc[5];
char in;
// int i = 0;
int in_number;

char charin;
uint8_t before_separator = 1;
uint8_t ucrc_src, ind1;
int n =0;


/* /// FUNCTIONS PROTOTYPES /// */
  
uint8_t crc8( uint8_t *addr, uint8_t len);
uint8_t Compute_CRC8(uint8_t *bytes, int len);

void traj_back(Servo &servo, int current_position);
void traj_down(Servo &servo = Servo2);
void close_gripper(Servo &servo = Servo3);
void traj_lift(Servo &servo = Servo2);
void traj_station(Servo &servo, int selected, int *current_position);
void open_gripper(Servo &servo = Servo3);

void setup() {
  
  Servo1.attach (11);
  Servo2.attach (10);
  Servo3.attach (9); 
   
  Serial.begin(9600);

  Servo1.write(0);
  Servo2.write(140);
  Servo3.write(160);

  //Serial.print("AT+BAUD8");
  //delay(200);
}

void loop() {
/*
 * IL PROTOCOLLO DI TRASMISSIONE PREVEDE LA COMUNICAZIONE DI STRINGHE PROVVISTE DI INIZIO E FINE
  
*              es: s/2*199/f 
*  ovvero con: s/ per indicare l'inizio della stringa
*              per separare l'input dal crc_src
*              /f per indicare la fine della stringa

*/            

  
 /* Alternatva di parse tramite UART (non compatibile con il codice successivo)
  *  while(Serial.available() > 0){
    Serial.println("ok");
    charin = Serial.read();
    parsed += charin;
    */
    
    parsed = Serial.readString();  
    delay(5);


 /* ///  PROTOCOL CHECK: if the string ha the correct beginnning divide the string into input and CRC8 with the help of the separator and the last '/' /// */
    if(parsed[0] == 's' && parsed[1] == '/'){
      
        in =  parsed[2];
        if( parsed[3] == '*'){

           // string selection for crc calculus
           ind1 = parsed.indexOf('*');  
           //finds location of input
           parsed_substr = parsed.substring(0, ind1+1); //captures data String before separator
           for(int k=0; k<parsed_substr.length(); k++){ 
              parsed4crc[k] = parsed_substr[k];   
           }

          // string selection to get crc from PC
          n = ind1+1;
          while(parsed[n] != '/' && n < parsed.length()){
            crc_src += parsed[n];
            n++;
            }
        }


 /* ///  CRC8 conversion from a string to an integer to compare it with the one calculated /// */
    ucrc_src  = atoi (crc_src.c_str ());

      }

 /* ///  CRC8 CONTROL /// */
    if(ucrc_src != crc8(parsed4crc, 4)){
      in='#';
      Serial.print("protocol communication error:" );
      Serial.print(ucrc_src);
      Serial.print(" != ");
      Serial.println(crc8(parsed4crc, 4));

    }
    else{
      in_number = (int)in - '0';    // Transforms the input from its ASCII value to an integer
    }
 /* ///  CHECK INPUT COMPATIBILITY AND ACTUATE THE TRAJECTORY /// */
  if(0 < in_number && in_number < 4) {
  
    Serial.println('n');
    
    Serial.println("traj_back");
    traj_back(Servo1, current_position);
    
    
    Serial.println("traj_down");
    traj_down();

    Serial.println("close_gripper");
    close_gripper();
    
    Serial.println("traj_lift");
    traj_lift();
    
    Serial.println("traj_station " + (String)in_number);
    traj_station(Servo1, in_number, &current_position);
    
    Serial.println("open_gripper");
    open_gripper();
    
    
  }

            
  Serial.println('y');

  /* /// RESET input and strings /// */
  crc_src="";
  parsed = "";
  in='#';
  
  delay(5);
}


/* /// FUNCTIONS DECLARATION /// */


void traj_back(Servo &servo, int current_position){
  //Servo1
  for(int i = current_position; i>=0; i--){
        servo.write(i);
        delay(20);
      }
      return;
}

void traj_down(Servo &servo = Servo2){ 
    for(int i=140;i>69;i--){
      servo.write(i); //maggiore significa più in alto
      delay(20);
    }
}

void close_gripper(Servo &servo = Servo3){ 
    for(int i=100;i<160;i++){
      servo.write(i); //maggiore significa più in alto
      delay(20);
    }
}

void traj_lift(Servo &servo = Servo2){ 
    for(int i=70;i<141;i++){
      servo.write(i); 
      delay(20);
    }
}

void traj_station(Servo &servo, int selected, int *current_position){  // Passing current_position by address (side effect same as return)
  //Servo1
    volatile int limit = 181/selected;
    for(int i=0;i<limit;i++){
      servo.write(i);
      delay(20);
    }
    *current_position = limit-1;
}

void open_gripper(Servo &servo = Servo3){ 
     for(int i=160;i>100;i--){
      servo.write(i); 
      delay(20);
    }
}





uint8_t crc8( uint8_t *addr, uint8_t len) {
      uint8_t crc=0;
      for (uint8_t x = 0; x < len; x++) {
         uint8_t inbyte = addr[x];
         for (uint8_t j = 0; j < 8 ; j++) {
             uint8_t mix = (crc ^ inbyte) & 0x01;
             crc >>= 1;
             if (mix) 
                crc ^= 0x8C;
         inbyte >>= 1;
      }
    }
   return crc;
}

uint8_t Compute_CRC8(uint8_t *bytes, int len) {
  const uint8_t generator = 0x31;   // polynomial = x^8 + x^5 + x^3 + x^2 + x + 1 (ignore MSB which is always 1)
  uint8_t crc = 0;

  while (len--)
  {
    crc ^= *bytes++; /* XOR-in the next input byte */

    for (volatile int i = 0; i < 8; i++)
    {
      if ((crc & 0x80) != 0)
      {
        crc = (uint8_t)((crc << 1) ^ generator);
      }
      else
      {
        crc <<= 1;
      }
    }
  }
  return crc;
}
