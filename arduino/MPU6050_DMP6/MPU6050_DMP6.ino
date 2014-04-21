// SDA: A4
// SCL: A5

// Black: GND
// Purple: VCC
// Grey: A4
// White: A5

#include "MPU6050.h"
#include "Wire.h"
#include "HMC58X3.h"

MPU6050 mpu;
HMC58X3 magn;

int ix,iy,iz;

void setup() {

    Serial.begin(115200);
    
    mpu.setI2CBypassEnabled(true);
    magn.init(false);
    magn.calibrate(1, 32);
    magn.setMode(0);
    mpu.setI2CBypassEnabled(false);
    
    mpu.dmpInitialize();
}


void loop() 
{
  Quaternion* q = mpu.readQuat();
  
  mpu.setI2CBypassEnabled(true);
  magn.getValues(&ix,&iy,&iz);
  mpu.setI2CBypassEnabled(false);
  
  Serial.write(255);
  Serial.write(255);
  write_int16(q->w*32767);
  write_int16(q->x*32767);
  write_int16(q->y*32767);
  write_int16(q->z*32767);
  write_int16(ix*16);
  write_int16(iy*16);
  write_int16(iz*16);

//  Serial.println("");
}

void write_int16(int i)
{
  unsigned int ui = i + 32766;
  Serial.write(ui/256);
  Serial.write(ui%256);
//  Serial.print(i);
//  Serial.print(" ");
}

float q_array[4];
void sendToCube(Quaternion* q)
{
  q_array[0] = q->w;
  q_array[1] = q->x;
  q_array[2] = q->y;
  q_array[3] = q->z;
  serialPrintFloatArr(q_array, 4);
  Serial.println("");
}

void serialPrintFloatArr(float * arr, int length) {
  for(int i=0; i<length; i++) {
    serialFloatPrint(arr[i]);
    Serial.print(",");
  }
}

void serialFloatPrint(float f) {
  byte * b = (byte *) &f;
  for(int i=0; i<4; i++) {
    
    byte b1 = (b[i] >> 4) & 0x0f;
    byte b2 = (b[i] & 0x0f);
    
    char c1 = (b1 < 10) ? ('0' + b1) : 'A' + b1 - 10;
    char c2 = (b2 < 10) ? ('0' + b2) : 'A' + b2 - 10;
    
    Serial.print(c1);
    Serial.print(c2);
  }
}

void outputRawValues()
{
    int ax, ay, az, gx, gy, gz;
    mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    Serial.print("a/g:\t");
    Serial.print(ax); Serial.print("\t");
    Serial.print(ay); Serial.print("\t");
    Serial.print(az); Serial.print("\t");
    Serial.print(gx); Serial.print("\t");
    Serial.print(gy); Serial.print("\t");
    Serial.println(gz);
}
