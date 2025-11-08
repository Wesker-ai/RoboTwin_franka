from ._base_task import Base_Task
from .utils import *
import numpy as np
import random
from ._GLOBAL_CONFIGS import *
from sapien import Pose

class clean_laptop(Base_Task):

    def setup_demo(self, **kwags):
        super()._init_task_env_(**kwags)

    def load_actors(self):
        self.laptop: ArticulationActor = rand_create_sapien_urdf_obj(
            scene=self,
            modelname="015_laptop",
            modelid=np.random.randint(0, 11),
            xlim=[0, 0.1],
            ylim=[0, 0.1],
            rotate_rand=True,
            rotate_lim=[0, 0, np.pi / 3],
            qpos=[0.7, 0, 0, 0.7],
            fix_root_link=True,
            scale=[1.2, 1.2, 1.2]
        )
        limit = self.laptop.get_qlimits()[0]
        self.laptop.set_qpos([limit[0]])
        self.laptop.set_mass(0.01)
        self.laptop.set_properties(1, 0)
        self.add_prohibit_area(self.laptop, padding=0.1)

        bottle_poses = [

        ]

        self.bottles = [
            create_actor(
                scene=self,
                pose=pose,
                model_id=random.randint(0, 20),
                scale=[0.7, 0.7, 0.7],
                modelname="001_bottle"
            ).set_mass(0.1) for idx, pose in enumerate(bottle_poses)
        ]
        
        self.fruit = create_actor(
            scene=self,
            modelname="103_fruit",
            model_id=0,
            pose=Pose([0, 0, 0.8], [0.707, 0.707, 0, 0]),
            is_static=True,
            scale=[0.05, 0.05, 0.05]
        )
        self.fruit.set_mass(0.1)
    
    def check_success(self):
        pass

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

