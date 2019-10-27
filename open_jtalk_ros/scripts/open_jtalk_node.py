#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Speak string topic by open_jtalk
"""

import rospy
import rospkg
from std_msgs.msg import String
import subprocess

def openjtalk(message, voicefilepath, speak_speed=1.0):
    open_jtalk = ['open_jtalk']
    dictionarydir= ['-x', '/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice= ['-m', voicefilepath]
    speed = ['-r', str(speak_speed)]
    outwav = ['-ow', '/dev/stdout']
    cmd_jtalk = open_jtalk+dictionarydir+htsvoice+speed+outwav

    aplay = ['aplay', '-q']

    p1 = subprocess.Popen(cmd_jtalk, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(aplay, stdin=p1.stdout)
    p1.stdin.write(message)
    p1.stdin.close()
    p1.wait()
    p2.wait()

    return;

class OpenJtalkROS(object):
    def __init__(self, ):
        rospy.init_node('open_jtalk_ros_node', anonymous=False)
        rospy.loginfo("start speaking")
        self.voicefilepath = rospkg.RosPack().get_path("open_jtalk_ros")+'/hts-voice/htsvoice-tohoku-f01/tohoku-f01-neutral.htsvoice'

    def __speaker(self, data):
        rospy.loginfo("openjtalk says: %s", data.data)

        openjtalk(data.data, self.voicefilepath)

    def run(self):
        rospy.Subscriber("chatter", String, self.__speaker, queue_size=1)
        rospy.spin()

if __name__ == '__main__':
    try:
        open_jtalk_ros = OpenJtalkROS()
        open_jtalk_ros.run()
    except rospy.ROSInterruptException :
        pass
