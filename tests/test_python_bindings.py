"""Exercise the compiled bindings without opening a serial port."""

from pathlib import Path
import sysconfig
import unittest

import unitree_actuator_sdk as sdk


class PythonBindingsTest(unittest.TestCase):
    def test_loads_built_extension_for_running_python(self):
        expected = (
            Path(__file__).resolve().parents[1]
            / "lib"
            / ("unitree_actuator_sdk" + sysconfig.get_config_var("EXT_SUFFIX"))
        )
        self.assertEqual(Path(sdk.__file__).resolve(), expected.resolve())

    def test_go_motor_command_and_native_queries(self):
        cmd = sdk.MotorCmd()
        cmd.motorType = sdk.MotorType.GO_M8010_6
        cmd.mode = sdk.queryMotorMode(cmd.motorType, sdk.MotorMode.FOC)
        cmd.id = 0
        cmd.q = 0.0
        cmd.dq = 6.28 * sdk.queryGearRatio(cmd.motorType)
        cmd.kp = 0.0
        cmd.kd = 0.01
        cmd.tau = 0.0

        self.assertEqual(cmd.motorType, sdk.MotorType.GO_M8010_6)
        self.assertEqual(cmd.mode, 1)
        self.assertAlmostEqual(cmd.dq, 39.7524, places=4)
        self.assertAlmostEqual(cmd.kd, 0.01, places=6)

        data = sdk.MotorData()
        data.motorType = cmd.motorType
        self.assertEqual(data.motorType, sdk.MotorType.GO_M8010_6)
        self.assertFalse(data.correct)


if __name__ == "__main__":
    unittest.main()
