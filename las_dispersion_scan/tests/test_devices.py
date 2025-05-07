import logging

import pytest

from las_dispersion_scan.devices import (
    DscanStatus,
    FakeDScanStatus,
    FakeMotor,
    FakeSpectrometer,
    Spectrometer,
    Stage,
)

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "Device,Type,",
    [
        (FakeDScanStatus, DscanStatus),
        (FakeMotor, Stage),
        (FakeSpectrometer, Spectrometer),
    ],
)
def test_fake_devices(Device, Type):
    device_instance = Device("MY:PREFIX", name="my_device")
    assert isinstance(device_instance, Type)
