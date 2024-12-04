# Changelog

### v0.0.7

- Removed open3d dependency, thanks [@abhishek47kashyap](https://github.com/abhishek47kashyap) for spotting this.


### v0.0.6

- Fixed bugs for `rerun-sdk>=0.18.0` after function signatures changed.
- Log invisible transform arrows.

**Breaking Changes**

- The rerun API has changed significantly, so you should upgrade `rerun-sdk` in conjunction with `rerun-robotics`.

### v0.0.5

Fixed the Panda demo.

**Breaking Changes**

The signature and behavior of `rerun_robotics.rerun_urdf.log_scene` has been changed

- The `timeless` parameter has been
  renamed `static`, as `timeless` has been deprecated by rerun as of version `0.16.0`.
- We log the mesh as `static=True`, so we don't unnecessarily log it again in the future.
