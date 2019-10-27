open_jtalk_ros
====
This code is licensed under the MIT licence.
However, several materials are licensed under other licenses.

# Install

```bash
$ cd catkin_ws/src
$ git clone --recursive https://github.com/Shuhei-YOSHIDA/ros_speaking.git
$ sudo apt install open-jtalk open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001
$ catkin build
```

# open_jtalk_ros package
"open_jtalk_ros.py" node subscribes topics 'chatter'(std_msgs/String) and 'words'(open_jtalk_ros/Words),
then the node speaks the sentence by [Open JTalk](http://open-jtalk.sourceforge.net/).

Voice data, which is included in this repository, is derived from [HTS voice tohoku-f01](https://github.com/icn-lab/htsvoice-tohoku-f01).
This voice data is licensed under the [Creative Commons Attributions 4.0](http://creativecommons.org/licenses/by/4.0/).
