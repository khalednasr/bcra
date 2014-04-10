#include <SPI.h>

// ADC0: CH0, CH1, SS: 9
// ADC1: CH2, CH3, SS: 10

// Connections:
// ADC 1 --- SS
// ADC 5 --- 11
// ADC 6 --- 12
// ADC 7 --- 13

int ss_pins[2] = {9, 10};

void init_adc()
{
  pinMode(ss_pins[0], OUTPUT);
  pinMode(ss_pins[1], OUTPUT);
  pinMode(ss_pins[2], OUTPUT);
  
  digitalWrite(ss_pins[0], HIGH);
  digitalWrite(ss_pins[1], HIGH);
  digitalWrite(ss_pins[2], HIGH);
  
  SPI.setClockDivider( SPI_CLOCK_DIV16 );
  SPI.setBitOrder(MSBFIRST);
  SPI.setDataMode(SPI_MODE0);
  SPI.setBitOrder(MSBFIRST);
  SPI.begin();
}

int read_adc(int ch)
{
  int ss_index = ch / 2;
  digitalWrite(ss_pins[ss_index], LOW);
  
  byte cmd;
  int adc_high_byte, adc_low_byte;
  SPI.transfer(0b00000001);
  
  if (ch % 2 == 0) cmd = 0b10100000;
  if (ch % 2 == 1) cmd = 0b11100000;
  adc_high_byte = SPI.transfer(cmd) & 0b00011111;
  adc_low_byte = SPI.transfer(0);
  
  int adc_reading = (adc_high_byte << 8) + adc_low_byte; 
  
  digitalWrite(ss_pins[ss_index], HIGH);
  
  return adc_reading;
}





