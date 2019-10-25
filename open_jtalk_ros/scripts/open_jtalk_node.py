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
    #outwav = ['-ow', '/dev/stdout']
    outwav = ['-ow', '/tmp/open_jtalk.wav']
    cmd = open_jtalk+dictionarydir+htsvoice+speed+outwav

    c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    c.stdin.write(message)
    c.stdin.close()
    c.wait()
    aplay = ['aplay', '-q', '/tmp/open_jtalk.wav']
    wr = subprocess.Popen(aplay)
    wr.wait()

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
