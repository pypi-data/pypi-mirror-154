import numpy
from ewokscore import Task
from .worker import persistent_worker
from . import utils

__all__ = ["Integrate1D"]


class Integrate1D(
    Task,
    input_names=["image", "detector", "geometry", "energy"],
    optional_input_names=[
        "monitor",
        "reference",
        "mask",
        "integration_options",
        "worker_options",
    ],
    output_names=["x", "y", "yerror", "xunits", "info"],
):
    """The intensity will be normalized to the reference:

    .. code:

        Inorm = I / monitor * reference
    """

    def run(self):
        raw_data = utils.get_image(self.inputs.image)
        normalization_factor, monitor, reference = self.get_normalization()
        worker_options = self.get_worker_options()
        integration_options = self.get_integration_config()
        with persistent_worker(worker_options, integration_options) as worker:
            pattern = worker.process(
                raw_data, normalization_factor=normalization_factor
            )
            pattern = pattern.T
            if len(pattern) == 3:
                self.outputs.x, self.outputs.y, self.outputs.yerror = pattern
            else:
                self.outputs.x, self.outputs.y = pattern
                self.outputs.yerror = numpy.full_like(self.outputs.y, numpy.nan)

            self.outputs.xunits = integration_options["unit"]

            info = {
                "detector": self.inputs.detector,
                "energy": self.inputs.energy,
                "geometry": self.inputs.geometry,
            }
            info["monitor"] = monitor
            info["reference"] = reference
            self.outputs.info = info

    def get_integration_config(self) -> dict:
        geometry = utils.data_from_storage(self.inputs.geometry)
        utils.validate_geometry(geometry)
        integration_options = self.inputs.integration_options
        if integration_options:
            config = {**integration_options, **geometry}
        else:
            config = dict(geometry)
        config.setdefault("unit", "2th_deg")
        config["detector"] = utils.data_from_storage(self.inputs.detector)
        config["wavelength"] = utils.energy_wavelength(self.inputs.energy)
        if not self.missing_inputs.mask:
            config["mask"] = utils.get_image(utils.data_from_storage(self.inputs.mask))
        return config

    def get_worker_options(self) -> dict:
        if self.inputs.worker_options:
            return utils.data_from_storage(self.inputs.worker_options)
        return dict()

    def get_normalization(self) -> tuple:
        # Inorm = I / normalization_factor
        monitor = self.inputs.monitor
        reference = self.inputs.reference
        if utils.is_data(reference):
            if not utils.is_data(monitor):
                raise ValueError("provide a 'monitor' when providing a 'reference'")
            monitor = utils.get_data(monitor)
            reference = utils.get_data(reference)
            normalization_factor = monitor / reference
        else:
            if utils.is_data(monitor):
                monitor = utils.get_data(monitor)
            else:
                monitor = float("nan")
            reference = float("nan")
        normalization_factor = monitor / reference
        if numpy.isnan(normalization_factor):
            normalization_factor = None
        return normalization_factor, monitor, reference
