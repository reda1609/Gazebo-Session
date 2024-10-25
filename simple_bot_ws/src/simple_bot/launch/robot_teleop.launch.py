# teleop_joy_launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Joy node
        Node(
            package='joy',
            executable='joy_node',
            name='joy_node',
        ),

        # Teleop Twist Joy node
        Node(
            package='teleop_twist_joy',
            executable='teleop_node',
            name='teleop_twist_joy_node',
            parameters=[{'require_enable_button': False}, 
                        {'axis_linear.x': 1},
                        {'axis_angular.z': 2}],
            # remappings=[
            #     ('/cmd_vel', '/robot/cmd_vel')  # Optionally remap cmd_vel topic
            # ]
        ),
    ])
