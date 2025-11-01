from ._base_task import Base_Task
from .utils import *
import sapien
import random
from ._GLOBAL_CONFIGS import *


class place_the_apple_into_the_plate(Base_Task):

    def setup_demo(self, **kwags):
        super()._init_task_env_(**kwags)

    def load_actors(self):

        plate_pos = sapien.Pose([random.uniform(0.1, 0.2), random.uniform(0.1, 0.2), 0.74], [0.707109, 0.707104, 0, 0])
        self.plate = create_actor(
            scene=self,
            pose=plate_pos,
            modelname="003_plate",
            model_id=0,
            is_static=True,
        )

        apple_pose = rand_pose(
            xlim=[-0.15, -0.1],
            ylim=[-0.1],
            zlim=[0.76],
            qpos=[0, 0, 1, 0],
        )
        
        self.apple = create_actor(
            scene=self,
            pose=apple_pose,
            modelname="035_apple",
            convex=True,
            scale=1.5
        )

        self.apple.set_mass(0.3)


    def play_once(self):
        # Get the apple and plate actors
        apple = self.apple
        plate = self.plate
        
        # Capture initial scene state
        self.save_camera_images(task_name="place_the_apple_into_the_plate", step_name="step1_initial_scene_state", generate_num_id="generate_num_0")
        
        # Use right arm as specified in the task
        arm_tag = ArmTag("right")
        
        # Get the plate's functional point for placement
        plate_target_pose = plate.get_functional_point(0, "pose")
        
        # Grasp the apple with right arm
        self.move(
            self.grasp_actor(
                actor=apple,
                arm_tag=arm_tag,
                pre_grasp_dis=0.1,
                grasp_dis=0
            )
        )
        
        # Capture state after grasping apple
        self.save_camera_images(task_name="place_the_apple_into_the_plate", step_name="step2_apple_grasped", generate_num_id="generate_num_0")
        
        # Lift the apple up to avoid collision
        self.move(
            self.move_by_displacement(
                arm_tag=arm_tag,
                z=0.07,
                move_axis='world'
            )
        )
        
        # Capture state after lifting apple
        self.save_camera_images(task_name="place_the_apple_into_the_plate", step_name="step3_apple_lifted", generate_num_id="generate_num_0")
        
        # Place the apple on the plate using the plate's functional point
        self.move(
            self.place_actor(
                actor=apple,
                arm_tag=arm_tag,
                target_pose=plate_target_pose,
                functional_point_id=None,  # No functional point on apple, use base alignment
                pre_dis=0.1,
                dis=0.02,
                is_open=True,
                constrain="free",
                pre_dis_axis='fp'
            )
        )
        
        # Capture state after placing apple on plate
        self.save_camera_images(task_name="place_the_apple_into_the_plate", step_name="step4_apple_placed", generate_num_id="generate_num_0")
        
        # Lift the gripper up after placing to avoid collision
        self.move(
            self.move_by_displacement(
                arm_tag=arm_tag,
                z=0.07,
                move_axis='world'
            )
        )
        
        # Capture state after retracting gripper
        self.save_camera_images(task_name="place_the_apple_into_the_plate", step_name="step5_gripper_retracted", generate_num_id="generate_num_0")
        
        # Return the right arm to origin
        self.move(self.back_to_origin(arm_tag=arm_tag))
        
        # Capture final scene state
        self.save_camera_images(task_name="place_the_apple_into_the_plate", step_name="step6_final_scene_state", generate_num_id="generate_num_0")

    def check_success(self):
        # both on the table
        return abs(self.apple.get_pose().p[2] - self.plate.get_pose().p[2]) < 0.05 and \
                abs(self.apple.get_pose().p[0] - self.plate.get_pose().p[0]) < 0.1 

    def visualize_scene(self):
        while not self.viewer.closed: 
            self.scene.step()  # Simulate the world
            self.scene.update_render()  # Update the world to the renderer
            self.viewer.render()
