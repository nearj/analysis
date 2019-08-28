from .definitions import *

class ScenarioSetting():
    def __init__(self, name, motion_data, video_data, incidence_data):
        self.name = name
        self.motion_data = motion_data
        self.video_data = video_data

class RawData:
    def __init__(self, path):
        self.path = path


class MotionData(RawData):
    def __init__(self, path, sensored_axes_tag, motion_seperator, is_classified,
                 axes = ['pitch', 'yaw', 'roll', 'surge', 'heave', 'sway']):
        super(MotionData, self).__init__(path)
        self.sensored_axes_tag = sensored_axes_tag
        self.motion_seperator = motion_seperator
        self.is_classified = is_classified
        self.axes = axes

class VideoData(RawData):
    def __init__(self, path, extension, width, height):
        super(VideoData, self).__init__(path)
        self.extension = extension
        self.width = width
        self.height = height

class Config:
    """ Configure for MPVR experiment.
    :var DATA_MANAGER: defualt raw data manager configure.
    :type DATA_MANAGER: dict
    :var THREEDI: stands for 3DI data set
    :type THREEDI: dict
    :var UOS2018: stands for university of seoul data set at 2018
    :type UOS2018: dict
    """
    def __init__(self,
                 scenario_name: str,
                 motion_data: MotionData,
                 video_data: VideoData,
                 incidence_data_path,
                 timestamp_path,
                 save_result_path,
                 target_sampling_rate = 3):
        self.scenario_name = scenario_name
        self.motion_data = motion_data
        self.video_data = video_data
        self.incidence_data_path = incidence_data_path
        self.timestamp_path = timestamp_path
        self.save_result_path = save_result_path
        self.target_sampling_rate = target_sampling_rate

    @staticmethod
    def section_list():
        return SECTIONS

    @staticmethod
    def get_section_scenarios(section):
        return globals()[section]['scenarios']

    @staticmethod
    def get_tags():
        return TAGS

    @classmethod
    def get_config(cls, section, scenario_name):
        return getattr(cls, str.lower(section))(scenario_name)


    @classmethod
    def threedi_2018(cls, scenario_name):
        sensored_axes_tag = None
        motion_seperator = [-0.8, -0.2, 0.2, 0.8]

        if scenario_name == '3DI_00':
            sensored_axes_tag = {'pitch': 'SensorPitch', 'roll': 'SensorRoll'}
            extension = '.png'
            width = 1
            height = 1

        else:
            sensored_axes_tag = {'pitch': 'PitchEulerAngle', 'roll': 'RollEulerAngle'}
            extension = '.mp4'
            width = 1
            height = 1

        default_raw_path    = DATA_RAW_DIR + THREEDI_2018['dir']
        motion_data_path    = default_raw_path + 'motion/' + scenario_name + '.csv'
        video_data_path     = default_raw_path + 'video/' + scenario_name + '.mp4'
        incidence_data_path = default_raw_path + 'incidence/' + scenario_name + '.csv'
        timestamp_path      = default_raw_path + 'timestamp/' + scenario_name + '.csv'

        save_result_path    = DATA_PROCESSED_DIR + 'result/' + THREEDI_2018['dir']
        motion_data         = MotionData(motion_data_path,
                                         sensored_axes_tag,
                                         motion_seperator,
                                         False)
        video_data          = VideoData(video_data_path,
                                        extension,
                                        width,
                                        height)
        return cls(scenario_name, motion_data, video_data, incidence_data_path, timestamp_path,
                   save_result_path)

    @classmethod
    def motion_device_2018(cls, scenario_name):
        sensored_axes_tag = {}
        motion_seperator = [-0.8, -0.2, 0.2, 0.8]
        if scenario_name in ['S1_pitch', 'S2_pitch', 'S3_pitch', 'S4', 'S6']:
            sensored_axes_tag['pitch'] = 'pitch'
        if scenario_name in ['S1_yaw', 'S2_yaw', 'S3_yaw', 'S5', 'S6']:
            sensored_axes_tag['yaw'] = 'yaw'
        if scenario_name in ['S1_roll', 'S2_roll', 'S3_roll', 'S5', 'S6']:
            sensored_axes_tag['roll'] = 'roll'
        if scenario_name in ['S1_surge', 'S2_surge', 'S3_surge', 'S4', 'S5', 'S6']:
            sensored_axes_tag['surge'] = 'surge'
        if scenario_name in ['S1_heave', 'S2_heave', 'S3_heave']:
            sensored_axes_tag['heave'] = 'heave'
        if scenario_name in ['S1_sway', 'S2_sway', 'S3_sway']:
            sensored_axes_tag['sway'] = 'sway'

        default_raw_path    = DATA_RAW_DIR + MOTION_DEVICE_2018['dir']
        motion_data_path    = default_raw_path + 'motion/' + scenario_name + '.csv'
        video_data_path     = default_raw_path + 'video/' + scenario_name + '.mp4'
        incidence_data_path = default_raw_path + 'incidence/' + scenario_name + '.csv'
        timestamp_path      = default_raw_path + 'timestamp/' + scenario_name + '.csv'

        save_result_path    = DATA_PROCESSED_DIR + 'result/' + MOTION_DEVICE_2018['dir']
        motion_data         = MotionData(motion_data_path,
                                         sensored_axes_tag,
                                         motion_seperator,
                                         True)
        video_data          = VideoData(video_data_path,
                                        '.mp4',
                                        1,
                                        1)
        return cls(scenario_name, motion_data, video_data, incidence_data_path, timestamp_path,
                   save_result_path)





    # ###########################################################################
    # #                                 UOS2018                                 #
    # ###########################################################################
    # UOS2018 = \
    # {
    #     'scenarios':
    #     {
    #         'S1_pitch':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                     'pitch'
    #                 ],
    #                 'time': 20,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 20,
    #                 'fps': 60
    #             }
    #         },
    #         'S1_yaw':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                     'yaw'
    #                 ],
    #                 'time': 20,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 20,
    #                 'fps': 60
    #             }
    #         },
    #         'S1_roll':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                     'roll'
    #                 ],
    #                 'time': 20,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 20,
    #                 'fps': 60
    #             }
    #         },
    #         'S1_surge':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                 ],
    #                 'time': 20,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 20,
    #                 'fps': 60
    #             }
    #         },
    #         'S1_heave':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                     'heave'
    #                 ],
    #                 'time': 10,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 10,
    #                 'fps': 60
    #             },
    #         },
    #         'S1_sway':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                 ],
    #                 'time': 20,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 20,
    #                 'fps': 60
    #             }
    #         },
    #         'S2_pitch':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                     'pitch'
    #                 ],
    #                 'time': 20,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 20,
    #                 'fps': 60
    #             },
    #         },
    #         'S2_yaw':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                     'yaw'
    #                 ],
    #                 'time': 20,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 20,
    #                 'fps': 60
    #             }
    #         },
    #         'S2_roll':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                     'roll'
    #                 ],
    #                 'time': 20,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 20,
    #                 'fps': 60
    #             },
    #         },
    #         'S2_surge':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                 ],
    #                 'time': 20,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 20,
    #                 'fps': 60
    #             },
    #         },
    #         'S2_heave':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                     'heave'
    #                 ],
    #                 'time': 10,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 10,
    #                 'fps': 60
    #             },
    #         },
    #         'S2_sway':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                 ],
    #                 'time': 20,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 20,
    #                 'fps': 60
    #             },
    #         },
    #         'S3_pitch':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                     'pitch'
    #                 ],
    #                 'time': 20,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 20,
    #                 'fps': 60
    #             },
    #         },
    #         'S3_yaw':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                     'yaw'
    #                 ],
    #                 'time': 20,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 20,
    #                 'fps': 60
    #             },
    #         },
    #         'S3_roll':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                     'roll'
    #                 ],
    #                 'time': 20,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 20,
    #                 'fps': 60
    #             },
    #         },
    #         'S3_surge':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                 ],
    #                 'time': 20,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 20,
    #                 'fps': 60
    #             },
    #         },
    #         'S3_heave':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                     'heave'
    #                 ],
    #                 'time': 10,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 10,
    #                 'fps': 60
    #             },
    #         },
    #         'S3_sway':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                 ],
    #                 'time': 20,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 20,
    #                 'fps': 60
    #             },
    #         },
    #         'S4':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                     'pitch, surge'
    #                 ],
    #                 'time': 60,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 60,
    #                 'fps': 60
    #             },
    #         },
    #         'S5':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                     'yaw', 'roll', 'surge'
    #                 ],
    #                 'time': 60,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 60,
    #                 'fps': 60
    #             },
    #         },
    #         'S6':
    #         {
    #             'motion':
    #             {
    #                 'extension': '.txt',
    #                 'sensored':
    #                 [
    #                     'pitch', 'yaw', 'roll', 'surge'
    #                 ],
    #                 'time': 60,
    #                 'sampling_rate': 3 #hz
    #             },
    #             'video':
    #             {
    #                 'extension': '.mp4',
    #                 'resolution':
    #                 {
    #                     'width': 1024,
    #                     'height': 768
    #                 },
    #                 'time': 60,
    #                 'fps': 60
    #             },
    #         },
    #     }
    # }

    # ###########################################################################
    # #                                   3DI                                   #
    # ###########################################################################
    # THREEDI = \
    # {
    #     'scenarios':
    #     {
    #         '3DI': 2636
    #     },
    #     'motion':
    #     {
    #         'extension': '.csv',
    #         'sensored': {
    #             'pitch': 'SensorPitch',
    #             # 'yaw': 'SensorYaw',
    #             'roll': 'SensorRoll'},
    #         'sampling_rate': None # not uniform
    #     },
    #     'video':
    #     {
    #         'extension': '.png',
    #         'resolution':
    #         {
    #             'width': 352,
    #             'height': 240
    #         },
    #         'fps': 25,
    #         'time': 105.40 # 1m 45.40 sec
    #     },
    #     'time':
    #     {
    #         'sampling': 'non_uniform',
    #         'time_column': 'Time',
    #         'start_index': 1,
    #         'end_index': 2636,
    #         'step_min': 0.30,
    #         'step_max': 0.36
    #     }
    # }
