import numpy as np
import os

#joint_test = np.load("client/npy/mp_landmark_left.npy")

def restruct_npy(_joint):
    joint = _joint
    print(joint.shape)
    print(joint)

    data = []

    # Compute angles between joints
    v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :3] # Parent joint
    v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :3] # Child joint
    v = v2 - v1 #[20,3]
    # Normalize v
    v = v / np.linalg.norm(v, axis=1)[:,np.newaxis]

    # Get angle using arcos of dot product
    angle = np.arccos(np.einsum('nt,nt->n',
        v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:],
        v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:])) # [15,]

    angle = np.degrees(angle) # Convert radian to degree

    angle_reshape = np.array([angle], dtype=np.float32)

    d = np.concatenate([joint.flatten(), angle_reshape.flatten()])

    data.append(d)
    data = np.array(data)

    print(data.shape)
    print(data)
    return data
