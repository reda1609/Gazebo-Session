from launch import LaunchDescription
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        # 1. Launching robot_state_publisher for bot1
        ExecuteProcess(
            cmd=['ros2', 'run', 'robot_state_publisher', 'robot_state_publisher',
                '~/Gazebo-Session/simple_bot_ws/src/simple_bot/description/bot1.urdf', 
                '__ns:=/bot1'],
            output='screen',
            shell=True,
        ),
        # 2. Launching robot_state_publisher for bot2
        ExecuteProcess(
            cmd=['ros2', 'run', 'robot_state_publisher', 'robot_state_publisher',
                 '~/Gazebo-Session/simple_bot_ws/src/simple_bot/description/bot2.urdf', 
                 '__ns:=/bot2'],
            output='screen',
            shell=True,
        ),
        # 3. Launching Gazebo
        ExecuteProcess(
            cmd=['ros2', 'launch', 'gazebo_ros', 'gazebo.launch.py', 
                'world:=' + '~/Gazebo-Session/simple_bot_ws/src/simple_bot/worlds/DEBI_world'],
            output='screen',
            shell=True,
        ),
        # 4. Spawn entity for bot1 at specific position
        ExecuteProcess(
            cmd=['ros2', 'run', 'gazebo_ros', 'spawn_entity.py', 
                 '-topic', '/bot1/robot_description', '-entity', '/bot1', 
                 '-x', '0.5', '-y', '1.7', '-z', '0.0',  # Position
                 '-R', '0.0', '-P', '0.0', '-Y', '0.0',  # Orientation
                 '__ns:=/bot1'],
            output='screen',
            shell=True,
        ),
        # 5. Spawn entity for bot2 at specific position
        ExecuteProcess(
            cmd=['ros2', 'run', 'gazebo_ros', 'spawn_entity.py', 
                 '-topic', '/bot2/robot_description', '-entity', '/bot2', 
                 '-x', '4.5', '-y', '1.7', '-z', '0.0',  # Position
                 '-R', '0.0', '-P', '0.0', '-Y', '3.14',  # Orientation
                 '__ns:=/bot2'],
            output='screen',
            shell=True,
        ),
    ])
