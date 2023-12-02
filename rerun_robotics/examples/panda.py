import numpy as np
import rerun as rr

from rerun_robotics import load_franka_panda


def panda_demo():
    print("Running Panda Demo - you will see the Panda arm jerk around randomly")
    rr.init("panda_demo", spawn=True)

    panda = load_franka_panda()

    for idx in range(100):
        rr.set_time_sequence("time", idx)
        current_joint_positions = panda.joint_positions

        # Note: these may violate joint limits
        delta = np.random.uniform(-0.03, 0.03, size=len(current_joint_positions))
        target_joint_positions = current_joint_positions + delta

        # Set gripper position to be at most 0.04 and max 0.0
        target_joint_positions[-1] = min(0.04, target_joint_positions[-1])
        target_joint_positions[-1] = max(0.0, target_joint_positions[-1])

        # Update panda
        panda.set_joint_positions(target_joint_positions)


if __name__ == "__main__":
    panda_demo()
