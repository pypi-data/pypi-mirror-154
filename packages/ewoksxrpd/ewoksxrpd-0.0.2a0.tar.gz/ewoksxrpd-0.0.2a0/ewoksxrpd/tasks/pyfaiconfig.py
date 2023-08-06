import json
from ewokscore import Task
from .utils import energy_wavelength
from pyFAI.io.ponifile import PoniFile

__all__ = ["PyFaiConfig"]


class PyFaiConfig(
    Task,
    optional_input_names=[
        "filename",
        "energy",
        "geometry",
        "mask",
        "detector",
        "calibrant",
    ],
    output_names=["energy", "geometry", "detector", "calibrant", "mask"],
):
    def run(self):
        adict = self.from_file()
        wavelength = adict.get("wavelength", None)
        if wavelength is not None:
            self.outputs.energy = energy_wavelength(wavelength)
        geometry = {
            k: adict[k]
            for k in ["dist", "poni1", "poni2", "rot1", "rot2", "rot3"]
            if k in adict
        }
        if len(geometry) != 6:
            geometry = self.inputs.geometry
        self.outputs.geometry = geometry
        self.outputs.detector = adict.get("detector", self.inputs.detector)
        self.outputs.calibrant = self.inputs.calibrant
        self.outputs.mask = self.inputs.mask

    def from_file(self) -> dict:
        filename = self.inputs.filename
        if not filename:
            return dict()
        if filename.endswith(".json"):
            with open(filename, "r") as fp:
                return json.load(fp)
        else:
            return PoniFile(filename).as_dict()
