from envs._base_task import Base_Task
from envs.place_the_apple_into_the_plate import place_the_apple_into_the_plate
from envs.utils import *
import sapien

class gpt_place_the_apple_into_the_plate(place_the_apple_into_the_plate):
    def play_once(self):
        # Capture initial scene state
        self.save_camera_images(task_name="place_the_apple_into_the_plate", step_name="step1_initial_scene_state", generate_num_id="generate_num_4")
        
        # Use right arm only as specified in task description
        arm_tag = ArmTag("right")
        
        # Get the plate's functional point for placement
        plate_target_pose = self.plate.get_functional_point(0, "pose")
        
        # Grasp the apple using right arm
        self.move(
            self.grasp_actor(
                actor=self.apple,
                arm_tag=arm_tag,
                pre_grasp_dis=0.1,
                grasp_dis=0
            )
        )
        
        # Capture state after grasping apple
        self.save_camera_images(task_name="place_the_apple_into_the_plate", step_name="step2_apple_grasped", generate_num_id="generate_num_4")
        
        # Lift the apple up after grasping to avoid collision
        self.move(
            self.move_by_displacement(
                arm_tag=arm_tag,
                z=0.07,  # Move 7cm upward
                move_axis='world'
            )
        )
        
        # Capture state after lifting apple
        self.save_camera_images(task_name="place_the_apple_into_the_plate", step_name="step3_apple_lifted", generate_num_id="generate_num_4")
        
        # Place the apple on the plate
        self.move(
            self.place_actor(
                actor=self.apple,
                arm_tag=arm_tag,
                target_pose=plate_target_pose,
                functional_point_id=None,  # Apple has no functional points
                pre_dis=0.1,
                dis=0.02,
                is_open=True,
                constrain="free",  # Use "free" for general placement
                pre_dis_axis='grasp'  # Use grasp direction for pre-displacement
            )
        )
        
        # Capture state after placing apple on plate
        self.save_camera_images(task_name="place_the_apple_into_the_plate", step_name="step4_apple_placed", generate_num_id="generate_num_4")
        
        # Lift the gripper up after placing to avoid collision
        self.move(
            self.move_by_displacement(
                arm_tag=arm_tag,
                z=0.07,  # Move 7cm upward
                move_axis='world'
            )
        )
        
        # Capture state after gripper retraction
        self.save_camera_images(task_name="place_the_apple_into_the_plate", step_name="step5_gripper_retracted", generate_num_id="generate_num_4")
        
        # Return the right arm to origin
        self.move(self.back_to_origin(arm_tag=arm_tag))
        
        # Capture final scene state
        self.save_camera_images(task_name="place_the_apple_into_the_plate", step_name="step6_final_scene_state", generate_num_id="generate_num_4")

'''
Observation Point Analysis:
1. initial_scene_state - Capture initial state before any robot actions
2. apple_grasped - After grasping the apple with the gripper
3. apple_lifted - After lifting the apple up to avoid collision
4. apple_placed - After placing the apple on the plate
5. gripper_retracted - After lifting the gripper up after placement
6. final_scene_state - Capture final state after task completion
'''
