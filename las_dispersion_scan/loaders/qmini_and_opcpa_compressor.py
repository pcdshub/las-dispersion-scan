import os

from ophyd import Component as Cpt
from ophyd import DerivedSignal, Signal
from ophyd.pseudopos import real_position_argument
from ophyd.signal import AttributeSignal
from pcdsdevices.pseudopos import SyncAxis

from ..devices import EllLinear, Qmini

qmini_prefix = os.environ.get("QMINI_PREFIX", "LAS:LLN:QMINI:01")
stage_prefix = os.environ.get("MOTOR_PREFIX", "IOC:TST:DScan:")
upstream_port = os.environ.get("UPSTREAM_PORT", "0")
upstream_channel = os.environ.get("UPSTREAM_CHANNEL", "1")
downstream_port = os.environ.get("DOWNSTREAM_PORT", "0")
downstream_channel = os.environ.get("DOWNSTREAM_CHANNEL", "1")
qmini_name = os.environ.get("QMINI_NAME", "las_lln_spec_01")
stage_name = os.environ.get("MOTOR_NAME", "las_lln_ell_01")
motor_units = os.environ.get("MOTOR_UNITS", "mm")

spectrometer = Qmini(qmini_prefix, name=qmini_name)


class DualElliptec(SyncAxis):
    upstream = Cpt(
        EllLinear,
        "",
        port=upstream_port,
        channel=upstream_channel,
        atol=0.05,
        motor_units=motor_units,
        use_retries=True,
    )
    downstream = Cpt(
        EllLinear,
        "",
        port=downstream_port,
        channel=downstream_channel,
        atol=0.05,
        motor_units=motor_units,
        use_retries=True,
    )

    user_setpoint = Cpt(AttributeSignal, attr="_user_setpoint_change")
    user_readback = Cpt(DerivedSignal, derived_from="sync.readback")

    scale_downstream = Cpt(Signal, value=1.0)
    scale_upstream = Cpt(Signal, value=1.0)
    offset_downstream = Cpt(Signal, value=0.0)
    offset_upstream = Cpt(Signal, value=0.0)

    @property
    def scales(self) -> dict[str, float]:
        try:
            return {
                "downstream": self.scale_downstream.get(),
                "upstream": self.scale_upstream.get(),
            }
        except AttributeError:
            # TODO: instantiation order means this has to be available before the components
            return {"downstream": 1.0, "upstream": 1.0}

    @scales.setter
    def scales(self, values):
        if not hasattr(self, "scale_downstream"):
            # TODO: instantiation order means this has to be available before the components
            return
        self.scale_downstream.put(values["downstream"])
        self.scale_upstream.put(values["upstream"])

    @property
    def offsets(self) -> dict[str, float]:
        try:
            return {
                "downstream": self.offset_downstream.get(),
                "upstream": self.offset_upstream.get(),
            }
        except AttributeError:
            # TODO: instantiation order means this has to be available before the components
            return {"downstream": 0.0, "upstream": 0.0}

    @offsets.setter
    def offsets(self, values):
        if not hasattr(self, "scale_downstream"):
            # TODO: instantiation order means this has to be available before the components
            return
        self.offset_downstream.put(values["downstream"])
        self.offset_upstream.put(values["upstream"])

    @property
    def _user_setpoint_change(self) -> float:
        try:
            return self.sync.target
        except Exception:
            return 0.0

    @_user_setpoint_change.setter
    def _user_setpoint_change(self, value: float):
        self.sync.move(value, wait=False)

    @property
    def egu(self) -> str:
        return "mm"

    @property
    def precision(self) -> int:
        return 3

    @real_position_argument
    def inverse(self, real_pos):
        """
        Calculate where the sync motor is based on the first real motor.
        The calculation is:
        1. Subtract the offset
        2. Divide by the scale
        """
        self._setup_offsets()
        attr1 = real_pos._fields[0]
        pos1 = real_pos[0]
        calc1 = self.inverse_single(attr1, pos1)
        attr2 = real_pos._fields[1]
        pos2 = real_pos[1]
        calc2 = self.inverse_single(attr2, pos2)
        calc = (calc1 + calc2) / 2
        return self.PseudoPosition(sync=calc)


stage = DualElliptec(stage_prefix, name=stage_name, concurrent=True)

stage.warn_deadband = 0.01
