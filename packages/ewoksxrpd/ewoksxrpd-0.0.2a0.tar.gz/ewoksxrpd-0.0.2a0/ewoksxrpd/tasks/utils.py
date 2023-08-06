from typing import Dict, Iterable, Mapping, Sequence, Tuple, List, Union
from numbers import Number
from contextlib import contextmanager

from numpy.typing import ArrayLike
import numpy
import pyFAI.units
import pyFAI.calibrant

from silx.io.url import DataUrl
import silx.io.h5py_utils
from silx.utils.retry import RetryError
from silx.io.utils import get_data as _get_data


def energy_wavelength(x):
    """keV to Angstrom and vice versa"""
    return pyFAI.units.hc * 1e-10 / x


GEOMETRY_PARAMETERS = {"dist", "poni1", "poni2", "rot1", "rot2", "rot3"}


def validate_geometry(geometry: dict):
    required = GEOMETRY_PARAMETERS
    existing = set(geometry.keys())
    missing = required - existing
    if missing:
        raise ValueError(f"geometry has missing parameters {sorted(missing)}")
    unexpected = existing - required
    if unexpected:
        raise ValueError(f"geometry has unexpected parameters {sorted(unexpected)}")


def calibrant_ring_labels(calibrant: pyFAI.calibrant.Calibrant) -> List[str]:
    labels = list()
    i = 0
    with open(calibrant._filename, "r") as fd:
        for line in fd:
            if line.startswith("#"):
                continue
            line = line.rstrip()
            label = line.rpartition("#")[-1]
            if not label or label in labels:
                label = f"ring{i}"
            label = label.strip()
            labels.append(label)
            i += 1
    return labels


def points_to_rings(
    points: Iterable[Tuple[float, float, int]], calibrant: pyFAI.calibrant.Calibrant
) -> Dict[int, Dict[str, list]]:
    rings = dict()
    labels = calibrant_ring_labels(calibrant)
    for p0, p1, i in points:
        i = int(i)
        try:
            label = labels[i]
        except IndexError:
            label = f"ring{i}"
        adict = rings.get(label)
        if adict:
            adict["p0"].append(p0)
            adict["p1"].append(p1)
        else:
            rings[label] = {"p0": [p0], "p1": [p1]}
    return rings


def h5url_parse(url: str) -> Tuple[str, str, Tuple]:
    obj = DataUrl(url)
    filename = str(obj.file_path())
    h5path = obj.data_path()
    if h5path is None:
        h5path = "/"
    idx = obj.data_slice()
    if idx is None:
        idx = tuple()
    return filename, h5path, idx


@contextmanager
def h5context(filename: str, h5path: str, **openargs):
    with silx.io.h5py_utils.File(filename, **openargs) as f:
        yield f[h5path]


@silx.io.h5py_utils.retry()
def get_hdf5_data(filename: str, h5path: str, idx=None, **options) -> numpy.ndarray:
    with h5context(filename, h5path, **options) as dset:
        if is_bliss_file(dset):
            if "end_time" not in get_nxentry(dset):
                raise RetryError
        if idx is None:
            idx = tuple()
        return dset[idx]


def is_bliss_file(h5item):
    return h5item.file.attrs.get("creator", "").lower() == "bliss"


def get_nxentry(h5item):
    parts = [s for s in h5item.name.split("/") if s]
    if parts:
        return h5item.file[parts[0]]
    else:
        raise ValueError("HDF5 item must be part of am NXentry")


def get_data(
    data: Union[str, ArrayLike, Number], gui: bool = False, **options
) -> Union[numpy.ndarray, Number]:
    if isinstance(data, str):
        if data.endswith(".h5") or data.endswith(".nx"):
            filename, h5path, idx = h5url_parse(data)
            if gui:
                return get_hdf5_data(
                    filename, h5path, idx=idx, retry_timeout=0, **options
                )
            else:
                return get_hdf5_data(filename, h5path, idx=idx, **options)
        else:
            return _get_data(data)
    elif isinstance(data, (Sequence, Number, numpy.ndarray)):
        return data
    else:
        raise TypeError(type(data))


def get_image(*args, **kwargs) -> numpy.ndarray:
    data = get_data(*args, **kwargs)
    return numpy.atleast_2d(numpy.squeeze(data))


def is_data(data):
    if isinstance(data, (numpy.ndarray, Number)):
        return True
    if isinstance(data, (str, list)) and data:
        return True
    return False


def data_from_storage(data, remove_numpy=True):
    if isinstance(data, numpy.ndarray):
        if not remove_numpy:
            return data
        elif data.ndim == 0:
            return data.item()
        else:
            return data.tolist()
    elif isinstance(data, Mapping):
        return {
            k: data_from_storage(v, remove_numpy=remove_numpy)
            for k, v in data.items()
            if not k.startswith("@")
        }
    else:
        return data
