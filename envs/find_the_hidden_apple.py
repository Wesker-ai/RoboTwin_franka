from ._base_task import Base_Task
from .utils import *
import numpy as np
import random
from ._GLOBAL_CONFIGS import *

class find_the_hidden_apple(Base_Task):

    def setup_demo(self, **kwags):
        super()._init_task_env_(**kwags)

    def load_actors(self):
        self.bottle_ids = random.sample(range(20), 3)
        self.bottle_poses = [
            rand_pose(
                xlim=[-0.2, 0.2],
                ylim=[-0.2, -0.05],
                zlim=[0.785],
                qpos=[0, 0, 1, 0],
                rotate_rand=True,
                rotate_lim=[0, 0, np.pi / 4],
            )
            for _ in range(4)
        ]
        self.bottles_eneties = [create_actor(self, 
                                             pose=self.bottle_poses[i], 
                                             modelname="001_bottle",
                                             model_id=i,
                                             is_static=True, # For Bottle Pose Adjustment
                                            #  convex=True,
                                             ) for i in self.bottle_ids]
        self.apple = create_actor(
            scene=self,
            pose=rand_pose(
                xlim=[-0.2, 0.2],
                ylim=[-0.2, -0.05],
                zlim=[0.785],
                qpos=[0, 0, 1, 0],
                rotate_rand=True,
                rotate_lim=[0, 0, np.pi / 4],
            ),
            modelname="035_apple",
            # convex=True,
            is_static=True,
        )
        
        self.bursh = create_actor(
            scene=self,
            pose=rand_pose(
                xlim=[-0.2, 0.2],
                ylim=[-0.2, -0.05],
                zlim=[0.785],
                qpos=[0, 0, 1, 0],
                rotate_rand=True,
                rotate_lim=[0, 0, np.pi / 4],
            ),
            modelname="083_brush",
            # convex=True,
            is_static=True,
            model_id=random.randint(0, 1)
        )
    
    def check_success(self):
        pass

    def visualize_scene(self):
        while not self.viewer.closed: 
            self.scene.step()  # Simulate the world
            self.scene.update_render()  # Update the world to the renderer
            self.viewer.render()
