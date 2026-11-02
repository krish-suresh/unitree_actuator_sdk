"""Run in a separate environment after installing the package with uv."""

from importlib.metadata import distribution
from pathlib import Path
import platform
import sysconfig
import unittest

import unitree_actuator_sdk as sdk


class InstalledPackageTest(unittest.TestCase):
    def test_import_comes_from_installed_distribution(self):
        dist = distribution("unitree-actuator-sdk")
        expected = dist.locate_file(
            "unitree_actuator_sdk" + sysconfig.get_config_var("EXT_SUFFIX")
        )
        self.assertTrue(expected.is_file())
        self.assertEqual(Path(sdk.__file__).resolve(), expected.resolve())

    def test_native_library_is_loaded_from_installation(self):
        name = {
            "x86_64": "libUnitreeMotorSDK_Linux64.so",
            "aarch64": "libUnitreeMotorSDK_Arm64.so",
        }[platform.machine().lower()]
        expected = Path(sdk.__file__).resolve().parent / "unitree_actuator_sdk.libs" / name
        self.assertTrue(expected.is_file())
        loaded = {
            line.split(maxsplit=5)[-1].strip().replace("\\040", " ")
            for line in Path("/proc/self/maps").read_text().splitlines()
            if name in line
        }
        self.assertEqual(loaded, {str(expected.resolve())})

    def test_motor_api_without_hardware(self):
        cmd = sdk.MotorCmd()
        cmd.motorType = sdk.MotorType.GO_M8010_6
        cmd.mode = sdk.queryMotorMode(cmd.motorType, sdk.MotorMode.FOC)
        cmd.q = 1.25
        self.assertEqual(cmd.mode, 1)
        self.assertAlmostEqual(cmd.q, 1.25)
        self.assertAlmostEqual(sdk.queryGearRatio(cmd.motorType), 6.33, places=5)
        self.assertFalse(sdk.MotorData().correct)


if __name__ == "__main__":
    unittest.main()
