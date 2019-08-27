import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__+'/../'))

DATA_DIR = os.path.join(ROOT_DIR + '/data/')
DATA_RAW_DIR = os.path.join(DATA_DIR + 'raw/')
DATA_PROCESSED_DIR = os.path.join(DATA_DIR + 'processed/')
PROJECT_DIR = os.path.join(ROOT_DIR + '/mpvr/')
DATAMANGER_DIR = os.path.join(PROJECT_DIR + 'datamanger/')

UTILS_DIR = os.path.join(PROJECT_DIR + 'utils/')

SECTIONS = ['THREEDI_2018', 'MOTION_DEVICE_2018']

THREEDI_2018 = {'dir': 'THREEDI_2018/',
                'name': 'THREEDI_2018',
                'scenarios': ['3DI_{:02}'.format(i) for i in range(1, 31)]}
MOTION_DEVICE_2018 = {'dir': 'MotionDevice_2018/',
                      'name': 'MotionDevice_2018',
                      'scenarios': ['S1_pitch', 'S1_yaw', 'S1_roll', 'S1_surge', 'S1_heave', 'S1_sway',
                                    'S2_pitch', 'S2_yaw', 'S2_roll', 'S2_surge', 'S2_heave', 'S2_sway',
                                    'S3_pitch', 'S3_yaw', 'S3_roll', 'S3_surge', 'S3_heave', 'S3_sway',
                                    'S4', 'S5', 'S6']}
TAGS = {
    'tbl': {'dir':'table/', 'ext':'.csv'},
    'grp': {'dir':'graph/', 'ext':'.png'},

    'time': {'title': 'Time'},
    'timediff': {'title': 'Timediff'},
    'index': {'title': 'Index'},
    'incidence': {'title': 'Incidence'},
    'pvalue': {'title': 'P-value'},
    'pearson': {'title': 'PLCC'},
    'spearmanr': {'title': 'SROCC'},
    'kendalltau': {'title': 'KENDALL'},

    'cor': {'dir':'Correlation/', 'title': 'Correlation'},
    'mpe': {'dir':'MPEntropy/', 'title':'MPEntropy'},
    'ent': {'dir':'Entropy/', 'title':'Entropy'},
    # 'mot': {'dir':'Motion/', 'title':'motion'},
    # 'prob': {'dir':'probability/', 'title':'probability'},
    # 'cml': {'dir':'cumulative/'},
    # 'dif': {'dir':'difference/'}
}
