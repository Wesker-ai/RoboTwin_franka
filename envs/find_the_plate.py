from ._base_task import Base_Task
from .utils import *
import sapien
import random
from ._GLOBAL_CONFIGS import *


class find_the_plate(Base_Task):

    def setup_demo(self, **kwags):
        super()._init_task_env_(**kwags)
        self.is_finshed_flag = False

    def load_actors(self):
        # plate_pos = rand_pose(
        #     xlim=[-0.25, 0.25],
        #     ylim=[-0.05, 0.15],
        #     zlim=[0.76],
        #     qpos=[0, 0, 1, 0],
        # )
        # Pose([0.112879, 0.135906, 0.739995], [0.707072, 0.707103, -0.00507516, -0.00539018])
        plate_pos = sapien.Pose([random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), 0.74], [0.707109, 0.707104, 0, 0])
        self.plate = create_actor(
            scene=self,
            pose=plate_pos,
            modelname="003_plate",
            model_id=0,
            convex=True,
            scale=2.4
        )
        self.plate.set_mass(0.05)

        pose = (sapien.Pose([plate_pos.p[0]+ 0.05, plate_pos.p[1] + 0.04, 0.785], [0.707109, 0.707104, 0, 0]),
                sapien.Pose([plate_pos.p[0]- 0.05, plate_pos.p[1], 0.762], [0.707109, 0.707104, 0, 0]))


        mug_pose = random.choice(pose)
        self.mug = create_actor(
            scene=self,
            pose=mug_pose,
            modelname="039_mug",
            convex=True,
            model_id=1
        )

        self.mug.set_mass(0.1)
        # choose the pose not used by the mug
        burger_pose = pose[1] if mug_pose is pose[0] else pose[0]
        self.hamburg = create_actor(
            scene=self,
            pose=burger_pose,
            modelname="006_hamburg",
            convex=True,
            model_id=random.randint(0, 5)
        )

        self.hamburg.set_mass(0.01)

    def play_once(self):
        # Use only right arm as specified
        right_arm = ArmTag("right")
        
        # Get plate position to use as reference
        plate_pose = self.plate.get_pose()
        plate_position = plate_pose.p
        
        # Define placement area away from plate (0.3 meters in front and right of plate)
        placement_offset = 0.1
        
        # Move mug first as specified
        # Grasp mug
        self.move(
            self.grasp_actor(
                actor=self.mug,
                arm_tag=right_arm,
                pre_grasp_dis=0.1,
                grasp_dis=0
            )
        )
                
        # Lift mug up to avoid collision
        self.move(
            self.move_by_displacement(
                arm_tag=right_arm,
                z=0.15,
                move_axis='world'
            )
        )
        
        # Place mug away from plate
        self.move(
            self.place_actor(
                actor=self.mug,
                arm_tag=right_arm,
                target_pose=[plate_position[0] + placement_offset, plate_position[1] + placement_offset, plate_position[2]] \
                    + [0.707109, 0.707104, 0, 0],
                functional_point_id=0,  # Use bottom functional point for placement
                pre_dis=0.1,
                dis=0.02,
                is_open=True,
                constrain="free",
                pre_dis_axis='fp'
            )
        )
                
        # Lift gripper after placing mug
        self.move(
            self.move_by_displacement(
                arm_tag=right_arm,
                z=0.1,
                move_axis='world'
            )
        )
        
        # Now move hamburg
        # Grasp hamburg
        self.move(
            self.grasp_actor(
                actor=self.hamburg,
                arm_tag=right_arm,
                pre_grasp_dis=0.1,
                grasp_dis=0
            )
        )
        
        # Lift hamburg up to avoid collision
        self.move(
            self.move_by_displacement(
                arm_tag=right_arm,
                z=0.15,
                move_axis='world'
            )
        )
        
        # Place hamburg away from plate
        self.move(
            self.place_actor(
                actor=self.hamburg,
                arm_tag=right_arm,
                target_pose=[plate_position[0] - placement_offset, plate_position[1] + placement_offset, plate_position[2]] +\
                    [0.707109, 0.707104, 0, 0],
                pre_dis=0.1,
                functional_point_id=0,  # Use bottom functional point for placement
                dis=0.02,
                is_open=True,
                constrain="free",
                pre_dis_axis='fp'
            )
        )
        
        
        # Lift gripper after placing hamburg
        self.move(
            self.move_by_displacement(
                arm_tag=right_arm,
                z=0.1,
                move_axis='world'
            )
        )
        
        # Return arm to origin
        self.move(self.back_to_origin(arm_tag=right_arm))
    def check_success(self):
        # both on the table
        return abs(self.mug.get_pose().p[2] - self.plate.get_pose().p[2]) < 0.02 and\
                abs(self.hamburg.get_pose().p[2] - self.plate.get_pose().p[2]) < 0.02

    def visualize_scene(self):
        while not self.viewer.closed: 
            self.scene.step()  # Simulate the world
            self.scene.update_render()  # Update the world to the renderer
            self.viewer.render()
