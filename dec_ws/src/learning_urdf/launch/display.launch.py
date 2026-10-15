from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
 
def generate_launch_description():
    # 1. 获取功能包路径（自动找到learning_urdf的位置）
    pkg_path = get_package_share_directory('learning_urdf')
    # 2. URDF文件路径
    urdf_path = os.path.join(pkg_path, 'urdf', 'mbot_base.urdf')
    # 3. RViz配置文件路径
    rviz_path = os.path.join(pkg_path, 'rviz', 'urdf_rviz.rviz')
 
    # 4. 启动RViz节点，加载URDF和RViz配置
    rviz_node = Node(
        package='rviz2',          # RViz功能包
        executable='rviz2',       # RViz可执行文件
        arguments=[
            '-d', rviz_path,      # 加载预配置的RViz文件
            '--ros-args', '-p', f'robot_description:={open(urdf_path).read()}'  # 传递URDF内容给ROS参数
        ]
    )
 
    # 5. 启动关节状态发布节点（显示关节运动，本例固定，可选）
    joint_state_pub_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui'  # 带GUI的关节控制（可拖动关节运动）
    )
 
    # 6. 启动机器人状态发布节点（发布TF树，让RViz显示连杆关系）
    robot_state_pub_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        arguments=[urdf_path]  # 传入URDF文件
    )
 
    return LaunchDescription([
        joint_state_pub_node,
        robot_state_pub_node,
        rviz_node
    ])