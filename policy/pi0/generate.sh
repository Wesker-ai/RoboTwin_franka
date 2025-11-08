data_dir=${1}
repo_id=${2}
uv run examples/franka-panda/convert_franka_data_to_lerobot.py --raw_dir $data_dir --repo_id $repo_id
