import numpy as np
import open3d as o3d
import rerun as rr


def clean_rerun_path(path: str) -> str:
    path = path.replace(".", "_")
    path = path.lstrip("/")
    return path


def o3d_point_cloud_to_rerun(pcd: o3d.geometry.PointCloud, point_size: float = 0.001) -> rr.Points3D:
    positions = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    return rr.Points3D(positions, colors=colors, radii=point_size)
