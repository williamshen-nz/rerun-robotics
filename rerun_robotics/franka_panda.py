import os
from typing import Sequence

import numpy as np
import rerun as rr
from pybullet_data import getDataPath
from yourdfpy import URDF

from rerun_robotics.rerun_urdf import log_scene

# We load the pybullet panda
panda_assets_dir = os.path.join(getDataPath(), "franka_panda")
panda_urdf_path = os.path.join(panda_assets_dir, "panda.urdf")

panda_neutral_joint_positions = (
    -0.000000,
    -0.785398,
    0.000000,
    -2.356194,
    0.000000,
    1.570796,
    0.785398,
    0.04,
)


def locate_franka_asset(fname: str) -> str:
    if not fname.startswith("package://"):
        raise ValueError(f"Expected package://, got {fname}")
    fname = fname.replace("package://", "")
    asset_path = os.path.join(panda_assets_dir, fname)
    return asset_path


class PandaRerun:
    """Helper class for commanding the Panda in rerun."""

    def __init__(self, urdf: URDF):
        self._urdf = urdf
        rr.log("panda_link0", rr.ViewCoordinates.RIGHT_HAND_Z_UP, static=True)
        log_scene(scene=urdf.scene, node="panda_link0", path="panda", static=False, add_mesh=True)

    @property
    def joint_positions(self) -> np.ndarray:
        return self._urdf.cfg

    def set_joint_positions(self, joint_positions: Sequence[float]) -> None:
        if len(joint_positions) != self._urdf.num_actuated_joints:
            raise ValueError(
                f"We only support setting 7 arm joints + 1 gripper joints, not {len(joint_positions)} joints"
            )
        self._urdf.update_cfg(joint_positions)
        log_scene(scene=self._urdf.scene, node="panda_link0", path="panda", static=False, add_mesh=False)


def load_franka_panda(initial_joint_positions=panda_neutral_joint_positions) -> PandaRerun:
    """
    Load franka to rerun.
    Modified from: https://github.com/rerun-io/rerun/blob/main/examples/python/ros_node/rerun_urdf.py
    """
    urdf = URDF.load(panda_urdf_path, filename_handler=locate_franka_asset)
    panda = PandaRerun(urdf)
    panda.set_joint_positions(initial_joint_positions)
    return panda
