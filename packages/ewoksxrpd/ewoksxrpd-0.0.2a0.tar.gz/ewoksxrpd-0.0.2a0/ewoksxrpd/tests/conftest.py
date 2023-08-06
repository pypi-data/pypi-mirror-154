import os
import h5py
import pytest
import numpy
from silx.io.dictdump import dicttonx

import pyFAI.azimuthalIntegrator
import pyFAI.detectors
from ewoksorange.canvas.handler import OrangeCanvasHandler
from ewoksorange.tests.conftest import qtapp  # noqa F401

from .utils import Calibration, Measurement, Setup, xPattern, yPattern
from .utils import measurement, calibration


@pytest.fixture(scope="session")
def setup1() -> Setup:
    # Detector size is approx. 0.18 x 0.18 m
    geometry = {
        "dist": 10e-2,  # 10 cm
        "poni1": 10e-2,  # 10 cm
        "poni2": 10e-2,  # 10 cm
        "rot1": numpy.radians(10),  # 10 deg
        "rot2": 0,  # 0 deg
        "rot3": 0,  # 0 deg
    }
    return Setup(detector="Pilatus1M", energy=12, geometry=geometry)


@pytest.fixture(scope="session")
def setup2(setup1) -> Setup:
    # setup1 with detector shifted 5 cm backwards
    geometry = dict(setup1.geometry)
    geometry["dist"] += 5e-2
    assert geometry["dist"] > 0
    return Setup(detector=setup1.detector, energy=setup1.energy, geometry=geometry)


@pytest.fixture(scope="session")
def aiSetup1(setup1: Setup) -> pyFAI.azimuthalIntegrator.AzimuthalIntegrator:
    detector = pyFAI.detectors.detector_factory(setup1.detector)
    return pyFAI.azimuthalIntegrator.AzimuthalIntegrator(
        detector=detector, **setup1.geometry
    )


@pytest.fixture(scope="session")
def aiSetup2(setup2: Setup) -> pyFAI.azimuthalIntegrator.AzimuthalIntegrator:
    detector = pyFAI.detectors.detector_factory(setup2.detector)
    return pyFAI.azimuthalIntegrator.AzimuthalIntegrator(
        detector=detector, **setup2.geometry
    )


def linspace(low_limit, high_limit, n):
    half_bin = (high_limit - low_limit) / (2 * n)
    return numpy.linspace(low_limit + half_bin, high_limit - half_bin, n)


@pytest.fixture(scope="session")
def xSampleA() -> xPattern:
    x = linspace(0, 30, 1024)
    return xPattern(x=x, low_limit=0, high_limit=30, units="2th_deg")


@pytest.fixture(scope="session")
def ySampleA(xSampleA: xPattern) -> yPattern:
    x = xSampleA.x
    y = numpy.zeros(x.size)
    peaks = list()
    s = 0.5
    for ufrac in [0.1, 0.4, 0.7]:
        A = 100
        u = x[0] + ufrac * (x[-1] - x[0])
        y += (
            A
            * numpy.exp(-((x - u) ** 2) / (2 * s**2))
            / (s * numpy.sqrt(2 * numpy.pi))
        )
        peaks.append((A, u, s))
    return yPattern(y=y, monitor=1000, theory=peaks)


@pytest.fixture(scope="session")
def xSampleB() -> xPattern:
    x = linspace(0, 180, 1024)
    return xPattern(x=x, low_limit=0, high_limit=180, units="2th_deg")


@pytest.fixture(scope="session")
def ySampleB(xSampleB: xPattern) -> yPattern:
    y = numpy.full(xSampleB.x.size, 10)
    return yPattern(y=y, monitor=1000, theory=10)


@pytest.fixture(scope="session")
def imageSetup1SampleA(
    aiSetup1: pyFAI.azimuthalIntegrator.AzimuthalIntegrator,
    xSampleA: xPattern,
    ySampleA: yPattern,
) -> Measurement:
    return measurement(aiSetup1, xSampleA, ySampleA, mult=2)


@pytest.fixture(scope="session")
def imageSetup2SampleA(
    aiSetup2: pyFAI.azimuthalIntegrator.AzimuthalIntegrator,
    xSampleA: xPattern,
    ySampleA: yPattern,
) -> Measurement:
    return measurement(aiSetup2, xSampleA, ySampleA, mult=2)


@pytest.fixture(scope="session")
def image1Setup1SampleB(
    aiSetup1: pyFAI.azimuthalIntegrator.AzimuthalIntegrator,
    xSampleB: xPattern,
    ySampleB: yPattern,
) -> Measurement:
    return measurement(aiSetup1, xSampleB, ySampleB, mult=2)


@pytest.fixture(scope="session")
def image2Setup1SampleB(
    aiSetup1: pyFAI.azimuthalIntegrator.AzimuthalIntegrator,
    xSampleB: xPattern,
    ySampleB: yPattern,
) -> Measurement:
    return measurement(aiSetup1, xSampleB, ySampleB, mult=3)


@pytest.fixture(scope="session")
def imageSetup1Calibrant1(
    aiSetup1: pyFAI.azimuthalIntegrator.AzimuthalIntegrator,
    setup1: Setup,
) -> Calibration:
    return calibration("LaB6", aiSetup1, setup1)


@pytest.fixture(scope="session")
def imageSetup2Calibrant1(
    aiSetup2: pyFAI.azimuthalIntegrator.AzimuthalIntegrator,
    setup2: Setup,
) -> Calibration:
    return calibration("LaB6", aiSetup2, setup2)


def next_scan_number(filename) -> int:
    if not os.path.exists(filename):
        return 1
    with h5py.File(filename, "r") as h5file:
        return int(max(map(float, h5file.keys()))) + 1


def singledistance_calibration_data(
    tmpdir, imageSetup1Calibrant1, setup1, imageSetup2Calibrant1, setup2
):
    mcalib_images = list()
    mcalib_positions = list()
    images = [
        (
            imageSetup1Calibrant1.image,
            setup1.geometry["dist"] * 100,
        ),
        (
            imageSetup2Calibrant1.image,
            setup2.geometry["dist"] * 100,
        ),
    ]
    data = {"@NX_class": "NXroot", "@default": "1.1"}
    filename = str(tmpdir / "calib.h5")
    for i, (image, detz) in enumerate(images, 1):
        data[f"{i}.1"] = {
            "@default": "plotselect",
            "instrument": {
                "@NX_class": "NXinstrument",
                "pilatus1": {
                    "@NX_class": "NXdetector",
                    "data": image,
                },
                "positioners": {"detz": detz, "detz@units": "cm"},
            },
            "title": "sct 1",
            "measurement": {">pilatus1": "../instrument/pilatus1/data"},
            "plotselect": {
                "@NX_class": "NXdata",
                "@signal": "data",
                ">data": "../instrument/pilatus1/data",
            },
        }
        mcalib_images.append(f"silx://{filename}?path=/{i}.1/measurement/pilatus1")
        mcalib_positions.append(
            f"silx://{filename}?path=/{i}.1/instrument/positioners/detz"
        )
    dicttonx(data, filename, update_mode="add")

    return mcalib_images, mcalib_positions


@pytest.fixture(scope="session")
def ewoks_orange_canvas(qtapp):  # noqa F811
    with OrangeCanvasHandler() as handler:
        yield handler
