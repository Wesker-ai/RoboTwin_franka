import sys
import os
import time
import traceback
import sapien.core as sapien
from sapien.render import clear_cache
import yaml
import importlib
import numpy as np
from argparse import ArgumentParser

# 内置参数（可直接修改这里的参数值）
TASK_NAME = "get_apple1"
TASK_CONFIG = "demo_franka"

current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(current_file_path)
# 添加项目根目录到路径（确保导入正常）
sys.path.append(os.path.dirname(parent_directory))


def class_decorator(task_name):
    envs_module = importlib.import_module(f"envs.{task_name}")
    try:
        env_class = getattr(envs_module, task_name)
        env_instance = env_class()
    except:
        raise SystemExit("No such task")
    return env_instance


def get_embodiment_config(robot_file):
    robot_config_file = os.path.join(robot_file, "config.yml")
    with open(robot_config_file, "r", encoding="utf-8") as f:
        embodiment_args = yaml.load(f.read(), Loader=yaml.FullLoader)
    return embodiment_args


def main():
    # 初始化SAPIEN场景（SAPIEN 3.0.0b1版本写法）
    engine = sapien.Engine()
    renderer = sapien.VulkanRenderer()
    engine.set_renderer(renderer)
    
    scene = engine.create_scene()
    scene.set_timestep(1/100.0)
    
    # 添加光照
    scene.add_directional_light([0, 1, -1], [1, 1, 1], 1)
    scene.add_ambient_light([0.5, 0.5, 0.5])

    # 创建Viewer（SAPIEN 3.0.0b1交互的关键类）
    viewer = sapien.Viewer(renderer)
    viewer.set_scene(scene)
    viewer.set_camera_xyz(x=-2, y=0, z=1)
    viewer.set_camera_rpy(r=0, p=-np.arctan2(1, 2), y=0)
    viewer.window.set_title("RoboTwin Scene")

    task = class_decorator(TASK_NAME)
    # 将场景、引擎和渲染器传递给任务环境
    task.scene = scene
    task.engine = engine
    task.renderer = renderer
    task.viewer = viewer  # 传递viewer用于交互

    # 加载配置文件
    config_path = os.path.join(parent_directory, f"../task_config/{TASK_CONFIG}.yml")
    with open(config_path, "r", encoding="utf-8") as f:
        args = yaml.load(f.read(), Loader=yaml.FullLoader)

    args['task_name'] = TASK_NAME

    # 从全局配置导入CONFIGS_PATH
    from envs import CONFIGS_PATH
    embodiment_config_path = os.path.join(CONFIGS_PATH, "_embodiment_config.yml")

    with open(embodiment_config_path, "r", encoding="utf-8") as f:
        _embodiment_types = yaml.load(f.read(), Loader=yaml.FullLoader)

    def get_embodiment_file(embodiment_type):
        robot_file = _embodiment_types[embodiment_type]["file_path"]
        if robot_file is None:
            raise "missing embodiment files"
        return robot_file

    embodiment_type = args.get("embodiment")
    if len(embodiment_type) == 1:
        args["left_robot_file"] = get_embodiment_file(embodiment_type[0])
        args["right_robot_file"] = get_embodiment_file(embodiment_type[0])
        args["dual_arm_embodied"] = True
    elif len(embodiment_type) == 3:
        args["left_robot_file"] = get_embodiment_file(embodiment_type[0])
        args["right_robot_file"] = get_embodiment_file(embodiment_type[1])
        args["embodiment_dis"] = embodiment_type[2]
        args["dual_arm_embodied"] = False
    else:
        raise "number of embodiment config parameters should be 1 or 3"

    args["left_embodiment_config"] = get_embodiment_config(args["left_robot_file"])
    args["right_embodiment_config"] = get_embodiment_config(args["right_robot_file"])

    if len(embodiment_type) == 1:
        embodiment_name = str(embodiment_type[0])
    else:
        embodiment_name = str(embodiment_type[0]) + "+" + str(embodiment_type[1])

    # 显示配置信息
    print("============= Config =============\n")
    print(f"\033[95mMessy Table:\033[0m {args['domain_randomization']['cluttered_table']}")
    print(f"\033[95mRandom Background:\033[0m {args['domain_randomization']['random_background']}")
    if args["domain_randomization"]["random_background"]:
        print(f" - Clean Background Rate: {args['domain_randomization']['clean_background_rate']}")
    print(f"\033[95mRandom Light:\033[0m {args['domain_randomization']['random_light']}")
    if args["domain_randomization"]["random_light"]:
        print(f" - Crazy Random Light Rate: {args['domain_randomization']['crazy_random_light_rate']}")
    print(f"\033[95mRandom Table Height:\033[0m {args['domain_randomization']['random_table_height']}")
    print(f"\033[95mRandom Head Camera Distance:\033[0m {args['domain_randomization']['random_head_camera_dis']}")

    print(f"\033[94mHead Camera Config:\033[0m {args['camera']['head_camera_type']}, {args['camera']['collect_head_camera']}")
    print(f"\033[94mWrist Camera Config:\033[0m {args['camera']['wrist_camera_type']}, {args['camera']['collect_wrist_camera']}")
    print(f"\033[94mEmbodiment Config:\033[0m {embodiment_name}")
    print("\n==================================")

    args["embodiment_name"] = embodiment_name
    args['task_config'] = TASK_CONFIG
    args["save_path"] = os.path.join(args["save_path"], str(args["task_name"]), args["task_config"])
    run(task, args, scene, viewer)


def run(TASK_ENV, args, scene, viewer):
    epid, suc_num, fail_num, seed_list = 0, 0, 0, []
    total_renders = 2  # 总渲染次数

    print(f"Task Name: \033[34m{args['task_name']}\033[0m")

    # 创建保存路径
    os.makedirs(args["save_path"], exist_ok=True)

    # 加载已有的种子列表
    if not args.get("use_seed", False):
        print("\033[93m" + "[Start Seed and Pre Motion Data Collection]" + "\033[0m")
        args["need_plan"] = True

        seed_file = os.path.join(args["save_path"], "seed.txt")
        if os.path.exists(seed_file):
            with open(seed_file, "r") as file:
                seed_list = file.read().split()
                if seed_list:
                    seed_list = [int(i) for i in seed_list]
                    suc_num = len(seed_list)
                    epid = max(seed_list) + 1
            print(f"Exist seed file, Start from: {epid} / {suc_num}")

    for render_count in range(total_renders):
        try:
            # 环境加载流程
            TASK_ENV.setup_demo(now_ep_num=suc_num, seed=epid, **args)
            
            # 处理单次渲染的episode（仅初始化，不执行任务）
            max_episodes = args.get("max_episodes", 1)
            while epid < max_episodes:
                epid += 1
                TASK_ENV.setup_demo(now_ep_num=suc_num, seed=epid,** args)
                print(f"Episode {epid} environment initialized")

        except Exception as e:
            print(f"simulate data episode {epid} fail! (seed = {epid})")
            print(f"Error: {str(e)}")
            traceback.print_exc()

        # 只清理第一次渲染的资源，保留第二次
        if render_count == 0:
            clear_cache()
            print("第一次渲染资源已清理")
        else:
            print("第二次渲染完成，保留窗口（支持交互调整）")

    # 最后一次渲染后启动交互模式（参考你的成功代码）
    print("最后一次渲染完成，窗口支持交互调整：")
    print(" - 左键拖动：旋转视角")
    print(" - 右键拖动：平移视角")
    print(" - 滚轮：缩放视角")
    print(" - Ctrl+左键：选择并移动物体")
    print(" - Shift+左键：选择并旋转物体")
    print("按 Ctrl+C 退出...")

    # 启动交互循环（与你的参考代码保持一致）
    while not viewer.closed:
        scene.step()  # 模拟物理世界
        scene.update_render()  # 更新渲染
        viewer.render()  # 渲染窗口
        time.sleep(0.01)

    print("程序已退出")


if __name__ == "__main__":
    # 支持命令行参数覆盖内置参数
    parser = ArgumentParser()
    parser.add_argument("--task_name", type=str, default=TASK_NAME)
    parser.add_argument("--task_config", type=str, default=TASK_CONFIG)
    args = parser.parse_args()
    TASK_NAME = args.task_name
    TASK_CONFIG = args.task_config
    main()
    