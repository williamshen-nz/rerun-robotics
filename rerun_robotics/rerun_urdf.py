"""
Modified from: https://github.com/rerun-io/rerun/blob/main/examples/python/ros_node/rerun_urdf.py
"""
from typing import Union, cast

import rerun as rr
import trimesh

from rerun_robotics.utils import clean_rerun_path, trimesh_to_rerun


def log_scene(
    scene: trimesh.Scene, node: str, path: Union[str, None] = None, static: bool = False, add_mesh: bool = True
) -> None:
    """Log a trimesh scene to rerun."""
    path = path + "/" + node if path else node
    path = clean_rerun_path(path)

    parent = scene.graph.transforms.parents.get(node)
    children = scene.graph.transforms.children.get(node)

    node_data = scene.graph.get(frame_to=node, frame_from=parent)

    if node_data:
        # Log the transform between this node and its direct parent (if it has one!).
        if parent:
            # We assume 4x4 homogeneous transforms in column-vector (i.e., last column is translation + 1.0).
            world_from_mesh = node_data[0]
            rr.log(
                path,
                rr.Transform3D(
                    translation=world_from_mesh[:3, 3],
                    mat3x3=world_from_mesh[:3, :3],
                ),
                static=static,
            )

        # Log this node's mesh, if it has one.
        if add_mesh:
            mesh = cast(trimesh.Trimesh, scene.geometry.get(node_data[1]))
            # Log mesh as static so we can reuse it. Re-logging it has high costs
            if mesh:
                rr.log(path, trimesh_to_rerun(mesh), static=True)

    if children:
        for child in children:
            log_scene(scene, child, path, static, add_mesh)
