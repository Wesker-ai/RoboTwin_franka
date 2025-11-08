import transforms3d as t3d
import numpy as np

axis = [0, 1, 0]  # x axis
angle = np.pi / 2
rotation_matrix = t3d.axangles.axangle2mat(axis=axis, angle=angle)

post_mat = np.array([[
                0.0,
                -0.0,
                -1.0,
                0.06605000048875809
            ],
            [
                0.7071099877357483,
                0.7071099877357483,
                -0.0,
                -0.0
            ],
            [
                0.7071099877357483,
                -0.7071099877357483,
                0.0,
                -0.6889299750328064
            ],
            [
                0.0,
                0.0,
                0.0,
                1.0
            ]], dtype=np.float32)

# Apply the rotation to the top-left 3x3 submatrix
rotated_submatrix = rotation_matrix @ post_mat[:3, :3]
post_mat[:3, :3] = rotated_submatrix

print(post_mat.tolist())