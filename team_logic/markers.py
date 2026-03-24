#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker, MarkerArray

class MarkerPublisher(Node):
    def __init__(self):
        super().__init__('marker_publisher')
        # Створюємо видавця для масиву маркерів
        self.publisher = self.create_publisher(MarkerArray, '/visualization_marker_array', 10)
        # Публікуємо кожну секунду, щоб вони не зникали
        self.timer = self.create_timer(1.0, self.publish_markers)
        self.get_logger().info('Вузол маркерів запущено. Розставляю кубики...')

    def publish_markers(self):
        marker_array = MarkerArray()
        
        # Наші координати (x, y, z) та кольори (r, g, b)
        coords = [
            {'pos': [0.3, 0.0, 0.025],   'color': [1.0, 0.0, 0.0], 'id': 0}, # Червоний
            {'pos': [0.0, 0.25, 0.025],  'color': [0.0, 1.0, 0.0], 'id': 1}, # Зелений
            {'pos': [-0.2, -0.2, 0.025], 'color': [0.0, 0.0, 1.0], 'id': 2}  # Синій
        ]
        
        for item in coords:
            marker = Marker()
            marker.header.frame_id = "mg400_base_link"
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.id = item['id']
            marker.type = Marker.CUBE
            marker.action = Marker.ADD
            
            # Позиція
            marker.pose.position.x = item['pos'][0]
            marker.pose.position.y = item['pos'][1]
            marker.pose.position.z = item['pos'][2]
            
            # Розмір кубика (5х5х5 см)
            marker.scale.x = 0.05
            marker.scale.y = 0.05
            marker.scale.z = 0.05
            
            # Колір та прозорість
            marker.color.r = item['color'][0]
            marker.color.g = item['color'][1]
            marker.color.b = item['color'][2]
            marker.color.a = 1.0 # Повна видимість
            
            marker_array.markers.append(marker)
        
        self.publisher.publish(marker_array)

def main(args=None):
    rclpy.init(args=args)
    node = MarkerPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
