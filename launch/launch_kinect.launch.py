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
    
    kinect_sensor = Node(
                package="kinect_ros2",
                executable="kinect_ros2_node",
                name="kinect_ros2",
                namespace="kinect",
                
    )
    

    depthimage_to_laserscan = Node(
            package='depthimage_to_laserscan',
            executable='depthimage_to_laserscan_node',
            name='depthimage_to_laserscan_node',
            remappings=[('depth', '/kinect/depth/image_raw'),
                        ('depth_camera_info', '/kinect/depth/camera_info'),
            ],
            parameters=[depthimage_to_laserscan_config])


    # Launch them all!
    return LaunchDescription([
        kinect_sensor,
        depthimage_to_laserscan,
    ])

