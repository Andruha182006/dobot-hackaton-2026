from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_bringup = get_package_share_directory('mg400_bringup')
    pkg_team = get_package_share_directory('team_logic')

    # Запускаємо заводський дисплей, але кажемо йому НЕ запускати GUI
    robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_bringup, 'launch', 'display.launch.py')
        ),
        launch_arguments={
            'use_gui': 'false',
            'publish_joint_state': 'false' # Це важливо, щоб не було конфлікту з твоїм mover.py
        }.items() 
    )

    # Твій вузол з маркерами (кубиками)
    markers_node = Node(
        package='team_logic',
        executable='markers',
        name='my_markers'
    )

    return LaunchDescription([
        robot_launch,
        markers_node
    ])
