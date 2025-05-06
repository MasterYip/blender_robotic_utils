import os
from blender_utils.animation.robot_animator import RobotAnimator, RobotAnimatorConfig, SwingTrajAnimator

# Directory Management
try:
    # Run in Terminal
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
except:
    # Run in ipykernel & interactive
    ROOT_DIR = os.getcwd()


def load_robot_animation():
    # Load configuration
    print("Loading cfg.")
    config = RobotAnimatorConfig(os.path.join(ROOT_DIR, 'robot_animator_cfg.yaml'))
    animator = RobotAnimator(config)
    # Load joint states
    file = os.path.join(ROOT_DIR, 'joint_states.csv')
    animator.load_animation(file)
    print("Keyframes set successfully.")


def load_swingtraj_animation():
    # Load swing trajectory
    traj_file = os.path.join(ROOT_DIR, 'swing_traj.csv')
    animator = SwingTrajAnimator(traj_file)
    print("Swing trajectory loaded successfully.")


if __name__ == "<run_path>":

    # NOTE: Please import robot before executing.
    # load_robot_animation()
    load_swingtraj_animation()
