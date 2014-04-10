void setup() 
{
  Serial.begin(115200);
}

void loop() 
{
   write_int16(1555);
   delay(100);
}

void write_int16(int i)
{
   unsigned long j = i + 32766;
   Serial.write(j/256);
   Serial.write(j%256);
}
