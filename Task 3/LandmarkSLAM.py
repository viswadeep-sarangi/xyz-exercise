from typing import List


def encompasses_all_modules(start_num: int, end_num: int, module_landmarks: List[List[int]]) -> bool:
    all_modules_have_values = True
    for single_module in module_landmarks:
        module_has_value = False
        for landmark in single_module:
            if end_num >= landmark >= start_num:
                module_has_value = True
        all_modules_have_values = all_modules_have_values and module_has_value
    return all_modules_have_values


def smallest_overlap_of_landmarks(module_landmarks: List[List[int]]) -> (int, int):
    flat_list = []
    for module in module_landmarks:
        flat_list += module
    flat_list.sort()
    start_ind = 0
    end_ind = len(flat_list)
    continueLoop = True

    while continueLoop:

        continueLoop = False
        curr_start_num = flat_list[start_ind]
        curr_end_num = flat_list[end_ind]
        new_start_num = flat_list[start_ind + 1]
        new_end_num = flat_list[end_ind - 1]

        if encompasses_all_modules(curr_start_num, new_end_num, module_landmarks):
            end_ind -= 1
            continueLoop = True
        if encompasses_all_modules(new_start_num, new_end_num, module_landmarks):
            start_ind += 1
            continueLoop = True

    return start_ind, end_ind


class LandmarkSLAM:

    def __init__(self):
        self.landmarks = []

    def add_landmark(self, landmark: int) -> List[int]:
        self.landmarks.append(landmark)
        self.landmarks.sort()
        return self.landmarks
