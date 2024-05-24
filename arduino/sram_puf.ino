char bytes[4] __attribute__((section(".noinit")));

void setup()
{
  Serial.begin(115200);
  for (int i = 0; i < 4; i++)
  {
    Serial.write((unsigned int)bytes[i]);
  }
  Serial.println();
}

void loop() {}