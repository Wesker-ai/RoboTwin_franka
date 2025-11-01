from ._base_task import Base_Task
from .utils import *
import sapien
import random
from ._GLOBAL_CONFIGS import *


class find_the_plate(Base_Task):

    def setup_demo(self, **kwags):
        super()._init_task_env_(**kwags)

    def load_actors(self):
        plate_pos = sapien.Pose([random.uniform(-0.08, 0.08), random.uniform(-0.08, 0.08), 0.740], [0.707109, 0.707104, 0, 0])
        self.plate = create_actor(
            scene=self,
            pose=plate_pos,
            modelname="003_plate",
            model_id=0,
            convex=True,
            scale=2.6
        )
        self.plate.set_mass(0.1)

        pose = (-1, 1)


        mug_pose = random.choice(pose)
        self.mug = create_actor(
            scene=self,
            pose=sapien.Pose([plate_pos.p[0]+ 0.025 * mug_pose, plate_pos.p[1] + 0.025 * mug_pose, 0.75], [0.707109, 0.707104, 0, 0]),
            modelname="039_mug",
            convex=True,
            model_id=1,
            scale=0.8
        )
        self.mug.set_mass(0.2)

        # choose the pose not used by the mug
        soap_pose = pose[1] if mug_pose is pose[0] else pose[0]
        self.soap = create_actor(
            scene=self,
            pose=sapien.Pose([plate_pos.p[0]+ random.uniform(0.04, 0.044) * soap_pose, plate_pos.p[1]+ random.uniform(0.04, 0.044) * soap_pose, 0.760], [0.707109, 0.707104, 0, 0]),
            modelname="107_soap",
            convex=True,
            model_id=random.randint(2, 3),
            scale=0.7,
        )

        self.soap.set_mass(0.07)

    def check_success(self):
        # both on the table
        return abs(self.mug.get_pose().p[2] - self.plate.get_pose().p[2]) < 0.02 and\
                abs(self.soap.get_pose().p[2] - self.plate.get_pose().p[2]) < 0.05 and\
                abs(self.soap.get_pose().p[0] - self.plate.get_pose().p[0]) >= 0.18 


    def visualize_scene(self):
        while not self.viewer.closed: 
            self.scene.step()  # Simulate the world
            self.scene.update_render()  # Update the world to the renderer
            self.viewer.render()


    def play_once(self):
        # Use only right arm as specified in task description
        right_arm = ArmTag("right")
        sign = 1 if self.plate.get_pose().p[0] >= 0 else -1
        
        # Get plate functional point for placement reference
        plate_center_pose = self.plate.get_functional_point(0, "pose")
                
        # Grasp the mug with right arm
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
                z=0.07,
                move_axis='world'
            )
        )
        
        # Find a safe placement location away from plate
        # Move mug to a position offset from plate (e.g., 0.3 meters to the right)  Pose([0.357851, -0.181893, 0.739904], [0.70537, 0.708817, 0.00368734, 0.00428236])
        safe_placement_pose = [0.357851, -0.181893, 0.75]+[       # z: same height as plate
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
        
        # Lift gripper after placing
        self.move(
            self.move_by_displacement(
                arm_tag=right_arm,
                z=0.1,
                move_axis='world'
            )
        )

        # soap_pose = self.soap.get_pose()
        # soap_orientation = soap_pose.q     Pose([0.0188185, 0.113534, 1.10307], [0.005245, 0.707102, 0.00524184, -0.707073])

        self.move(
            self.grasp_actor(
                actor=self.soap,
                arm_tag=right_arm,
                pre_grasp_dis=0.1,
                grasp_dis=0,
                contact_point_id=[0]  # Use contact point for soap
            )
        )
        
        # Lift soap up
        self.move(
            self.move_by_displacement(
                arm_tag=right_arm,
                z=0.07,
                move_axis='world'
            )
        )
        
        # Place soap away from plate (opposite side from mug) Pose([-0.346942, -0.179817, 0.740829], [0.697623, 0.71456, -0.0373541, -0.0364804])
        soap_safe_pose = [-0.346942, -0.179817, 0.77] + [0.707, 0.0, 0.0, -0.707]
        
        self.move(
            self.place_actor(
                actor=self.soap,
                arm_tag=right_arm,
                target_pose=soap_safe_pose,
                pre_dis=0.1,
                dis=0.02,
                is_open=True,
                constrain="free",
                pre_dis_axis='grasp',
            )
        )
                
        # Lift gripper after placing soap
        self.move(
            self.move_by_displacement(
                arm_tag=right_arm,
                z=0.07,
                move_axis='world'
            )
        )
                    
        # Return right arm to origin position
        self.move(
            self.back_to_origin(arm_tag=right_arm)
        )
