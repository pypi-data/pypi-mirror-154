from dataclasses import field

import marshmallow_dataclass
from marshmallow import pre_load

from datagen.modalities.textual.common.ndarray import NumpyArray


@marshmallow_dataclass.dataclass
class Keypoints:
    coords_2d: NumpyArray = field(repr=False)
    coords_3d: NumpyArray = field(repr=False)
    is_visible: NumpyArray = field(repr=False)

    @pre_load
    def rename_fields(self, in_data: dict, **kwargs) -> dict:
        in_data["coords_2d"] = (in_data.pop("keypoints_2d_coordinates"),)
        in_data["coords_3d"] = in_data.pop("keypoints_3d_coordinates")
        in_data["is_visible"] = list(map(lambda s: s == "true", in_data.pop("is_visible")))
        return in_data


@marshmallow_dataclass.dataclass
class SceneKeypoints:
    standard: Keypoints
    dense: Keypoints
