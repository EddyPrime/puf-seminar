# puf-seminar
Physical Unclonable Functions seminar repository for the course Advanced Information System Security and Blockchain 2023/24 at Engineering in Computer Science Master's degree Sapienza.

## Usage

### Requirements

Python packages

```shell
pyserial
numpy
```

### Arduino

The Arduino program, the custom serial monitor and the Python analysis script are contained in the **arduino** folder. Make sure that `bytes_to_read` in `serial_monitor.py` is at most the value in `char bytes[]` and `i < ` in `sram_puf.ino`. For instance
```python
bytes_to_read = 4
```
and
```c++
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
```

The number of bytes to read from the device depends on the device itself. The seminar involved a Keystudio Mega 2560 R3 board with 8KB of SRAM. Taking into account the bytes occupied by the program, the boot loader, etc., 8004 is the upperbound of bytes that can be retrieved.

To read data from the board, do the following steps:

1. Set up the parameters, i.e. the number of bytes
2. Compile and upload the program onto the board. You can do this by using, for instance, the Arduino IDE
3. Identify the port where your device is connected to and hardcode it into the variable `SERIAL_PORT` in `serial_monitor.py`
4. Start the monitor by running
```shell
python3 serial_monitor.py
``` 
5. Connect the device via USB to your computer
6. Wait for the string to be read (upon completion, the string will be printed on `stdout`)
7. Disconnect the device from your computer
8. Wait some seconds to let the memory cells completely discharge
9. Repeat from 5
10. Once the amount of strings collected makes you happy, press `Ctrl-C` or `Cmd-C` to exit the program

Once you collected some strings from the device, you may want to compute some metrics. Run
```shell
python3 analysis.py
```

### Canetti

The main code of the fuzzy extractor proposed by Canetti et al. is in `canetti.py`. You can execute it by running
```shell
python3 canetti.py
```
Some parameters can be set to perform different experiments. In particular:
- **n** is the length of the string in bits
- **k** is the length of the key in bits
- **eabs** is the absolute error of the noisy source
- **experiments** is the number of runs performed to collect statistics
- **random_w** chooses whether retrieving them from a file (0) or generating them randomly (not 0). In the first case, make sure to collect data from your device before executing this script.

The cryptographic primitive which the fuzzy extractor is built upon, i.e. digital lockers, is implemented in **digitallocker.py**. Random generation of strings is in charge of **patterns.py**.

### X-Lock

This is a Git Submodule that refers to [this repository](https://github.com/EddyPrime/xlock). It contains the code of the fuzzy extractor proposed by Liberati et al.

To compile run:
- `make` for an optimized compilation
- `make debug` to have more debug information
- `make speed` to include also speed metrics

After compilation, execute the code by running
```shell
make run
```

To clean up everything after execution, run:
```shell
make clean
```