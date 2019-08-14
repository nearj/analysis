class Config:
    """ Configure for MPVR experiment.
    :var DATA_MANAGER: defualt raw data manager configure.
    :type DATA_MANAGER: dict
    :var THREEDI: stands for 3DI data set
    :type THREEDI: dict
    :var UOS2018: stands for university of seoul data set at 2018
    :type UOS2018: dict

    """
    ###########################################################################
    #                               DATA MANAGER                              #
    ###########################################################################
    DATA_MANAGER = \
    {
        'LOAD_MOTION_DIR': './data/raw/motion/',
        'LOAD_VIDEO_DIR': './data/raw/video/',

        'SAVE_DIR': './data/',
        'SAVE_OPTIONS':
        {
            'pre': 'preprocessed/',
            'pro': 'processed/',
            'pst': 'postprocessed/',

            'tbl': 'table/',
            'grp': 'graph/',

            'mpe': 'MPentropy/',
            'ent': 'entropy/',
            'mot': 'motion/',
            'prob': 'probability/',
            'cml': 'cumulative/',
            'dif': 'difference/',
        },
        'LOAD_OPTIONS':[],
        'BIN_SEPERATOR': [-0.8, -0.2, 0.2, 0.8],
        'EXTENSION':
        {
            'csv': '.csv',
            'json': '.json',
            'excel': '.xlsx',
            'txt': '.txt',
            'meta': '.meta',
            'png': '.png',
            'mp4': '.mp4'
        },
        'AXIS': ['pitch', 'yaw', 'roll', 'surge', 'heave', 'sway']
    }

    ###########################################################################
    #                                   3DI                                   #
    ###########################################################################
    THREEDI = \
    {
        'scenarios':
        {
            '3DI': 2636
        },
        'motion':
        {
            'extension': '.csv',
            'sensored': {
                'pitch': 'SensorPitch',
                # 'yaw': 'SensorYaw',
                'roll': 'SensorRoll'},
            'sampling_rate': None # not uniform
        },
        'video':
        {
            'extension': '.png',
            'resolution':
            {
                'width': 352,
                'height': 240
            },
            'fps': 25,
            'time': 105.40 # 1m 45.40 sec
        },
        'time':
        {
            'sampling': 'non_uniform',
            'time_column': 'Time',
            'start_index': 1,
            'end_index': 2636,
            'step_min': 0.30,
            'step_max': 0.36
        }
    }

    ###########################################################################
    #                                 UOS2018                                 #
    ###########################################################################
    UOS2018 = \
    {
        'scenarios':
        {
            'S1_pitch':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                        'pitch'
                    ],
                    'time': 20,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 20,
                    'fps': 60
                }
            },
            'S1_yaw':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                        'yaw'
                    ],
                    'time': 20,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 20,
                    'fps': 60
                }
            },
            'S1_roll':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                        'roll'
                    ],
                    'time': 20,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 20,
                    'fps': 60
                }
            },
            'S1_surge':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                    ],
                    'time': 20,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 20,
                    'fps': 60
                }
            },
            'S1_heave':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                        'heave'
                    ],
                    'time': 10,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 10,
                    'fps': 60
                },
            },
            'S1_sway':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                    ],
                    'time': 20,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 20,
                    'fps': 60
                }
            },
            'S2_pitch':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                        'pitch'
                    ],
                    'time': 20,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 20,
                    'fps': 60
                },
            },
            'S2_yaw':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                        'yaw'
                    ],
                    'time': 20,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 20,
                    'fps': 60
                }
            },
            'S2_roll':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                        'roll'
                    ],
                    'time': 20,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 20,
                    'fps': 60
                },
            },
            'S2_surge':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                    ],
                    'time': 20,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 20,
                    'fps': 60
                },
            },
            'S2_heave':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                        'heave'
                    ],
                    'time': 10,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 10,
                    'fps': 60
                },
            },
            'S2_sway':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                    ],
                    'time': 20,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 20,
                    'fps': 60
                },
            },
            'S3_pitch':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                        'pitch'
                    ],
                    'time': 20,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 20,
                    'fps': 60
                },
            },
            'S3_yaw':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                        'yaw'
                    ],
                    'time': 20,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 20,
                    'fps': 60
                },
            },
            'S3_roll':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                        'roll'
                    ],
                    'time': 20,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 20,
                    'fps': 60
                },
            },
            'S3_surge':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                    ],
                    'time': 20,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 20,
                    'fps': 60
                },
            },
            'S3_heave':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                        'heave'
                    ],
                    'time': 10,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 10,
                    'fps': 60
                },
            },
            'S3_sway':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                    ],
                    'time': 20,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 20,
                    'fps': 60
                },
            },
            'S4':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                        'pitch, surge'
                    ],
                    'time': 60,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 60,
                    'fps': 60
                },
            },
            'S5':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                        'yaw', 'roll', 'surge'
                    ],
                    'time': 60,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 60,
                    'fps': 60
                },
            },
            'S6':
            {
                'motion':
                {
                    'extension': '.txt',
                    'sensored':
                    [
                        'pitch', 'yaw', 'roll', 'surge'
                    ],
                    'time': 60,
                    'sampling_rate': 3 #hz
                },
                'video':
                {
                    'extension': '.mp4',
                    'resolution':
                    {
                        'width': 1024,
                        'height': 768
                    },
                    'time': 60,
                    'fps': 60
                },
            },
        }
    }
