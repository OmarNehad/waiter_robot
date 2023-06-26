from launch import LaunchDescription
import launch_ros.actions
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    return LaunchDescription([
        launch_ros.actions.Node(
          parameters=[
            get_package_share_directory("waiter_robot") + '/config/mapper_params_localization.yaml'
          ],
          package='slam_toolbox',
          executable='localization_slam_toolbox_node',
          name='slam_toolbox',
          output='screen'
        )
    ])


# ACML LOCALITZATION
# ros2 launch nav2_bringup localization_launch.py map:=./my_map_save.yaml use_sim_time:=true
# set intial pose
# set to transient local
