from ._base_task import Base_Task
from .utils import *
import sapien
import random
from ._GLOBAL_CONFIGS import *

class line_the_groceries(Base_Task):

    def setup_demo(self, **kwags):
        super()._init_task_env_(**kwags)

    def load_actors(self):
        pass
    
    def check_success(self):
        pass


    def visualize_scene(self):
        while not self.viewer.closed: 
            self.scene.step()  # Simulate the world
            self.scene.update_render()  # Update the world to the renderer
            self.viewer.render()
