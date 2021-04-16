from VisualSLAMInterface import VisualSLAMInterface
import sys
from queue import Queue
import math


class MetricSLAM(VisualSLAMInterface):
    def __init__(self, min_feat=0, max_feat=sys.maxsize, max_size=sys.maxsize):
        self.min_feat = min_feat
        self.max_feat = max_feat
        self.max_size = max_size
        self.frames_queue = Queue(maxsize=self.max_size)
        self.num_frames = 0
        self.latest_frame = None
        self.meters_travelled = 0
        self.avg_num_feat = 0
        self.avg_num_matches = 0

    def add_frame(self, frame):
        """
        Overridden from VisualSLAMInterface.
        The tuple input assumes the following format (x, y, z, qw, qx, qy, qz, ext_feat, matched_feat).
        Here 'x,y,z' is the translation in meters
        'qw, qx, qy, qz' is the quaternion rotation
        'ext_feat' is the number of extracted features
        'matched_feat' is the total number of matches
        :param frame:
        :return: None
        """
        if self.frames_queue.full():
            earliest_frame = self.frames_queue.get()
        if self.latest_frame is not None:
            # Incrementing number of meters travelled
            delta_met = math.sqrt(
                math.pow(self.latest_frame[0] - frame[0], 2) +
                math.pow(self.latest_frame[1] - frame[1], 2) +
                math.pow(self.latest_frame[2] - frame[2], 2)
            )
            self.meters_travelled += delta_met

            # Updating average number of features
            self.avg_num_feat = ((self.avg_num_feat * self.num_frames) + frame[7])/(self.num_frames+1)

            # Updating average number of matches
            self.avg_num_matches = ((self.avg_num_matches * self.num_frames) + frame[8]) / (self.avg_num_matches + 1)

        self.frames_queue.put(frame)
        self.latest_frame = frame
        self.num_frames += 1

        # Checking for early warning signs
        if frame[7] < self.min_feat:
            print("Early Warning Sign: Number of features extracted is less than min_feat")
        if frame[7] > self.max_feat:
            print("Early Warning Sign: Number of features extracted more than max_feat")
