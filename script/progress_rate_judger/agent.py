import openai
import ffmpeg
import subprocess
import numpy as np
import os
import cv2
import tempfile
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) 

API_KEY = "sk-w5JCPUJMAqnQ7J9xCakSIv906EHPlvrb8cNQVbS7HXrqFMJt"

PROMPT = """
You is a progress rate judger, your task is to judge the progress rate of a task.
The task's information would be provided in the following format:
Task Information:
- Task Name: {task_name}
- Task States: {task_state_0, task_state_1, ..., task_state_n}

Your task is to judge which state does the task progress to based on the provided states.
If you found in the video that the task paused at the state {task_state_i}, the progress rate should be {i / n}.
You should only return the progress rate. If you cannot judge the progress rate, return -1.
"""

client = openai.OpenAI(
    api_key=API_KEY,
    base_url="https://api.moonshot.cn/v1",
)
def get_asked_frame(video_path, opt: str ):
    """
    使用ffmpeg从视频中提取最后一帧并返回为numpy数组
    
    Args:
        video_path: 视频文件的路径
        
    Returns:
        np.ndarray: 最后一帧的图像数据，格式为(H, W, 3)的numpy数组
    """
    import subprocess
    import numpy as np
    import os
    import tempfile
    
    # 检查视频文件是否存在
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"视频文件不存在: {video_path}")
    
    try:
        # 首先获取视频的总帧数
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vcodec', 'copy',
            '-an', '-f', 'null', '-'
        ]
        result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
        
        # 解析输出以获取总帧数
        frame_count = None
        for line in result.stderr.split('\n'):
            if 'frame=' in line:
                try:
                    frame_count = int(line.split('frame=')[1].strip().split()[0])
                except ValueError:
                    continue
        
        if frame_count is None:
            raise ValueError("无法获取视频的总帧数")
        
        if opt == "first":
            frame_idx = 0
        elif opt == "last":
            frame_idx = frame_count - 1
        elif opt == "mid":
            frame_idx = frame_count // 2
        
        # 使用ffmpeg提取最后一帧并直接读取到内存中
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f'select=eq(n\\,{frame_idx})',
            '-vframes', '1',
            '-f', 'image2pipe',
            '-pix_fmt', 'rgb24',
            '-vcodec', 'rawvideo',
            '-'
        ]
        
        # 运行ffmpeg命令并捕获输出
        pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = pipe.communicate()
        
        if pipe.returncode != 0:
            raise RuntimeError(f"ffmpeg命令执行失败: {stderr.decode('utf-8')}")
        
        # 获取视频分辨率以正确解析原始数据
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height',
            '-of', 'csv=s=x:p=0',
            video_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
        width, height = map(int, result.stdout.strip().split('x'))
        
        # 将原始RGB数据转换为numpy数组
        image = np.frombuffer(stdout, dtype=np.uint8).reshape((height, width, 3))
        
        return image
        
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"ffmpeg命令执行失败: {e}")
    except Exception as e:
        raise e
    
def save_asked_frame_to_dir(video_path, save_dir, opt: str, filename=None):
    """
    将视频的最后一帧以图片形式保存到指定目录下
    
    Args:
        video_path: 视频文件的路径
        save_dir: 保存图片的目录路径
        opt: 提取帧的选项，"first", "last", "mid"
        filename: 保存的图片文件名，如果为None则自动生成
        
    Returns:
        str: 保存的图片文件的完整路径
    """
    # 确保保存目录存在
    os.makedirs(save_dir, exist_ok=True)
    
    # 如果未指定文件名，则根据视频文件名自动生成
    if filename is None:
        video_name = os.path.basename(video_path).split('.')[0]
        filename = f"{video_name}_last_frame.png"
    
    # 确保文件名有正确的扩展名
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        filename += '.png'
    
    # 构建完整的保存路径
    save_path = os.path.join(save_dir, filename)
    
    try:
        # 获取最后一帧
        last_frame = get_asked_frame(video_path, opt)
        
        # 使用cv2保存图像（需要将RGB转换为BGR格式）
        cv2.imwrite(save_path, cv2.cvtColor(last_frame, cv2.COLOR_RGB2BGR))
        
        print(f"成功将视频的最后一帧保存到: {save_path}")
        return save_path
        
    except Exception as e:
        raise RuntimeError(f"保存最后一帧失败: {str(e)}")
    
def get_progress_rate(task, agrs):
    video_path = f"{task.eval_video_path}/episode{task.test_num}.mp4"
    fram_last = save_asked_frame_to_dir(video_path, task.save_dir, "last")
    
    try:
        from code_gen import task_info
        task_name = agrs["task_name"].upper()
        if hasattr(task_info, task_name):
            task_info = getattr(task_info, task_name)
    except KeyError:
        raise KeyError("task_name not found in agrs")
    except ImportError:
        raise ImportError("task_info module not found")
    
    response = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system", "content": PROMPT},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url", 
                        "image_url": 
                        {
                            "url": f"file://{fram_last}"
                        },
                    },
                    {
                        "type": "text",
                        "text": f"Task Name: {task_name}\
                            Task States: {task_info.task_states}" 
                    }

                ]
            }
        ],
        max_tokens=1024,
        temperature=0,
    )
    

