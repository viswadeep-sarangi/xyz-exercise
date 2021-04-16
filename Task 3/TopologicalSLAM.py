from MetricSLAM import MetricSLAM
import sys
from queue import Queue


class TopologicalSLAM(MetricSLAM):
    def __init__(self, min_feat=0, max_feat=sys.maxsize, max_size=sys.maxsize):
        super().__init__(min_feat=min_feat, max_feat=max_feat, max_size=max_size)
        self.confidence_values = []

    def add_frame(self, frame):
        """
        Overridden from MetricSLAMINterface.
        The tuple input assumes the following format (x, y, z, qw, qx, qy, qz, ext_feat, matched_feat, confidence_value).
        Here 'x,y,z' is the translation in meters
        'qw, qx, qy, qz' is the quaternion rotation
        'ext_feat' is the number of extracted features
        'matched_feat' is the total number of matches
        'confidence_value' is the additional parameter for TopologicalSLAM
        :param frame:
        :return: None
        """
        super().add_frame()
        self.confidence_values.append(frame[-1])

    def max_acc_confidence(self, time_int=5):

        if len(self.confidence_values) < time_int:
            return 0, len(self.confidence_values)

        max_accum_conf = 0
        max_start_index = 0
        for i in range(len(self.confidence_values) - time_int):
            curr_sum = sum(self.confidence_values[i:i + time_int])
            if curr_sum > max_accum_conf:
                max_accum_conf = curr_sum
                max_start_index = i
        return max_start_index, max_start_index + time_int - 1  # -1 to make it inclusive of both indices
