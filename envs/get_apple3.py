from ._base_task import Base_Task
from .utils import *
import math
import sapien
import numpy as np
#from maskangle import MaskAngle, RLEMaskProcessor  # 保留原始注释

class get_apple3(Base_Task):  # 对齐 adjust_bottle 的 Base_task 继承结构
    def setup_demo(self, **kwags):
        """初始化演示环境（与 adjust_bottle 接口一致）"""
        super()._init_task_env_(**kwags)
        self.actor_loader = self._create_actor_loader()  # 初始化物体加载器（保留原始加载逻辑）

    def _create_actor_loader(self):
        """创建物体加载器（完整保留原始 ActorLoader 逻辑）"""
        class ActorLoader:
            def __init__(self, scene):
                self.scene = scene
                # 保留原始 _POSE_CONFIG 位姿配置（核心加载参数）
                self._POSE_CONFIG = {
                    'hammer': sapien.Pose([0.10162, -0.00280908, 0.829741],
                                          [0.111541, 0.849231, -0.499952, 0.128119]),
                    'actor1': sapien.Pose([0.0463346, 0.0777677, 0.819773],
                                          [0.277809, 0.0247334, -0.000171301, 0.960318]),
                    'actor2': sapien.Pose([0.0173133, 0.00850899, 0.788428],
                                          [-0.104428, 0.69561, 0.121403, 0.700345]),
                    'actor3': sapien.Pose([-0.0464481, -0.0891362, 0.799518],
                                          [0.34244, -0.222404, -0.217985, 0.886428]),
                    'actor4': sapien.Pose([-0.026355, -0.00166851, 0.813548],
                                          [0.766203, 0.171537, 0.614278, -0.0785502]),
                    'actor5': sapien.Pose([0.0727069, 0.00253, 0.8], 
                                         [0.707, 0.707, 0.0, 0.0]),
                    'actor6': sapien.Pose([-0.0481493, 0.00591826, 0.85547], [0.579516, 0.454998, 0.422098, 0.528178])
                }
                self.actors = {}  # 存储加载物体的字典（原始结构不变）

            # 保留原始小苹果加载方法（参数完全不变）
            def load_small_apple(self):
                """加载小苹果（原始逻辑完整保留）"""
                actor, actor_data = create_actor(
                    self.scene,
                    pose=self._POSE_CONFIG['actor1'],  # 原始 pose 配置
                    modelname="035_apple",  # 原始模型名
                    scale=[0.025, 0.025, 0.025],  # 原始缩放参数
                    convex=True  # 原始凸包设置
                )
                actor.find_component_by_type(sapien.physx.PhysxRigidDynamicComponent).mass = 0.01  # 原始质量设置
                return actor, actor_data

            # 保留其他必要物体加载方法（按需保留核心物体）
            def load_hammer(self):
                """加载锤子（原始逻辑完整保留）"""
                hammer, hammer_data = create_glb(
                    self.scene,
                    pose=self._POSE_CONFIG['hammer'],
                    modelname="001_bottles",
                    scale=(0.01, 0.01, 0.01),
                    convex=True,
                    model_id=16,
                )
                hammer.find_component_by_type(sapien.physx.PhysxRigidDynamicComponent).mass = 0.01
                return hammer, hammer_data

            # 保留原始批量加载方法（加载顺序和物体类型不变）
            def load_all_actors(self):
                """加载所有物体（原始加载逻辑不变）"""
                self.actors['small_apple'] = self.load_small_apple()  # 核心苹果加载
                self.actors['hammer'] = self.load_hammer()  # 辅助物体加载
                self.actors['brush'] = self.load_brush()  # 可继续保留其他物体
                # ... 其他物体加载逻辑（table_tennis/wooden_box 等）
                return self.actors

            # 保留原始位置检查方法（逻辑完全不变）
            def is_object_at_target(self, obj_name: str, target_pose: sapien.Pose, threshold: float = 0.05) -> bool:
                """检查物体是否到达目标位置（原始逻辑完整保留）"""
                if obj_name not in self.actors:
                    raise ValueError(f"物体 '{obj_name}' 未加载。请先使用 load_all_actors() 加载物体。")
                current_pose = self.actors[obj_name][0].get_pose()
                distance = np.linalg.norm(current_pose.p - target_pose.p)
                return distance < threshold

            # 补充原始代码中其他 load_* 方法（如 load_brush/load_table_tennis 等）
            def load_brush(self):
                """加载刷子（原始逻辑完整保留）"""
                actor, actor_data = create_actor(
                    self.scene,
                    pose=self._POSE_CONFIG['actor2'],
                    modelname="024_brush",
                    scale=[0.025, 0.025, 0.025],
                    convex=True
                )
                actor.find_component_by_type(sapien.physx.PhysxRigidDynamicComponent).mass = 0.01
                return actor, actor_data
            # ... 其他 load_* 方法（table_tennis/wooden_box 等）按原始代码保留

        return ActorLoader(self.scene)  # 将场景传入加载器

    def load_actors(self):
        """加载任务物体（整合原始加载逻辑与 adjust_bottle 环境配置）"""
        # 1. 调用原始加载器加载所有物体（保留核心加载逻辑）
        self.all_actors = self.actor_loader.load_all_actors()
        self.apple = self.all_actors['small_apple'][0]  # 获取苹果实体（任务核心物体）

        # 2. 环境配置（对齐 adjust_bottle 的流程）
        self.delay(4)  # 原始延迟加载逻辑
        self.add_prohibit_area(self.apple, padding=0.1)  # 苹果禁止区域（根据体积调整）
        # 定义目标位姿（参考 adjust_bottle 的 target_pose 设置）
        self.target_pose = sapien.Pose(p=[0.2, -0.1, 0.9], q=[0, 1, 0, 0])  # 苹果目标位置

    def play_once(self):
        """任务演示流程（参考 adjust_bottle 的脚本化动作逻辑）"""
        # 选择操作手臂（简化逻辑，可根据实际需求扩展）
        arm_tag = ArmTag("right")  # 假设使用右臂操作

        # 执行抓取-放置流程（复用 adjust_bottle 的动作接口）
        self.move(self.grasp_actor(
            self.apple, 
            arm_tag=arm_tag, 
            pre_grasp_dis=0.08  # 苹果体积小，预抓取距离略小
        ))
        self.move(self.move_by_displacement(arm_tag=arm_tag, z=0.1, move_axis="arm"))  # 抬升
        self.move(self.place_actor(
            self.apple,
            target_pose=self.target_pose,  # 放置到目标位置
            arm_tag=arm_tag,
            functional_point_id=0,
            pre_dis=0.0,
            is_open=False
        ))

        # 记录任务信息（对齐 adjust_bottle 的 info 格式）
        self.info["info"] = {
            "{A}": "035_apple",  # 苹果模型标识
            "{a}": str(arm_tag)  # 使用的手臂标识
        }
        return self.info

    def check_success(self):
        """任务成功判定（复用原始位置检查逻辑）"""
        # 使用原始 is_object_at_target 方法判断苹果是否到达目标位置
        return self.actor_loader.is_object_at_target(
            obj_name="small_apple",
            target_pose=self.target_pose,
            threshold=0.08  # 苹果位置容差（根据体积调整）
        )