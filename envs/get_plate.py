from ._base_task import Base_Task
from .utils import *
import sapien
import numpy as np
from ._GLOBAL_CONFIGS import *


class get_plate(Base_Task):
    def setup_demo(self, **kwags):
        super()._init_task_env_(** kwags)

    def load_actors(self):
        # 定义所有物体的初始位姿
        hammer_origin_x = 0.0165791  # 锤子原始x坐标（基准点）
        hammer_origin_y = 0.089866   # 锤子原始y坐标（基准点）
        hammer_origin_z = 0.787721   # 锤子原始z坐标（固定）
        # 随机化锤子的x和y偏移（范围可根据需求调整）
        x_offset = np.random.uniform(-0.05, 0.15)  # x随机偏移
        y_offset = np.random.uniform(-0.35, 0.35)  # y随机偏移
        # 计算锤子的新坐标
        hammer_new_x = hammer_origin_x + x_offset
        hammer_new_y = hammer_origin_y + y_offset
        hammer_new_z = hammer_origin_z  # z坐标保持不变

        # 2. 计算其他物体相对锤子的偏移量（基于原始坐标）
        # 相对偏移 = 物体原始坐标 - 锤子原始坐标
        rel_offsets = {
            'plate': [
                -0.0286168 - hammer_origin_x,  # plate原始x - 锤子原始x
                -0.00286766 - hammer_origin_y, # plate原始y - 锤子原始y
                0.739971 - hammer_origin_z     # plate原始z - 锤子原始z
            ],
            'scanner': [
                -0.0900408 - hammer_origin_x,  # scanner原始x - 锤子原始x
                0.0643627 - hammer_origin_y,   # scanner原始y - 锤子原始y
                0.740904 - hammer_origin_z     # scanner原始z - 锤子原始z
            ],
            'microphone': [
                -0.0229023 - hammer_origin_x,  # microphone原始x - 锤子原始x
                -0.0319179 - hammer_origin_y,  # microphone原始y - 锤子原始y
                0.801101 - hammer_origin_z     # microphone原始z - 锤子原始z
            ]
        }

        # 3. 更新位姿配置（所有物体基于锤子新坐标计算位置）
        self.pose_config = {
            # 锤子（基准物体）：随机化后的坐标
            'hammer': sapien.Pose(
                [hammer_new_x, hammer_new_y, hammer_new_z],  # 新位置（随机化x/y）
                [0.0628832, 0.169547, 0.981691, 0.0598458]   # 旋转保持不变
            ),
            # 盘子（基于锤子新坐标）
            'plate': sapien.Pose(
                [
                    hammer_new_x + rel_offsets['plate'][0],  # 锤子新x + 相对x偏移
                    hammer_new_y + rel_offsets['plate'][1],  # 锤子新y + 相对y偏移
                    hammer_new_z + rel_offsets['plate'][2]   # 锤子新z + 相对z偏移
                ], 
                [0.49668, 0.497135, 0.502784, 0.503363]  # 旋转保持不变
            ),
            # 扫描仪（基于锤子新坐标）
            'scanner': sapien.Pose(
                [
                    hammer_new_x + rel_offsets['scanner'][0],  # 锤子新x + 相对x偏移
                    hammer_new_y + rel_offsets['scanner'][1],  # 锤子新y + 相对y偏移
                    hammer_new_z + rel_offsets['scanner'][2]   # 锤子新z + 相对z偏移
                ], 
                [-0.42473, -0.415828, 0.569248, 0.568022]  # 旋转保持不变
            ),   
            # 麦克风（基于锤子新坐标）
            'microphone': sapien.Pose(
                [
                    hammer_new_x + rel_offsets['microphone'][0],  # 锤子新x + 相对x偏移
                    hammer_new_y + rel_offsets['microphone'][1],  # 锤子新y + 相对y偏移
                    hammer_new_z + rel_offsets['microphone'][2]   # 锤子新z + 相对z偏移
                ], 
                [0.413404, -0.440348, -0.554438, 0.572529]  # 旋转保持不变
            ),
            # 其他物体（dustpan、shoe、bowl等）可按此格式添加...
            'dustpan': sapien.Pose(
                p=[0, 0.3, 0.8],  # 若无需相对定位，可保留原始绝对坐标
                q=[1, 0.67, 0.2, -0.3]
            ),
            # ... 其他物体配置 ...
        }
        # 加载麦克风
        self.microphone_model_id = np.random.choice([0,1,4,5])
        self.microphone = create_actor(
            self,
            pose=self.pose_config['microphone'],
            modelname="018_microphone",
            model_id=self.microphone_model_id,
            convex=True
        )

        # 加载锤子
        self.hammer = create_actor(
            self.scene,
            pose=self.pose_config['hammer'],
            modelname="020_hammer",
            is_static=False,
            convex=True
        )
        self.hammer.set_mass(0.01)
        # 加载盘子
        self.plate = create_actor(
            self,
            pose=self.pose_config['plate'],
            modelname="003_plate",
            scale=[0.025, 0.025, 0.025],
            is_static=True,
            convex=True
        )

        # 加载扫描仪
        self.scanner = create_actor(
            self.scene,
            pose=self.pose_config['scanner'],
            modelname="024_scanner",
            scale=[0.25, 0.25, 0.25],
            is_static=False,
            convex=True
        )

        # 设置目标位姿
        self.target_pose = sapien.Pose(p=[0.2, -0.1, 0.9], q=[0, 1, 0, 0])
        self.add_prohibit_area(self.plate, padding=0.1)
    def play_once(self):
        # Capture initial scene state
        self.save_camera_images(task_name="get_plate", step_name="step1_initial_scene", generate_num_id="generate_num_1")

        # Select arm based on brush position
        Arm_tag = ArmTag("right")
        self.move(self.open_gripper(Arm_tag))
        
        self.move(self.grasp_actor(self.hammer, arm_tag=Arm_tag, pre_grasp_dis=0.12, grasp_dis=0.01, contact_point_id=[0]))
        self.move(self.move_by_displacement(arm_tag=Arm_tag, z=0.1, move_axis="arm"))
        # Place the hammer at target pose (functional point 0) while keeping gripper closed
        self.move(
            self.place_actor(
                self.hammer, 
                target_pose= [0.25, 0.1, 0.95, 0, 1, 0, 0],
                arm_tag=Arm_tag,
                functional_point_id=0,
                pre_dis=0.06,
                is_open=False,
            ))
        self.move(self.open_gripper(Arm_tag))

        self.move_by_displacement(arm_tag=Arm_tag, x=0,y=0, z=0.15, move_axis="arm")
        self.move(self.back_to_origin(Arm_tag))
    
        self.move(self.grasp_actor(self.scanner, arm_tag=Arm_tag, pre_grasp_dis=0.1, contact_point_id=[0]))
        self.move(self.move_by_displacement(arm_tag=Arm_tag, x=0,y=0,z=0.15, move_axis="arm"))
        self.move(
            self.place_actor(
                self.scanner,
                target_pose=[-0.25, 0.1, 0.8, 0, 1, 0, 0],
                arm_tag=Arm_tag,
                functional_point_id=0,
                pre_dis=0.06,
                is_open=False,
            ))
        self.move(self.open_gripper(Arm_tag))
        
        self.move(self.back_to_origin(Arm_tag))
        self.move(self.grasp_actor(self.microphone, arm_tag=Arm_tag, pre_grasp_dis=0.08, contact_point_id=[8]))
        self.move(self.back_to_origin(Arm_tag))
        #self.move(self.move_to_pose(Arm_tag, target_pose=[-0.25, 0.1, 0.8, 0, 1, 0, 0]))
        #self.move(self.open_gripper(Arm_tag))
        # self.move(self.place_actor(
        #     self.microphone,
        #     target_pose=[-0.25, 0.1, 0.8, 0, 1, 0, 0],
        #     arm_tag=Arm_tag,
        #     #functional_point_id,
        #     pre_dis=0.06,
        #     is_open=False
        # ))

        self.info["info"] = {
            "{A}": "003_plate/base0",
            "{B}": "020_hammer/base0",
            "{C}": "024_scanner/base0",
            "{D}":f"018_microphone/base{self.microphone_model_id}",
            "{a}": str(ArmTag("right")),
        }
        return self.info
    
    def check_success(self):
        current_pose = self.microphone.get_pose().p  
        # 检查z坐标（高度）是否大于0.8
        return current_pose[2] > 0.8
