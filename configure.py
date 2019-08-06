class Config:
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

    DEFAULT = \
    {
        'scenarios':
        {
            'S1_pitch': 1200,
            'S1_yaw': 1200,
            'S1_roll': 1200,
            'S1_surge': 1200,
            'S1_heave': 600,
            'S1_sway': 1200,
            'S2_pitch': 1200,
            'S2_yaw': 1200,
            'S2_roll': 1200,
            'S2_surge': 1200,
            'S2_heave': 600,
            'S2_sway': 1200,
            'S3_pitch': 1200,
            'S3_yaw': 1200,
            'S3_roll': 1200,
            'S3_surge': 1200,
            'S3_heave': 600,
            'S3_sway': 1200,
            'S4': 3600,
            'S5': 3600,
            'S6': 3600
        },
        'motion':
        {
            'extension': '.txt',
            'sensored':
            {
                'pitch': 'pitch',
                'yaw': 'yaw',
                'roll': 'roll',
                'heave': 'heave'
            },
            'sampling_rate': 3 # hz
        },
        'video':
        {
            'extension': '.mp4',
            'resolution':
            {
                'width': 1024,
                'height': 768
            },
            'fps': 25,
            'time': 105.40 # 1m 45.40 sec

        }
    }
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
