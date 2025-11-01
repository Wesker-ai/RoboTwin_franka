from envs._base_task import Base_Task
from envs.find_the_plate import find_the_plate
from envs.utils import *
import sapien

class gpt_find_the_plate(find_the_plate):
    def play_once(self):
        # Use only right arm as specified in task description
        right_arm = ArmTag("right")
        
        # Initial observation
        self.save_camera_images(task_name="find_the_plate", step_name="step1_initial_scene", generate_num_id="generate_num_0")
        
        # Get plate functional point for placement reference
        plate_center_pose = self.plate.get_functional_point(0, "pose")
        
        # First move mug away from plate
        # Get mug position to determine if we need to grasp it
        mug_pose = self.mug.get_pose()
        mug_position = mug_pose.p
        
        # Grasp the mug with right arm
        self.move(
            self.grasp_actor(
                actor=self.mug,
                arm_tag=right_arm,
                pre_grasp_dis=0.1,
                grasp_dis=0
            )
        )
        
        # Observation after grasping mug
        self.save_camera_images(task_name="find_the_plate", step_name="step2_mug_grasped", generate_num_id="generate_num_0")
        
        # Lift mug up to avoid collision
        self.move(
            self.move_by_displacement(
                arm_tag=right_arm,
                z=0.07,
                move_axis='world'
            )
        )
        
        # Observation after lifting mug
        self.save_camera_images(task_name="find_the_plate", step_name="step3_mug_lifted", generate_num_id="generate_num_0")
        
        # Find a safe placement location away from plate
        # Move mug to a position offset from plate (e.g., 0.3 meters to the right)
        safe_placement_pose = [
            plate_center_pose.p[0] + 0.3,  # x: right of plate
            plate_center_pose.p[1],         # y: same as plate
            plate_center_pose.p[2],         # z: same height as plate
            plate_center_pose.q[0],         # qw
            plate_center_pose.q[1],         # qx
            plate_center_pose.q[2],         # qy
            plate_center_pose.q[3]          # qz
        ]
        
        # Place mug at safe location
        self.move(
            self.place_actor(
                actor=self.mug,
                arm_tag=right_arm,
                target_pose=safe_placement_pose,
                functional_point_id=1,  # Use bottom functional point for stable placement
                pre_dis=0.1,
                dis=0.02,
                is_open=True,
                constrain="free",
                pre_dis_axis='fp'
            )
        )
        
        # Observation after placing mug
        self.save_camera_images(task_name="find_the_plate", step_name="step4_mug_placed", generate_num_id="generate_num_0")
        
        # Lift gripper after placing
        self.move(
            self.move_by_displacement(
                arm_tag=right_arm,
                z=0.07,
                move_axis='world'
            )
        )
        
        # Observation after lifting gripper
        self.save_camera_images(task_name="find_the_plate", step_name="step5_gripper_lifted_after_mug", generate_num_id="generate_num_0")
        
        # Check if soap is on or near the plate and needs to be moved
        soap_pose = self.soap.get_pose()
        soap_position = soap_pose.p
        
        # If soap is close to plate (within 0.2 meters), move it away
        plate_position = plate_center_pose.p
        distance_to_plate = ((soap_position[0] - plate_position[0])**2 + 
                           (soap_position[1] - plate_position[1])**2 + 
                           (soap_position[2] - plate_position[2])**2)**0.5
        
        if distance_to_plate < 0.2:
            # Grasp soap with right arm
            self.move(
                self.grasp_actor(
                    actor=self.soap,
                    arm_tag=right_arm,
                    pre_grasp_dis=0.1,
                    grasp_dis=0,
                    contact_point_id=[0]  # Use contact point for soap
                )
            )
            
            # Observation after grasping soap
            self.save_camera_images(task_name="find_the_plate", step_name="step6_soap_grasped", generate_num_id="generate_num_0")
            
            # Lift soap up
            self.move(
                self.move_by_displacement(
                    arm_tag=right_arm,
                    z=0.07,
                    move_axis='world'
                )
            )
            
            # Observation after lifting soap
            self.save_camera_images(task_name="find_the_plate", step_name="step7_soap_lifted", generate_num_id="generate_num_0")
            
            # Place soap away from plate (opposite side from mug)
            soap_safe_pose = [
                plate_center_pose.p[0] - 0.3,  # x: left of plate
                plate_center_pose.p[1],        # y: same as plate
                plate_center_pose.p[2],        # z: same height as plate
                plate_center_pose.q[0],        # qw
                plate_center_pose.q[1],        # qx
                plate_center_pose.q[2],        # qy
                plate_center_pose.q[3]         # qz
            ]
            
            self.move(
                self.place_actor(
                    actor=self.soap,
                    arm_tag=right_arm,
                    target_pose=soap_safe_pose,
                    pre_dis=0.1,
                    dis=0.02,
                    is_open=True,
                    constrain="free",
                    pre_dis_axis='grasp'
                )
            )
            
            # Observation after placing soap
            self.save_camera_images(task_name="find_the_plate", step_name="step8_soap_placed", generate_num_id="generate_num_0")
            
            # Lift gripper after placing soap
            self.move(
                self.move_by_displacement(
                    arm_tag=right_arm,
                    z=0.07,
                    move_axis='world'
                )
            )
            
            # Observation after lifting gripper after soap
            self.save_camera_images(task_name="find_the_plate", step_name="step9_gripper_lifted_after_soap", generate_num_id="generate_num_0")
        
        # Return right arm to origin position
        self.move(
            self.back_to_origin(arm_tag=right_arm)
        )
        
        # Final observation
        self.save_camera_images(task_name="find_the_plate", step_name="step10_final_scene", generate_num_id="generate_num_0")

'''
Observation Point Analysis:
1. Initial scene state before any operations
2. After grasping the mug
3. After lifting the mug up
4. After placing the mug in safe location
5. After lifting gripper after mug placement
6. After grasping the soap (if applicable)
7. After lifting the soap up (if applicable)
8. After placing the soap in safe location (if applicable)
9. After lifting gripper after soap placement (if applicable)
10. Final scene state after all operations
'''
