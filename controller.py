import pystk
import math
import numpy as np


def control(aim_point, current_vel, skid=False):
    """
    Set the Action for the low-level controller
    :param aim_point: Aim point, in screen coordinate frame [-1..1]
    :param current_vel: Current velocity of the kart
    :return: a pystk.Action (set acceleration, brake, steer, drift)
    """
    action = pystk.Action()

    """
    Your code here
    Hint: Use action.acceleration (0..1) to change the velocity. Try targeting a target_velocity (e.g. 20).
    Hint: Use action.brake to True/False to brake (optionally)
    Hint: Use action.steer to turn the kart towards the aim_point, clip the steer angle to -1..1
    Hint: You may want to use action.drift=True for wide turns (it will turn faster)
    """
    target_velocity = 25
    x = aim_point[0]
    y = aim_point[1]
    
    action.steer = 32*x
    if abs(action.steer) > 22:
        action.drift = True
    else:
        action.drift = False

    if y > 0:
        action.brake = True

    else:
        action.brake = False

    if current_vel < target_velocity and action.drift == False:
        action.acceleration = 1.0
    else:
        action.acceleration = 0

    if abs(x) <= 0.1 and y < -0.15:
        action.nitro = True
    else:
        action.nitro = False

    return action




if __name__ == '__main__':
    from .utils import PyTux
    from argparse import ArgumentParser

    def test_controller(args):
        import numpy as np
        pytux = PyTux()
        for t in args.track:
            steps, how_far = pytux.rollout(t, control, max_frames=1000, verbose=args.verbose)
            print(steps, how_far)
        pytux.close()


    parser = ArgumentParser()
    parser.add_argument('track', nargs='+')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    test_controller(args)