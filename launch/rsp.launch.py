import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

import xacro


def generate_launch_description():

    # Check if we're told to use sim time i.e in simulation i.e. in gazebo
    use_sim_time = LaunchConfiguration('use_sim_time')

    # This option enables the use of gaezbo diff driver in simualtion as it is more accruate:
    #use_ros2_control = LaunchConfiguration('use_ros2_control')

    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('waiter_robot'))
    xacro_file = os.path.join(pkg_path,'description','robot.urdf.xacro')
    #robot_description_config = xacro.process_file(xacro_file).toxml()
    robot_description_config = Command(['xacro ', xacro_file, ' sim_mode:=', use_sim_time])
    
    # Create a robot_state_publisher node
    params = {'robot_description': robot_description_config, 'use_sim_time': use_sim_time}
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )


    # Launch!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'),


        # DeclareLaunchArgument(
        #     'use_ros2_control',
        #     default_value='true',
        #     description='Use ros2_control if true'),

        node_robot_state_publisher
    ])