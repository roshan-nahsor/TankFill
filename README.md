# TankFill

In places where water supply is restricted to only a certain duration of time, proper water management is required. It requires manually opening the tap to fill the tank, which is not always possible as a person needs to be there physically available during that time. Hence our project focuses on automated water filling with IoT integration.

## Description
This project includes 2 devices, namely RaspberryPi and esp32 micro-controller. The RaspberryPi is used for hosting the website and esp32 is used for obtaining the height of the water level in the tank by using an Ultasonic Sensor.
This website is built using Django which uses Python language. We chose this framework as it comes with many features built-in, including a database; as well as it will help in easy integration as Raspberry Pi works on Python as well.
Both the devices communicate with each other wirelessly using MQTT protocol, which is a message queuing protocol.

The website will have a login page and new users can only be added by the admin. After login, the user is shown a screen that shows a graph (bar or line) as per the user's choice which will display the amount of water present in the tank.
