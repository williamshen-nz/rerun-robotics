# Changelog

### v0.0.5

Fixed the Panda demo.

**Breaking Changes**

The signature and behavior of `rerun_robotics.rerun_urdf.log_scene` has been changed

- The `timeless` parameter has been
  renamed `static`, as `timeless` has been deprecated by rerun as of version `0.16.0`.
- We log the mesh as `static=True`, so we don't unnecessarily log it again in the future.
