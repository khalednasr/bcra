#include<SoftwareSerial.h>
#define RxD 6
#define TxD 7

// connect KEY to +5V
SoftwareSerial BT(RxD,TxD);

void setup() 
{
  Serial.begin(115200);
  
  BT.begin(38400);
  BT.print("AT+UART=115200,0,0\r\n");
  print_bt_response();

  BT.print("AT+UART?\r\n");
  print_bt_response();
}

void loop() 
{
   
}

void print_bt_response()
{
  while (BT.available() == 0);
  while (BT.available()>0)
  {
    Serial.print((char)BT.read());
  }
}
