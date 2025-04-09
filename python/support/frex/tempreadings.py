"""Determine the the temperature readings as per the lm sensors package."""

import shutil
import subprocess

class TemperatureReadings:

    def __init__(self) -> None:
        self._sensors = shutil.which('sensors')
        self._tr = None

    def __enter__(self):
        try:
            assert self._sensors is not None
        except AssertionError as exc:
            self._logger.log(logging.ERROR, 'lm sensors package seems missing from system')
            raise FileNotFoundError from exc
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        return False

    def __call__(self) -> float:
        self._tr = subprocess.check_output(r'sensors | rg "(CPU|MB)\sTemperature"', shell=True)

    def __repr__(self) -> object:
        _me = type(self).__name__
        return f"{_me}()"

    def __str__(self) -> str:
        try:
            assert self._tr is not None
        except AssertionError as exc:
            return 'Temperature readings not avalable'
        return self._tr.decode().rstrip()

if __name__ == '__main__':

    pass
