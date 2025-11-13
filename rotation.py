import transforms3d as t3d
import numpy as np

axis = [[1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
        ]
angle = np.pi / 2
rotation_matrix = [t3d.axangles.axangle2mat(axis=a, angle=angle) for a in axis]

post_mat_1 = np.array(
            [
            [
                0.0,
                -0.0,
                -1.0,
                0.1564899981021881
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
                -0.720550000667572
            ],
            [
                0.0,
                0.0,
                0.0,
                1.0
            ]
        ],dtype=np.float32)

post_mat_2 = np.array(
            [
            [
                0.0,
                0.0,
                1.0,
                0.1501999944448471
            ],
            [
                0.7071099877357483,
                0.7071099877357483,
                -0.0,
                0.0
            ],
            [
                -0.7071099877357483,
                0.7071099877357483,
                -0.0,
                0.7159799933433533
            ],
            [
                0.0,
                0.0,
                0.0,
                1.0
            ]
        ], dtype=np.float32
)

# Apply the rotation to the top-left 3x3 submatrix
for idx, rot in enumerate(rotation_matrix):
    rotated_submatrix_1 = rot @ post_mat_1[:3, :3]
    post_mat_1[:3, :3] = rotated_submatrix_1
    print(post_mat_1.tolist())

    rotated_submatrix_2 = rot @ post_mat_2[:3, :3]
    post_mat_2[:3, :3] = rotated_submatrix_2
    print(post_mat_2.tolist())

    print()
