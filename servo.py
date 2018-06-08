# coding: utf-8
from machine import Pin, PWM
from time import sleep
from _thread import start_new_thread

class JointServo():
    MIN_ANGLE = 0
    MAX_ANGLE = 180
    MIN_DUTY = 28
    MAX_DUTY = 122
    FREQ = 50

    @classmethod
    def _angleToDuty(cls, angle):
        ang = angle if angle > cls.MIN_ANGLE else cls.MIN_ANGLE
        ang = ang if ang < cls.MAX_ANGLE else cls.MAX_ANGLE
        duty = int((ang - cls.MIN_ANGLE) * (cls.MAX_DUTY - cls.MIN_DUTY) / (cls.MAX_ANGLE - cls.MIN_ANGLE) + cls.MIN_DUTY)
        print(duty)
        return duty

    def __init__(self, pin, angle):
        print(pin)
        self._servo = PWM(Pin(pin), duty=self._angleToDuty(angle), freq=JointServo.FREQ)

    def move(self, angle):
        print(angle)
        self._servo.duty(JointServo._angleToDuty(angle))
