#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 14:11:08 2019

@author: frizzo
"""

import skfuzzy as fuzz
import skfuzzy.control as ctrl
import numpy as np


def get(): 
    sensor_names = ['centerLeftSensor',
                    'centerRightSensor',
                    'leftSensor',
                    'rightSensor']
    
    wheel_names = ['leftWheelVel',
                   'rightWheelVel']
    
    sensors = {sensor_name: ctrl.Antecedent(np.arange(0, 2000, 1), sensor_name) for sensor_name in sensor_names}
    orientation  = ctrl.Antecedent(np.arange(-181, 181, 0.1), 'orientation')
    wheels = {wheel_name: ctrl.Consequent(np.arange(-5, 5, 0.1), wheel_name) for wheel_name in wheel_names}
    
    for sensor in sensors.values():
        sensor['longe']       = fuzz.trimf(sensor.universe, [0, 0, 500])
        sensor['perto']       = fuzz.trapmf(sensor.universe, [250, 750, 1000, 1750])
        sensor['muitoPerto'] = fuzz.trapmf(sensor.universe, [1000, 1500, 2000, 2000])
    
    orientation['esquerda']       = fuzz.trimf(orientation.universe, [-181, -90, 0])
    orientation['meio']     = fuzz.trapmf(orientation.universe, [-45, -30, 30, 45])
    orientation['direita']      = fuzz.trimf(orientation.universe, [0, 90, 181])
    
    for wheel in wheels.values():
        wheel['trasRapido']   = fuzz.trimf(wheel.universe, [-5, -5, -2])
        wheel['trasDevagar']   = fuzz.trimf(wheel.universe, [-3,   -1.5, 0])
        wheel['parado']       = fuzz.trimf(wheel.universe, [-0.2, 0, 0.2])
        wheel['frenteDevagar']   = fuzz.trimf(wheel.universe, [0, 1.5, 3])
        wheel['frenteRapido']   = fuzz.trimf(wheel.universe, [2, 5, 5])
    
    wheelRules = [
      ctrl.Rule(orientation['meio'] & \
                sensors['leftSensor']['longe'] & \
                sensors['centerLeftSensor']['longe'] & \
                sensors['rightSensor']['longe'] & \
                sensors['centerRightSensor']['longe'],
                [wheels['leftWheelVel']['frenteRapido'], wheels['rightWheelVel']['frenteRapido']]),
                
      ctrl.Rule(orientation['meio'] & \
                sensors['leftSensor']['perto'] & \
                sensors['centerLeftSensor']['perto'] & \
                sensors['rightSensor']['longe'] & \
                sensors['centerRightSensor']['longe'],
                [wheels['leftWheelVel']['frenteRapido'], wheels['rightWheelVel']['frenteDevagar']]),
                
#      ctrl.Rule(orientation['meio'] & \
#                sensors['leftSensor']['longe'] & \
#                sensors['centerLeftSensor']['perto'] & \
#                sensors['rightSensor']['perto'] & \
#                sensors['centerRightSensor']['longe'],
#                [wheels['leftWheelVel']['frenteDevagar'], wheels['rightWheelVel']['frenteRapido']]),
                
      ctrl.Rule(orientation['meio'] & \
                sensors['leftSensor']['longe'] & \
                sensors['centerLeftSensor']['longe'] & \
                sensors['rightSensor']['perto'] & \
                sensors['centerRightSensor']['perto'],
                [wheels['leftWheelVel']['frenteDevagar'], wheels['rightWheelVel']['frenteRapido']]),
                
      ctrl.Rule(orientation['direita'] & \
                sensors['leftSensor']['perto'] & \
                sensors['centerLeftSensor']['longe'] & \
                sensors['rightSensor']['longe'] & \
                sensors['centerRightSensor']['longe'],
                [wheels['leftWheelVel']['frenteRapido'], wheels['rightWheelVel']['frenteRapido']]),
                
      ctrl.Rule(orientation['direita'] & \
                sensors['leftSensor']['longe'] & \
                sensors['centerLeftSensor']['longe'],
                [wheels['leftWheelVel']['parado'], wheels['rightWheelVel']['frenteRapido']]),
                
      ctrl.Rule(orientation['direita'] & \
                sensors['leftSensor']['perto'] & \
                sensors['centerLeftSensor']['perto'] & \
                sensors['rightSensor']['perto'] & \
                sensors['centerRightSensor']['perto'],
                [wheels['leftWheelVel']['parado'], wheels['rightWheelVel']['frenteRapido']]),
                
      ctrl.Rule(orientation['direita'] & \
                sensors['leftSensor']['perto'] & \
                sensors['centerLeftSensor']['perto'] & \
                sensors['rightSensor']['longe'] & \
                sensors['centerRightSensor']['longe'],
                [wheels['leftWheelVel']['frenteRapido'], wheels['rightWheelVel']['frenteDevagar']]),
                
      ctrl.Rule(orientation['esquerda'] & \
                sensors['leftSensor']['longe'] & \
                sensors['centerLeftSensor']['longe'] & \
                sensors['rightSensor']['perto'] & \
                sensors['centerRightSensor']['longe'],
                [wheels['leftWheelVel']['frenteRapido'], wheels['rightWheelVel']['frenteRapido']]),
                
      ctrl.Rule(orientation['esquerda'] & \
                sensors['rightSensor']['longe'] & \
                sensors['centerRightSensor']['longe'],
                [wheels['leftWheelVel']['frenteRapido'], wheels['rightWheelVel']['parado']]),
                
      ctrl.Rule(orientation['esquerda'] & \
                sensors['leftSensor']['perto'] & \
                sensors['centerLeftSensor']['perto'] & \
                sensors['rightSensor']['perto'] & \
                sensors['centerRightSensor']['perto'],
                [wheels['leftWheelVel']['frenteRapido'], wheels['rightWheelVel']['parado']]),
                
      ctrl.Rule(orientation['esquerda'] & \
                sensors['leftSensor']['longe'] & \
                sensors['centerLeftSensor']['longe'] & \
                sensors['rightSensor']['perto'] & \
                sensors['centerRightSensor']['perto'],
                [wheels['leftWheelVel']['frenteDevagar'], wheels['rightWheelVel']['frenteRapido']]),
    
      ctrl.Rule(sensors['centerLeftSensor']['muitoPerto'] | sensors['centerLeftSensor']['muitoPerto'], [wheels['leftWheelVel']['frenteRapido'], wheels['rightWheelVel']['trasRapido']]),
      ctrl.Rule(sensors['centerRightSensor']['muitoPerto'] | sensors['centerRightSensor']['muitoPerto'], [wheels['rightWheelVel']['frenteDevagar'], wheels['leftWheelVel']['parado']]),
      
      ctrl.Rule(~sensors['leftSensor']['longe'], [wheels['leftWheelVel']['frenteRapido'], wheels['rightWheelVel']['frenteDevagar']]),
      ctrl.Rule(~sensors['rightSensor']['longe'], [wheels['rightWheelVel']['frenteRapido'], wheels['leftWheelVel']['frenteDevagar']]),
      
      ctrl.Rule(~sensors['centerLeftSensor']['longe'], [wheels['leftWheelVel']['frenteRapido'], wheels['rightWheelVel']['parado']]),
      ctrl.Rule(~sensors['centerRightSensor']['longe'], [wheels['rightWheelVel']['frenteRapido'], wheels['leftWheelVel']['parado']]),
    ]
    
    wheelControl = ctrl.ControlSystem(wheelRules)
    return ctrl.ControlSystemSimulation(wheelControl)