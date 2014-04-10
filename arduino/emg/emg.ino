

unsigned long period = 2500;

void setup() 
{
  Serial.begin(115200);
  init_adc();
}

float adc_readings[4];
unsigned long last_time = 0, now = 0, elapsed = 0;

void loop() 
{
  now = micros();
  elapsed = now - last_time;
  if (elapsed >= period)
  {
    adc_readings[0] = read_adc(0);
    adc_readings[1] = read_adc(1);
    adc_readings[2] = read_adc(2);
    adc_readings[3] = read_adc(3);

    Serial.write(255);
    Serial.write(255);
    write_int16(adc_readings[0]);
    write_int16(adc_readings[1]);
    write_int16(adc_readings[2]);
    write_int16(adc_readings[3]);
    write_int16(elapsed);
    last_time = now;
  }
}
void write_int16(int i)
{
   unsigned long j = i + 32766;
   Serial.write(j/256);
   Serial.write(j%256);
}
