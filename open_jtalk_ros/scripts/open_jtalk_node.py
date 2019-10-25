#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Speak string topic by open_jtalk
"""

import rospy
import rospkg
from std_msgs.msg import String
import subprocess

class OpenJtalkROS(object):
    def __init__(self, ):
        rospy.init_node('open_jtalk_ros_node', anonymous=True)
        rospy.loginfo("start speaking")

    def __speaker(self, data):
        rospy.loginfo("%s", data.data)

        open_jtalk = ['open_jtalk']
        mech = ['-x', '/var/lib/mecab/dic/open-jtalk/naist-jdic']
        htsvoice= ['-m', rospkg.RosPack().get_path("open_jtalk_ros")+'/hts-voice/htsvoice-tohoku-f01/tohoku-f01-happy.htsvoice']
        speed = ['-r', '1.0']
        #outwav = ['-ow', '/dev/stdout']
        outwav = ['-ow', '/tmp/open_jtalk.wav']
        cmd = open_jtalk+mech+htsvoice+speed+outwav

        c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        c.stdin.write(data.data)
        c.stdin.close()
        c.wait()
        aplay = ['aplay', '-q', '/tmp/open_jtalk.wav']
        wr = subprocess.Popen(aplay)
        wr.wait()

        rospy.loginfo("spoke")

    def run(self):
        rospy.Subscriber("chatter", String, self.__speaker)
        rospy.spin()

if __name__ == '__main__':
    try:
        open_jtalk_ros = OpenJtalkROS()
        open_jtalk_ros.run()
    except rospy.ROSInterruptException :
        pass
