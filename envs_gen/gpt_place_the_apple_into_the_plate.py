from envs._base_task import Base_Task
from envs.place_the_apple_into_the_plate import place_the_apple_into_the_plate
from envs.utils import *
import sapien

class gpt_place_the_apple_into_the_plate(place_the_apple_into_the_plate):
    def play_once(self):
        # Capture initial scene state
        self.save_camera_images(task_name="place_the_apple_into_the_plate", step_name="initial_scene_state", generate_num_id="generate_num_0")
        
        # Use right arm as specified in the task
        arm_tag = ArmTag("right")
        
        # First, grasp the apple with right hand
        self.move(
            self.grasp_actor(
                actor=self.apple,
                arm_tag=arm_tag,
                pre_grasp_dis=0.1,
                grasp_dis=0
            )
        )
        
        # Capture scene after apple is grasped
        self.save_camera_images(task_name="place_the_apple_into_the_plate", step_name="step1_apple_grasped", generate_num_id="generate_num_0")
        
        # Lift the apple up to avoid collision
        self.move(
            self.move_by_displacement(
                arm_tag=arm_tag,
                z=0.07,
                move_axis='world'
            )
        )
        
        # Capture scene after apple is lifted
        self.save_camera_images(task_name="place_the_apple_into_the_plate", step_name="step2_apple_lifted", generate_num_id="generate_num_0")
        
        # Get the plate's functional point for placement
        plate_target_pose = self.plate.get_functional_point(0, "pose")
        
        # Place the apple on the plate
        self.move(
            self.place_actor(
                actor=self.apple,
                arm_tag=arm_tag,
                target_pose=plate_target_pose,
                functional_point_id=None,  # Apple has no functional points, use base alignment
                pre_dis=0.1,
                dis=0.02,
                is_open=True,
                constrain="free",
                pre_dis_axis='fp'
            )
        )
        
        # Capture scene after apple is placed on plate
        self.save_camera_images(task_name="place_the_apple_into_the_plate", step_name="step3_apple_placed", generate_num_id="generate_num_0")
        
        # Lift the gripper up after placing to avoid collision
        self.move(
            self.move_by_displacement(
                arm_tag=arm_tag,
                z=0.07,
                move_axis='world'
            )
        )
        
        # Capture scene after gripper is retracted
        self.save_camera_images(task_name="place_the_apple_into_the_plate", step_name="step4_gripper_retracted", generate_num_id="generate_num_0")
        
        # Return right arm to origin
        self.move(self.back_to_origin(arm_tag=arm_tag))
        
        # Capture final scene state
        self.save_camera_images(task_name="place_the_apple_into_the_plate", step_name="final_scene_state", generate_num_id="generate_num_0")

'''
Observation Point Analysis:
1. initial_scene_state - Capture the initial scene before any manipulation
2. step1_apple_grasped - After grasping the apple with the right hand
3. step2_apple_lifted - After lifting the apple up to avoid collision
4. step3_apple_placed - After placing the apple on the plate
5. step4_gripper_retracted - After lifting the gripper up after placement
6. final_scene_state - Capture the final scene after task completion
'''
