import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('team_logic')
    gazebo_ros_share = get_package_share_directory('gazebo_ros')

    # Шлях до вашого файлу світу
    world_path = os.path.join(pkg_share, 'worlds', 'task1.world')

    # 1. Запуск Gazebo з вашим світом
    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gazebo_ros_share, 'launch', 'gzserver.launch.py')),
        launch_arguments={'world': world_path}.items()
    )
    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gazebo_ros_share, 'launch', 'gzclient.launch.py'))
    )

    # 2. Публікація стану робота (URDF)
    # Тут ми викликаємо ваш основний лаунч, але тільки частину з описом робота
    robot_state_pub = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_share, 'launch', 'start_all.launch.py')),
        launch_arguments={'use_gui': 'false'}.items()
    )

    # 3. Спавн (поява) робота в Gazebo
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'mg400'],
        output='screen'
    )

    return LaunchDescription([
        gzserver,
        gzclient,
        robot_state_pub,
        spawn_robot
    ])
