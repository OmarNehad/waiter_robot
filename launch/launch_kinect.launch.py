import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node



def generate_launch_description():

    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='waiter_robot'
    depthimage_to_laserscan_config = os.path.join(get_package_share_directory('depthimage_to_laserscan'), 'cfg', 'param.yaml')
    config_dir = os.path.join(get_package_share_directory('waiter_robot'),'config')
    
    kinect_sensor = Node(
                package="kinect_ros2",
                executable="kinect_ros2_node",
                name="kinect_ros2",
                namespace="kinect",
    )
    
    cartographer_node = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        name='mapping_node',
        output='screen',
        arguments=['-configuration_directory', config_dir,'-configuration_basename','turtlebot3_lds_2d.lua']

        )
    cartographer_occupancy_grid_node = Node(
        package='cartographer_ros',
        executable='cartographer_occupancy_grid_node',
        name='occupancy_node',
        output='screen'

        )

    depthimage_to_laserscan = Node(
            package='depthimage_to_laserscan',
            executable='depthimage_to_laserscan_node',
            name='depthimage_to_laserscan_node',
            remappings=[('depth', '/kinect/depth/image_raw'),
                        ('depth_camera_info', '/kinect/depth/camera_info'),
                        ('scan','scan')],
            parameters=[depthimage_to_laserscan_config])


    # Launch them all!
    return LaunchDescription([
        kinect_sensor,
        depthimage_to_laserscan,
        #slam_toolbox,
        #start_async_slam_toolbox_node,
    ])


# ros2 launch slam_toolbox online_async_launch.py params_file:=./src/waiter_robot/config/mapper_params_online_async.yaml use_sim_time:=false 
#slam_async_params_file = os.path.join(get_package_share_directory("waiter_robot"),
    #                                   'config', 'mapper_params_online_async.yaml')

    # slam_toolbox = IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource([os.path.join(
    #                 get_package_share_directory("slam_toolbox"),'launch','online_async_launch.py'
    #             )]), launch_arguments={'use_sim_time': 'false', 'params_file':slam_async_params_file}.items()
    # )   


    # start_async_slam_toolbox_node = Node(
    #     parameters=[
    #       slam_async_params_file,
    #       {'use_sim_time': 'false'}
    #     ],
    #     package='slam_toolbox',
    #     executable='async_slam_toolbox_node',
    #     name='slam_toolbox',
    #     output='screen'
    #     )
