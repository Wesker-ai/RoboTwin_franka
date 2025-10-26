from ._base_task import Base_Task
from .utils import *
import sapien
import random
from ._GLOBAL_CONFIGS import *


class place_the_apple_into_the_plate(Base_Task):

    def setup_demo(self, **kwags):
        super()._init_task_env_(**kwags)

    def load_actors(self):

        plate_pos = sapien.Pose([random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), 0.74], [0.707109, 0.707104, 0, 0])
        self.plate = create_actor(
            scene=self,
            pose=plate_pos,
            modelname="003_plate",
            model_id=0,
            convex=True,
            scale=2.2
        )
        self.plate.set_mass(0.05)

        pose = (sapien.Pose([plate_pos.p[0]+ 0.03, plate_pos.p[1] + 0.02, 0.785], [0.707109, 0.707104, 0, 0]),
                sapien.Pose([plate_pos.p[0]- 0.05, plate_pos.p[1], 0.762], [0.707109, 0.707104, 0, 0]))



    def play_once(self):
        pass

    def check_success(self):
        # both on the table
        return abs(self.mug.get_pose().p[2] - self.plate.get_pose().p[2]) < 0.02 and\
                abs(self.hamburg.get_pose().p[2] - self.plate.get_pose().p[2]) < 0.02

    def visualize_scene(self):
        while not self.viewer.closed: 
            self.scene.step()  # Simulate the world
            self.scene.update_render()  # Update the world to the renderer
            self.viewer.render()
