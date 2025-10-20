import pickle
import numpy as np

# 加载 .pkl 文件
with open("/home/owlet/project/RoboTwin/data/beat_block_hammer/demo_franka/_traj_data/episode1.pkl", "rb") as f:
    data = pickle.load(f)

# 查看数据类型和维度（以 numpy 数组为例）
if isinstance(data, np.ndarray):
    print("数据维度：", data.shape)
else:
    print("数据类型：", type(data))
    # 若为字典/列表等，可进一步遍历查看内部元素维度
