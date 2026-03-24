#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import time

class DobotMover(Node):
    def __init__(self):
        super().__init__('dobot_mover')
        self.joint_pub = self.create_publisher(JointState, '/mg400/joint_states', 10)
        self.timer = self.create_timer(0.02, self.move_loop)

        # Поточні позиції суглобів (з яких починаємо)
        self.current_j = [0.0, 0.0, 0.0]
        # Коефіцієнт плавності (0.01 - дуже повільно, 0.1 - швидко)
        self.smoothness = 0.05 

        self.start_time = time.time()
        self.get_logger().info('🚀 ПЛАВНИЙ РУХ ЗАПУЩЕНО!')

    def move_loop(self):
        elapsed_time = time.time() - self.start_time
        cycle_time = elapsed_time % 15.0

        # Визначаємо ЦІЛЬОВУ позицію (куди хочемо прийти)
        if cycle_time < 5.0:
            target_j = [0.0, 0.4, 0.4]    # Червоний
        elif cycle_time < 10.0:
            target_j = [1.57, 0.5, 0.5]   # Зелений
        else:
            target_j = [-2.35, 0.3, 0.3]  # Синій

        # МАГІЯ ПЛАВНОСТІ: наближаємо поточне значення до цільового потроху
        for i in range(3):
            # Формула: поточне = поточне + (ціль - поточне) * швидкість
            self.current_j[i] += (target_j[i] - self.current_j[i]) * self.smoothness

        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['mg400_j1', 'mg400_j2_1', 'mg400_j2_2', 'mg400_j3_1', 'mg400_j3_2', 'mg400_j4_1', 'mg400_j4_2', 'mg400_j5']
        
        msg.position = [
            self.current_j[0], 
            self.current_j[1], self.current_j[1], 
            -self.current_j[2], -self.current_j[2], 
            0.0, 0.0, 0.0
        ]

        self.joint_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = DobotMover()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
