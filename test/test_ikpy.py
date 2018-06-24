import ikpy
import numpy as np
from ikpy import plot_utils
import matplotlib.pyplot as plt


def test():
    my_chain = ikpy.chain.Chain.from_urdf_file("poppy_ergo.URDF")
    target_vector = [ 0.1, -0.2, 0.1]
    target_frame = np.eye(4)
    target_frame[:3, 3] = target_vector
    print("The angles of each joints are : ", my_chain.inverse_kinematics(target_frame))
    ax = plot_utils.init_3d_figure()
    my_chain.plot(my_chain.inverse_kinematics(target_frame), ax, target=target_vector, show=True)
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)

if __name__ == '__main__':
    test()

