bash test_scene_render.sh get_apple1 demo_franka#!/bin/bash

# 检查参数数量是否正确
if [ $# -ne 2 ]; then
    echo "用法: $0 <task_name> <dataset_name>"
    echo "示例: $0 get_apple1 demo_franka"
    exit 1
fi

TASK_NAME=$1
DATASET_NAME=$2

# 设置 PYTHONPATH，确保项目模块可导入（当前目录为项目根目录）
export PYTHONPATH=$(pwd)

# 执行 Python 渲染脚本，传递任务名称和数据集名称
python script/test_scene_render.py "$TASK_NAME" "$DATASET_NAME"