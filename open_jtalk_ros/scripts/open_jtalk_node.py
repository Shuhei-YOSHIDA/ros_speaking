#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Speak string topic by open_jtalk
"""

import rospy
import rospkg
from std_msgs.msg import String
from open_jtalk_ros.msg import Words
from open_jtalk_ros.srv import *
import subprocess


def openjtalk(message, voicefilepath, speak_speed=1.0):
    if speak_speed < 0.1: #speak_speed = 0 is dangerous
        rospy.logwarn("Too low speak_speed %s is set, then reset to default", speak_speed)
        speak_speed = 1.0

    open_jtalk = ['open_jtalk']
    dictionarydir= ['-x', '/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice= ['-m', voicefilepath]
    speed = ['-r', str(speak_speed)]
    outwav = ['-ow', '/dev/stdout']
    cmd_jtalk = open_jtalk+dictionarydir+htsvoice+speed+outwav

    aplay = ['aplay', '-q']

    p1 = subprocess.Popen(cmd_jtalk, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(aplay, stdin=p1.stdout)
    try:
        p1.stdin.write(message.encode()) # For python3(noetic)
    except Exception as e:
        rospy.logdebug('open_jtalk_ros in ROS melodic')
        p1.stdin.write(message) # For python2(melodic)
    p1.stdin.close()
    p1.wait()
    p2.wait()

    return;


class OpenJtalkROS(object):
    def __init__(self, ):
        rospy.init_node('open_jtalk_ros_node', anonymous=False)
        rospy.loginfo("start speaking")
        self.voicefilepath = rospkg.RosPack().get_path("open_jtalk_ros")+'/hts-voice/htsvoice-tohoku-f01/tohoku-f01-neutral.htsvoice'
        self.voice_speed = 1.0

    def __speaker(self, data):
        rospy.loginfo("openjtalk says: %s", data.data)

        openjtalk(data.data, self.voicefilepath, self.voice_speed)

    def __wordsSpeaker(self, data):
        rospy.loginfo("openjtalk says: %s", data.words)

        openjtalk(data.words, data.voice_data_path, data.voice_speed)

    def __setVoiceData(self, req):
        self.voicefilepath = req.voice_data_path # check validity of path
        self.voice_speed = req.voice_speed

        return SetVoiceDataResponse()

    def run(self):
        rospy.Subscriber("chatter", String, self.__speaker, queue_size=1)
        rospy.Subscriber("words", Words, self.__wordsSpeaker, queue_size=1)

        rospy.Service('set_voice_data', SetVoiceData, self.__setVoiceData)

        rospy.spin()

if __name__ == '__main__':
    try:
        open_jtalk_ros = OpenJtalkROS()
        open_jtalk_ros.run()
    except rospy.ROSInterruptException :
        pass
