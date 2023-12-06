"""
Modified from: https://github.com/rerun-io/rerun/blob/main/examples/python/ros_node/rerun_urdf.py
"""
from typing import Union, cast

import numpy as np
import rerun as rr
import trimesh

from rerun_robotics.utils import clean_rerun_path


def log_scene(
    scene: trimesh.Scene, node: str, path: Union[str, None] = None, timeless: bool = False, add_mesh: bool = True
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
                timeless=timeless,
            )

        # Log this node's mesh, if it has one.
        mesh = cast(trimesh.Trimesh, scene.geometry.get(node_data[1])) if add_mesh else None
        if mesh:
            # If trimesh gives us a single vertex color for the entire mesh, we can interpret that
            # as an albedo factor for the whole primitive.
            vertex_colors = None
            mesh_material = None
            try:
                colors = mesh.visual.to_color().vertex_colors
                if len(colors) == 4:
                    # If trimesh gives us a single vertex color for the entire mesh, we can interpret that
                    # as an albedo factor for the whole primitive.
                    mesh_material = rr.Material(albedo_factor=np.array(colors))
                else:
                    vertex_colors = colors
            except Exception:
                pass

            rr.log(
                path,
                rr.Mesh3D(
                    vertex_positions=mesh.vertices,
                    vertex_colors=vertex_colors,
                    vertex_normals=mesh.vertex_normals,
                    indices=mesh.faces,
                    mesh_material=mesh_material,
                ),
                timeless=timeless,
            )

    if children:
        for child in children:
            log_scene(scene, child, path, timeless)
