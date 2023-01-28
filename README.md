# Ditto : the delivery robot
![3](https://user-images.githubusercontent.com/60263608/215241634-c957b7bc-4646-467a-811b-57b1627128ac.png)



We Jain University robotics team, are currently developing autonomous delivery robot for our college, this project uses many open source softwares and a few softwares buillt inhouse, we aim to make this project open source so many can use our package to develop their own autonomous delivery robots.

![1](https://user-images.githubusercontent.com/60263608/193443207-ad83f952-3ed0-423f-a124-01a2075aa3f0.jpeg)

## INSTALLATION
```bash
cd catkin_ws/src
git clone https://github.com/siddarth09/Ditto.git
cd ..
catkin_make
```

### Hardware Requirements

| Hardware      | No.Required   | Estimated amount|
| ------------- |:-------------:| -----:|
| Motors (depends on bot)with encoders  | 4x2(encoders) |Rs.11000 |
| IMU (MPU6050)     | 1      |  Rs.100 |
| OAK-D lite | 1      |  Rs.16000 |
| GPS module | 1| Rs.400 |

### Simulation 
------------------

Simulation plays an important role in understanding many message types, working on depth camera before having an actual hardware. It also helps in understanding the robot model (if you have followed the same measurements) in a real physics world. 

> To use GAZEBO

```bash
roslaunch ditto world.launch
```






