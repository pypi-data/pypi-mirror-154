from __future__ import annotations

import dataclasses
import warnings

import pyo

import walkman


class InvalidInputIndexWarning(Warning):
    pass


@dataclasses.dataclass
class ConvolutionReverb(walkman.ModuleWithDecibel):
    """"""

    impulse_path: str = ""

    def setup_pyo_object(self):
        super().setup_pyo_object()

        self._balance_signal_to = pyo.SigTo(1)
        try:
            pyo_input = self.input_provider.audio_input_list[0]
        except IndexError:
            warnings.warn(
                f"Found no audio inputs! Using {self.get_name()} module is useless "
                "without any audio input!"
            )
            pyo_input = pyo.Sig(0)
        self._convolution_reverb = pyo.CvlVerb(
            pyo_input,
            self.impulse_path,
            mul=self._decibel_signal_to,
            bal=self._balance_signal_to,
        ).stop()

        self.internal_pyo_object_list.extend(
            [self._convolution_reverb, self._balance_signal_to]
        )

    def _initialise(
        self,
        input_index: int = 0,
        decibel: walkman.Parameter = -6,  # type: ignore
        balance: walkman.Parameter = 1,  # type: ignore
    ):
        super()._initialise(decibel=decibel)

        try:
            pyo_input = self.input_provider.audio_input_list[input_index]
        except IndexError:
            warnings.warn(
                f"There is no input with input_index = '{input_index}'!"
                f" WALKMAN ignored current cue settings for {self.get_name()}.",
                InvalidInputIndexWarning,
            )

        else:
            self._convolution_reverb.setInput(pyo_input)
            self._balance_signal_to.setValue(balance.value)

    @property
    def _pyo_object(self) -> pyo.PyoObject:
        return self._convolution_reverb
