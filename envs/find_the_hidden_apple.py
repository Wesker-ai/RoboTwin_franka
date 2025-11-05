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
            pose=Pose([-0.0468304 + displacement_plane[0], 0.289028 + displacement_plane[1], 0.777073], [-0.0113291, 0.742763, 0.0159257, 0.669269]),
            modelname="001_bottle",
            convex=True,
            # is_static=True,
            scale=np.array([1.8, 1.8, 1.8], dtype=np.float32)
        )
        self.bottle.set_mass(0.6)

        self.apple = create_actor(
            scene=self,
            pose=Pose([0.00759442 + displacement_plane[0], 0.200816 + displacement_plane[1], 0.743446], [-0.0751978, 0.261037, 0.581789, 0.766633]),
            modelname="035_apple",
            convex=True,
            # is_static=True,
            scale=np.array([0.4, 0.4, 0.4], dtype=np.float32)
        )
        self.apple.set_mass(0.5)


        self.notebook = create_actor(
            scene=self,
            pose=Pose([0.040957 + displacement_plane[0], 0.189455 + displacement_plane[1], 0.78631], [-0.21131, 0.143538, 0.6235, 0.738913]),
            modelname="092_notebook",
            convex=True,
            # is_static=True,
            model_id=random.choice([0,2]),
            scale=np.array([1.8, 1.8, 1.8], dtype=np.float32)
        )
        self.notebook.set_mass(0.3)


        self.keyboard = create_actor(
            scene=self,
            pose=Pose([0.133545 + displacement_plane[0], 0.171531 + displacement_plane[1], 0.740893], [0.468723, 0.453055, 0.527021, 0.545242]),
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
        pass

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

