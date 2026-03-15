#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math

class DobotMover(Node):
    def __init__(self):
        super().__init__('dobot_mover')
        
        # Видавець для керування віртуальним роботом в RViz
        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)
        
        # Таймер для оновлення позиції (50 Гц для дуже плавного руху)
        self.timer = self.create_timer(0.02, self.move_loop)
        
        # Початкові кути (всі в нулі)
        self.current_joints = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        
        # --- ЦІЛЬОВІ КУТИ (ПОКИ ЩО ТЕСТОВІ) ---
        # Сюди математик підставить правильні значення для координат кубиків:
        # Кубик 1 (червоний): x: 0.3, y: 0.0, z: 0.0
        # Кубик 2 (зелений):  x: 0.0, y: 0.25, z: 0.0
        # Кубик 3 (синій):    x: -0.25, y: -0.25, z: 0.0
        self.target_joints = [
            [0.5, -0.3, 0.1, 0.0, 0.0, 0.0],  # Для червоного
            [-0.2, 0.4, 0.2, 0.0, 0.0, 0.0],  # Для зеленого
            [0.3, 0.2, -0.1, 0.0, 0.0, 0.0]   # Для синього
        ]
        
        self.target_index = 0  # Індекс поточної цілі (0, 1, 2)
        self.speed = 0.03       # Швидкість руху (менше число = плавніше)
        
        self.get_logger().info('🚀 Dobot Mover Node запущено!')

    def move_loop(self):
        # Створюємо повідомлення
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        # Назви суглобів МАЮТЬ збігатися з моделлю MG400
        msg.name = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']
        
        # Поточна ціль
        target = self.target_joints[self.target_index]
        
        # Плавно рухаємо кожен суглоб до цільового кута
        all_reached = True
        for i in range(6):
            diff = target[i] - self.current_joints[i]
            if abs(diff) > 0.005:  # Якщо різниця ще суттєва
                self.current_joints[i] += diff * self.speed
                all_reached = False
            else:
                # Якщо дуже близько, фіксуємо точно на цілі
                self.current_joints[i] = target[i]
        
        # Якщо досягли цілі - перемикаємось на наступний кубик
        if all_reached:
            self.target_index = (self.target_index + 1) % 3
            self.get_logger().info(f'🎯 Перемикаюсь на кубик {self.target_index + 1}')
        
        # Публікуємо нові кути
        msg.position = self.current_joints
        self.joint_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = DobotMover()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('👋 Вимкнення вузла...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()