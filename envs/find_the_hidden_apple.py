from ._base_task import Base_Task
from .utils import *
import numpy as np
import random
from ._GLOBAL_CONFIGS import *
from sapien import Pose

class find_the_hidden_apple(Base_Task):

    def setup_demo(self, **kwags):
        super()._init_task_env_(**kwags)

    def load_actors(self):
        displacement_plane = [random.uniform(-0.2, 0), random.uniform(-0.2, 0)]

        self.bottle = create_actor(
            scene=self, 
            pose=Pose([-0.0809142+ displacement_plane[0], 0.104552 + displacement_plane[1],0.777538], [0.0953172, 0.00765218, -0.000383877, 0.995417]),
            modelname="001_bottle",
            convex=True,
            # is_static=True,
            scale=np.array([1.8, 1.8, 1.8], dtype=np.float32)
        )
        self.bottle.set_mass(0.6)

        self.apple = create_actor(
            scene=self,
            pose=Pose([0.00759442 + displacement_plane[0], 0.200816 + displacement_plane[1], 0.743446], [-0.0751978, 0.261037, 0.581789, 0.766633]),
            modelname="103_fruit",
            convex=True,
            # is_static=True,
            scale=np.array([0.025, 0.025, 0.025], dtype=np.float32)
        )
        self.apple.set_mass(0.5)

        self.plastic_box = create_actor(
            scene=self, 
            pose=Pose([-0.106387 + displacement_plane[0], 0.125716 + displacement_plane[1], 0.741113], [0.653899, 0.653999, -0.269004, -0.268958]),
            modelname="062_plasticbox",
            model_id=1,
            convex=True,
            scale=[1.5, 1.5, 1.5]
        )
        self.plastic_box.set_mass(2)

        self.test_notebook = create_actor(
            scene=self,
            pose=Pose([0.565004, 0.183004, 0.835934], [0.486723, 0.509867, 0.489861, -0.513004]),
            modelname="092_notebook",
            model_id=2,
            convex=True
        )
        self.test_notebook.set_mass(0.5)


        self.notebook = create_actor(
            scene=self,
            pose=Pose([0.0370055 + displacement_plane[0], 0.0898387 + displacement_plane[1], 0.782214], [-0.111888, 0.152333, 0.69424, 0.694483]),
            modelname="092_notebook",
            convex=True,
            # is_static=True,
            model_id=0, 
            scale=np.array([1.8, 1.8, 1.8], dtype=np.float32)
        )
        self.notebook.set_mass(0.3)


        self.keyboard = create_actor(
            scene=self,
            pose=Pose([0.101803 + displacement_plane[0], 0.124976 + displacement_plane[1], 0.740893], [0.468636, 0.452964, 0.527099, 0.545318]),
            modelname="116_keyboard",
            convex=True,
            # is_static=True,
            model_id=0,
            scale=np.array([1.2, 1.2, 1.2], dtype=np.float32)
        )
        self.keyboard.set_mass(0.8)

        self.plate = create_actor(
            scene=self,
            pose = Pose([0.5, -0.2, 0.77], [0.707, 0.707, 0, 0]),
            modelname="003_plate",
            convex=True,
            is_static=True
        )
    
    def check_success(self):
        apple_pos = self.apple.get_pose().p
        plate_pose = self.plate.get_pose().p
        success_threshold = 0.1  # Define a threshold distance for success
        if np.linalg(apple_pos, plate_pose) < success_threshold:
            return True
        return False

    def play_once(self):
        arm_tag = ArmTag("right")
        self.move(
            self.grasp_actor(
                actor=self.test_notebook,
                arm_tag=arm_tag,
                
            )
        )

    def visualize_scene(self):
        while not self.viewer.closed:
            self.scene.step()  # Simulate the world
            self.scene.update_render()  # Update the world to the renderer
            self.viewer.render()
        actors =  self.scene.get_all_actors()
        for a in actors:
            print("---------------")
            print(a.name)
            print(a.get_pose())
            print("---------------")

