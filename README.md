# README.md

If you have any questions or need assistance with usage, feel free to contact support@unitree.com.

### Notice

support motor: GO-M8010-6 motor、A1 motor、 B1 motor

gcc >= 5.4.0 (for x86 platform)

gcc >= 7.5.0 (for Arm platform) 

run gcc --version  command to check your gcc version

### Build
Requires CMake 3.18 or newer, a C++14 compiler, and Python 3.7 or newer
with matching development headers. The bundled pybind11 2.13.6 supports
standard CPython 3.13 builds.

```bash
mkdir build
cd build
cmake ..
make
```

### Build for Python 3.13

Install Python 3.13 and its development headers (for example,
`python3.13-dev` on distributions that provide that package). From the
repository root, use a separate build directory for each Python version:

```bash
cmake -S . -B build/python313 \
  -DPython_EXECUTABLE="$(command -v python3.13)"
cmake --build build/python313 --target unitree_actuator_sdk -j
(cd build/python313 && ctest --output-on-failure)
```

If Python is managed by `uv`, use `-DPython_EXECUTABLE="$(uv python find 3.13)"`
instead. An absolute path to a virtual environment's Python also works.
The selected interpreter must have development headers available.

On x86-64 Linux, the extension is written to
`lib/unitree_actuator_sdk.cpython-313-x86_64-linux-gnu.so`, alongside
`libUnitreeMotorSDK_Linux64.so`. On ARM64, the extension has the corresponding
platform suffix and links to `libUnitreeMotorSDK_Arm64.so`. The output goes
to this repository's `lib/` directory regardless of the build directory.
Each Python version needs its own build; renaming a Python 3.8 or 3.12
extension does not make it compatible with Python 3.13.

CTest imports the extension and checks command construction and native
queries without opening a serial port or moving a motor. To build the C++
examples as well, omit `--target unitree_actuator_sdk` from the build command.

### Run
If the compilation is successful, many C++ example executable files will be generated in the build folder. Then run the examples with 'sudo', for example:
```bash
sudo ./example_a1_motor
```

If you need to run the Python example, please enter the "python" folder. Then run the examples with 'sudo', for example:
```python
sudo python3 example_a1_motor.py
```

For the Python 3.13 GO-M8010-6 example, use the same interpreter selected
at build time and run from the `python/` directory:

```bash
cd python
sudo /absolute/path/to/python3.13 example_goM8010_6_motor.py
```

This example sends motor commands; use CTest above for a hardware-free check.

### Tip

The code snippet below demonstrates an example of assigning values to the command structure `cmd` in `example_a1_motor.cpp`. It should be noted that the commands are all for the **rotor** side. However, the commands we usually compute are for the **output** side. Therefore, when assigning values, we need to consider the conversion between them.

```c++
cmd.motorType = MotorType::A1;
data.motorType = MotorType::A1;
cmd.mode  = queryMotorMode(MotorType::A1,MotorMode::FOC);
cmd.id    = 0;
cmd.kp    = 0.0;
cmd.kd    = 2;
cmd.q     = 0.0;
cmd.dq    = -6.28*queryGearRatio(MotorType::A1);
cmd.tau   = 0.0;
serial.sendRecv(&cmd,&data);
```

![Simple Diagram of A1 Motor](Simple_Diagram_of_A1_Motor.png)

Typically, for kp and kd, assuming the motor's gear ratio is r, when calculating kp and kd on the rotor side, we need to convert kp and kd on the output side by dividing them by the square of r. 

$$kp_{\text{rotor}} = \frac{kp_{\text{output}}}{r^2}$$

$$kd_{\text{rotor}} = \frac{kd_{\text{output}}}{r^2}$$

This conversion relationship is demonstrated in the example `example_a1_motor_output.cpp`.By the way, in the example `example_a1_motor_output.cpp`, the kp on the rotor side is additionally divided by 26.07, and the kd on the rotor side is additionally multiplied by 100.0. These are magic numbers for the A1 and B1 motor. When controlling other motors, there is no need to consider these additional steps.
