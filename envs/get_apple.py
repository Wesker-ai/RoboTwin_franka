from ._base_task import Base_Task
from .utils import *
import sapien
import numpy as np
from ._GLOBAL_CONFIGS import *


class get_apple(Base_Task):
    def setup_demo(self, **kwags):
        super()._init_task_env_(** kwags)

    def load_actors(self):
        self.target_pose = [-0.25, 0.1, 0.95, 0, 1, 0, 0]
        # 定义所有物体的初始位姿（源自原POSE_CONFIG）
        x = 0.0301201 + np.random.uniform(-0.05, 0.15)  # x坐标随机化
        y = 0.0785133 + np.random.uniform(-0.35, 0.35)  # y坐标随机化
        z = 0.828805  # z坐标保持不变
        self.pose_config = {
            # 'shoe': sapien.Pose([-0.00806595, 0.00641218, 0.775649], [0.485869, 0.502523, -0.464847, 0.543432]),
            # 'bottle': sapien.Pose([0.0301201, 0.0785133, 0.828805], [-0.0866998, 0.854526, -0.407251, -0.310508]),
            # 'apple': sapien.Pose([-0.104534, -0.10756, 0.764068], [-0.0201814, 0.873546, 0.484488, 0.0422078]),
            
            # 'brush': sapien.Pose([-0.151422, 0.0361413, 0.822379], [0.00318154, -0.00379553, 0.711133, -0.70304])
                'bottle': sapien.Pose(
                    [
                        x,  # x坐标随机化
                        y,  # y坐标随机化
                        0.828805  # z坐标保持不变
                    ], 
                    [-0.0866998, 0.854526, -0.407251, -0.310508]
                ),
                # 其他物品基于瓶子新坐标的相对偏移（自动随瓶子位置变化）
                'shoe': sapien.Pose(
                    [
                        x + (-0.038186),  # 瓶子新x + 相对偏移
                        y + (-0.072101),  # 瓶子新y + 相对偏移
                        z + (-0.053156)   # 瓶子z + 相对偏移
                    ], 
                    [0.485869, 0.502523, -0.464847, 0.543432]
                ),
                'apple': sapien.Pose(
                    [
                        x + (-0.134654),  # 瓶子新x + 相对偏移
                        y + (-0.186073),  # 瓶子新y + 相对偏移
                        z + (-0.064737)   # 瓶子z + 相对偏移
                    ], 
                    [-0.0201814, 0.873546, 0.484488, 0.0422078]
                ),
                
                'brush': sapien.Pose(
                    [
                        x + (-0.181542),  # 瓶子新x + 相对偏移
                        y + (-0.042372),  # 瓶子新y + 相对偏移
                        z + (-0.006426)   # 瓶子z + 相对偏移
                    ], 
                    [0.00318154, -0.00379553, 0.711133, -0.70304]
                )
        }
# bottle:Pose([0.0107527, -0.0421576, 0.775286], [-0.987502, -0.00828747, -0.145748, 0.0594032])
# brush:Pose([-0.274379, -0.00919102, 0.778563], [0.690496, 0.170047, 0.649765, -0.268523])
# apple:Pose([-0.0330594, 0.12024, 0.790943], [0.566127, -0.288353, 0.587167, -0.501585])
        # 直接加载苹果（核心物体）
        self.apple = create_actor(
            self,
            pose=self.pose_config['apple'],
            modelname="035_apple",
            scale=[0.025, 0.025, 0.025],
            convex=True
        )
        self.apple.set_mass(0.01)

        # 直接加载瓶子
        self.bottle = create_actor(
            self,
            pose=self.pose_config['bottle'],
            modelname="001_bottle",
            scale=(0.01, 0.01, 0.01),
            convex=True,
            model_id=np.random.choice([1, 16])
        )
        #self.bottle.set_mass(0.01)

        self.shoe = create_actor(
            self,
            pose=self.pose_config['shoe'],
            modelname="041_shoe",
            scale=[0.03, 0.03, 0.03],
            convex=True,
            model_id=np.random.choice([0, 7])
        )
        # self.shoe.set_mass(0.01)

        # 直接加载刷子（如需其他物体可按此格式添加）
        self.brush = create_actor(
            self,
            pose=self.pose_config['brush'],
            modelname="083_brush",
            scale=[0.025, 0.025, 0.025],
            convex=True,
            model_id=np.random.choice([0, 1])
        )
        # self.brush.set_mass(0.01)


        # 环境配置（与adjust_bottle风格一致）
        #self.delay(20)
        self.add_prohibit_area(self.apple, padding=0.1)

    def play_once(self):
        # Capture initial scene state
        self.save_camera_images(task_name="get_apple", step_name="step1_initial_scene", generate_num_id="generate_num_1")
        
        # First, remove the brush that's hiding the apple
        # brush_pose = self.brush.get_pose()
        
        # Select arm based on brush position
        Arm_tag = ArmTag("right")
        self.move(self.open_gripper(Arm_tag))
        
        self.move(self.grasp_actor(self.bottle, arm_tag=Arm_tag, pre_grasp_dis=0.12, grasp_dis=0.01))
        self.move(self.move_by_displacement(arm_tag=Arm_tag, z=0.1, move_axis="arm"))
        # Place the bottle at target pose (functional point 0) while keeping gripper closed
        self.move(
            self.place_actor(
                self.bottle,
                target_pose= [0.25, 0.1, 0.95, 0, 1, 0, 0],
                arm_tag=Arm_tag,
                functional_point_id=0,
                pre_dis=0.06,
                is_open=False,
            ))
        self.move(self.open_gripper(Arm_tag))
        self.move_by_displacement(arm_tag=Arm_tag, x=-0.1,y=0, z=0.05, move_axis="arm")
        self.move(self.back_to_origin(Arm_tag))
        self.move(self.move_by_displacement(arm_tag=Arm_tag, x=0.2,y=0, z=0.15, move_axis="arm"))
        self.move(self.move_to_pose(Arm_tag, target_pose= self.pose_config['shoe']))
        
        # 苹果的夹取（位姿不正确）
        self.move(self.grasp_actor(self.apple, arm_tag=Arm_tag, pre_grasp_dis=0.1, contact_point_id=[0,1,2,3]))
        self.move(self.move_by_displacement(arm_tag=Arm_tag, x=-0.1,y=0,z=0.15, move_axis="arm"))
        self.move(self.back_to_origin(Arm_tag))
        #self.move(self.move_to_pose(Arm_tag, target_pose=[-0.25, 0.1, 0.8, 0, 1, 0, 0]))
        #self.move(self.open_gripper(Arm_tag))
        # self.move(self.place_actor(
        #     self.apple,
        #     target_pose=[-0.25, 0.1, 0.8, 0, 1, 0, 0],
        #     arm_tag=Arm_tag,
        #     #functional_point_id,
        #     pre_dis=0.06,
        #     is_open=False
        # ))
    def check_success(self):
        """直接检查苹果位姿，不依赖actor_loader"""
        current_pose = self.apple.get_pose().p  # 获取苹果的3D位置 [x, y, z]
        # 检查z坐标（高度）是否大于0.8
        return current_pose[2] > 0.8
