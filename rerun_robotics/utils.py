import numpy as np
import open3d as o3d
import rerun as rr
import trimesh


def clean_rerun_path(path: str) -> str:
    path = path.replace(".", "_")
    path = path.lstrip("/")
    return path


def o3d_point_cloud_to_rerun(pcd: o3d.geometry.PointCloud, point_size: float = 0.001) -> rr.Points3D:
    positions = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    return rr.Points3D(positions, colors=colors, radii=point_size)


def trimesh_to_rerun(geometry: trimesh.PointCloud | trimesh.Trimesh):
    if isinstance(geometry, trimesh.PointCloud):
        return rr.Points3D(positions=geometry.vertices, colors=geometry.colors)
    elif isinstance(geometry, trimesh.Trimesh):
        # If trimesh gives us a single vertex color for the entire mesh, we can interpret that
        # as an albedo factor for the whole primitive.
        mesh = geometry
        vertex_colors = None
        mesh_material = None
        if hasattr(mesh.visual, "vertex_colors"):
            colors = mesh.visual.vertex_colors
            if len(colors) == 4:
                # If trimesh gives us a single vertex color for the entire mesh, we can interpret that
                # as an albedo factor for the whole primitive.
                mesh_material = rr.Material(albedo_factor=np.array(colors))
            else:
                vertex_colors = colors
        elif hasattr(mesh.visual, "material"):
            # There are other properties in trimesh material, but rerun only supports albedo
            trimesh_material = mesh.visual.material
            mesh_material = rr.Material(albedo_factor=trimesh_material.main_color)
        else:
            raise NotImplementedError("Couldn't determine mesh color or material")

        return rr.Mesh3D(
            vertex_positions=mesh.vertices,
            vertex_colors=vertex_colors,
            vertex_normals=mesh.vertex_normals,
            triangle_indices=mesh.faces,
            mesh_material=mesh_material,
        )
    else:
        raise NotImplementedError(f"Unsupported trimesh geometry: {type(geometry)}")
