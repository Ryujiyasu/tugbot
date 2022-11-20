import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    pkg_ros_ign_gazebo = get_package_share_directory('ros_ign_gazebo')
    pkg_tugbot = get_package_share_directory('tugbot')

    ign_resource_path = SetEnvironmentVariable(
        name='IGN_GAZEBO_RESOURCE_PATH',
        value=[
            os.path.join(pkg_tugbot, 'worlds')])

    ign_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_ign_gazebo, 'launch', 'ign_gazebo.launch.py')),
        launch_arguments={
           'ign_args': '-r tugbot_warehouse.sdf'
        }.items(),
    )

    # urdf

    urdf_dir = os.path.join(pkg_tugbot, 'urdf')
    urdf_file = os.path.join(urdf_dir, 'tugbot.urdf')
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()
    robot_description = {"robot_description": robot_desc}

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[robot_description],
    )

    # Bridge
    bridge = Node(
        package='ros_ign_bridge',
        executable='parameter_bridge',
        arguments=[
            '/world/world_demo/model/tugbot/link/scan_omni/sensor/scan_omni/scan/points@sensor_msgs/msg/PointCloud2@ignition.msgs.PointCloudPacked'
        ],
        remappings=[
            ('/world/world_demo/model/tugbot/link/scan_omni/sensor/scan_omni/scan/points', 'points'),
        ],
        output='screen'
    )

    return LaunchDescription([
        ign_resource_path,
        ign_gazebo,
        bridge,
        robot_state_publisher
    ])
