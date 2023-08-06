import pytest

from bmi_wavewatch3 import BmiWaveWatch3


@pytest.mark.skip("slow")
def test_initialize(datadir):
    bmi = BmiWaveWatch3()
    bmi.initialize(datadir / "config.toml")
