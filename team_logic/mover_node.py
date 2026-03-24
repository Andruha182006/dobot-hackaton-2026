#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import time
import math

class DobotMover(Node):
    def __init__(self):
        super().__init__('dobot_mover')
        self.joint_pub = self.create_publisher(JointState, '/mg400/joint_states', 10)
        self.timer = self.create_timer(0.02, self.move_loop)

        self.current_j = [0.0, 0.0, 0.0]
        self.smoothness = 0.05 
        self.start_time = time.time()
        self.get_logger().info('РОБОТ ГОТОВИЙ ДО РУХУ')

    def move_loop(self):
        elapsed_time = time.time() - self.start_time
        cycle_time = elapsed_time % 5.0      # 5 сек на кубик
        total_cycle = elapsed_time % 15.0    # 15 сек на коло

        # 1. ТАРГЕТИ ДЛЯ БАЗИ (Поворот)
        if total_cycle < 5.0:
            target_base = 0.0         # Червоний
        elif total_cycle < 10.0:
            target_base = 1.57        # Зелений
        else:
            target_base = -2.35       # СИНІЙ (Точна координата)

        # 2. МАТЕМАТИКА "ЗГИНАННЯ ВГОРІ"
        # multiplier = 0 (вгорі), multiplier = 1 (торкання кубика)
        multiplier = 0.5 - 0.5 * math.cos((cycle_time / 5.0) * 2 * math.pi)

        # Плече нахиляється від 0.1 (вертикально) до 0.9 (торкання)
        bend_factor = 0.1 + (0.9 * multiplier)
        # Лікоть згинається від 0.0 до 0.5
        elbow_factor = 0.0 + (0.0 * multiplier)

        target_j = [target_base, bend_factor, elbow_factor]

        # 3. ПЛАВНИЙ РУХ
        for i in range(3):
            self.current_j[i] += (target_j[i] - self.current_j[i]) * self.smoothness

        # 4. ПУБЛІКАЦІЯ СТАНУ
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = [
            'mg400_j1', 'mg400_j2_1', 'mg400_j2_2', 
            'mg400_j3_1', 'mg400_j3_2', 'mg400_j4_1', 'mg400_j4_2', 'mg400_j5'
        ]
        
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
