from setuptools import setup
import os
from glob import glob

package_name = 'team_logic'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    # Додайте ці два рядки:
    (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    (os.path.join('share', package_name, 'worlds'), glob(os.path.join('worlds', '*.world'))),
],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # ОСЬ ТУТ МАГІЯ: ми кажемо системі, що команда 'markers' 
            # запускає функцію main у файлі markers.py
            'markers = team_logic.markers:main',
            'mover = team_logic.mover_node:main',
        ],
    },
)
