from ._base_task import Base_Task
from .utils import *
import sapien
import numpy as np
from ._GLOBAL_CONFIGS import *


class get_apple1(Base_Task):
    def setup_demo(self, **kwags):
        super()._init_task_env_(** kwags)

    def load_actors(self):
        # 定义所有物体的初始位姿（源自原POSE_CONFIG）
        self.pose_config = {
            'hammer': sapien.Pose(
                [0.10162, -0.00280908, 0.829741],
                [0.111541, 0.849231, -0.499952, 0.128119]
            ),
            'apple': sapien.Pose(
                [0.0463346, 0.0777677, 0.789773],
                [0.277809, 0.0247334, -0.000171301, 0.960318]
            ),
            'brush': sapien.Pose(
                [0.0173133, 0.00850899, 0.788428],
                [-0.104428, 0.69561, 0.121403, 0.700345]
            )
            # 可根据需要添加其他物体的位姿配置
        }

        # 直接加载苹果（核心物体）
        self.apple = create_actor(
            self,
            pose=self.pose_config['apple'],
            modelname="035_apple",
            scale=[0.025, 0.025, 0.025],
            convex=True
        )
        self.apple.set_mass(0.01)

        # 直接加载锤子
        self.hammer = create_actor(
            self,
            pose=self.pose_config['hammer'],
            modelname="001_bottle",
            scale=(0.01, 0.01, 0.01),
            convex=True,
            model_id=16,
        )
        #self.hammer.set_mass(0.01)

        # 直接加载刷子（如需其他物体可按此格式添加）
        self.brush = create_actor(
            self,
            pose=self.pose_config['brush'],
            modelname="083_brush",
            scale=[0.025, 0.025, 0.025],
            convex=True
        )
        # self.brush.set_mass(0.01)

        # 环境配置（与adjust_bottle风格一致）
        self.delay(20)
        self.add_prohibit_area(self.apple, padding=0.1)
        self.target_pose = sapien.Pose(p=[0.2, -0.1, 0.9], q=[0, 1, 0, 0])

    def play_once(self):
        arm_tag = "right"  # 选择右臂操作

        # 执行抓取-放置流程（复用adjust_bottle动作接口）
        # self.move(self.grasp_actor(
        #     self.hammer,
        #     arm_tag=arm_tag,
        #     pre_grasp_dis=0.08
        # ))
        self.move(self.move_by_displacement(arm_tag=arm_tag, z=0.1, move_axis="arm"))
        # self.move(self.place_actor(
        #     self.hammer,
        #     target_pose=self.target_pose,
        #     arm_tag=arm_tag,
        #     functional_point_id=0,
        #     pre_dis=0.0,
        #     is_open=False
        # ))

        self.info["info"] = {
            "{A}": "035_apple",
            "{a}": str(arm_tag)
        }
        return self.info

    def check_success(self):
        """直接检查苹果位姿，不依赖actor_loader"""
        current_pose = self.apple.get_pose()
        distance = np.linalg.norm(current_pose.p - self.target_pose.p)
        return distance < 0.08
