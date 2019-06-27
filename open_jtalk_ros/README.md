open_jtalk_ros
====

# open_jtalk_ros.py
This node subscribes a topic 'chatter'(std_msgs/String),
then the node speaks the sentence by [Open JTalk](http://open-jtalk.sourceforge.net/).

Voice data, which is assigned in this node, is derived from [HTS voice tohoku-f01](https://github.com/icn-lab/htsvoice-tohoku-f01).
You need to install this data to suitable directory.

