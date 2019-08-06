class DataManagerDefalut(DataManager):
    def __init__(self, *args, **kwargs):
        super(DataManager3DI, self).__init__(*args, **kwargs)
        self._scenarios   = kwargs.get('scenarios')
        self._sensored    = kwargs.get('sensored')
        self._unsensored  = [axis for axis in self._axis if axis not in self._sensored.keys()]

    def from_config(cls, conf):
        return cls(motion_load_dir      = conf.PREPROCESS_MOTION['LOAD_DIR'],
                   motion_save_dir      = conf.PREPROCESS_MOTION['SAVE_DIR'],
                   bin_seperator = conf.PREPROCESS_MOTION['BIN_SEPERATOR'],
                   extension     = conf.EXTENSION,
                   axis          = conf.AXIS,
                   scenarios     = conf.THREEDI['scenarios'].keys(),
                   sensored      = conf.THREEDI['motion']['sensored'])

    def _load(self):
        """load files from directory

        Args:
           directory (str) directory to load (default LOAD_DIR: ./data/raw/motion)

        Returns:
           {(str): [[arr]]} all data in directory of format txt-files about sampled at 3hz
        """

        ret = {}
        for scenario in self._scenarios:
            _file = self._motion_load_dir + scenario + self._extension['txt']
            _raw_data = np.genfromtxt(codecs.open(_file, encoding='UTF8').
                                      readline().replace(u'\ufeff', '').split(' ')[:-1], dtype='i4')
            ret[_file_name] = _raw_data.reshape((int)(_raw_data.size / RAW_DATA_FRAME_SIZE),
                                                RAW_DATA_FRAME_SIZE)
        return ret

class PreprocessorDefault(Preprocessor):
    def __init__(self,
                 bin_magnitude = BIN_MAGNITUDE,
                 bin_degree = BIN_DEGREE,
                 roi = np.index_exp[:, :],
                 resolution = (1024, 768))
        super(PreprocessorDefault, self).__init__(bin_magnitude, bin_degree, roi, resolution)
        pass

    def set_video_src(self, video_src):
        self._video_src = cv2.VideoCapture(video_src)

    def set_motion_src(self, motion_src):
        self._motion_src = motion_src

    def get_preprocessed_data(self):
        self._make_video_histogram()
        self._make_motion_histogram()
        yield self._mapping_motion_to_histogram(), self._mapping_video_to_histogram()

    def _classification_video(self):
        prevgray  = cv2.cvtColor(self._video_src.read()[1][self._roi], cv2.COLOR_BGR2GRAY)
        frame_max = self._video_src.get(cv2.CAP_PROP_FRAME_COUNT)
        frame_num = 1
        while frame_num < frame_max:
            gray = cv2.cvtColor(cv2.cvtColor(frame[self._roi], cv2.COLOR_BGR2GRAY))
            if frame_num % 20 == 19:
                gray = cv2.cvtColor(frame[self._roi], cv2.COLOR_BGR2GRAY)
                flow = cv2.calcOpticalFlowFarneback(
                    prevgray, gray, None, 0.5, 4, 15, 3, 5, 1.2, 0)
                polars = cv2.cartToPolar(flow[0], flow[1], None, None, True)
                yield(np.array([Preprocessor._video_bin_selection(polar) for polar in polars]))
            if frame_num % 20 == 0:
                prevgray = cv2.cvtColor(frame[self._roi], cv2.COLOR_BGR2GRAY)
        self._video_src.release()

    def _make_video_histogram(self):
        for values in self._classification_video():
            for v in values:
                self._video_histogram[v] += 1

        self._video_histogram /= np.sum(self._video_histogram)

    def _mapping_video_to_histogram(self):
        for values in self._classification_video():
            yield [self._video_histogram[v] for v in values]

    def _make_motion_histogram(self):
        """ make lookup table in file(scanning) which check probability of a motion vector of a
         frame up to all frames to decide the motion vector is how many occured in the experiment

        Args:
        motion_vectors (arr;2d) data for make lookup table

        Returns:
        tuple([arr], [float]) lookup-table to decide probability of a motion vector
        """

        u = np.unique(self._motion_src, axis=0, return_counts=True)
        self._motion_histogram = (ret[0], ret[1] / ret[1].sum())

    def _mapping_motion_to_histogram(self):
        """ decide probabiltiy of a motion vectors

        Args:
        motion_vectors (arr; 2d)

        Returns:
        tuple([arr], [float]) the probabiltiy of a motion vectors in frames
        """
        for motion_vector in self._motion_src:
            motion_vector[3] = 0 # surge
            motion_vector[5] = 0 # sway

        self._make_motion_histogram()
        for motion_vector in self._motion_src:
            for i in range(len(self._motion_histogram[0])):
                if np.array_equal(motion_vector, self._motion_histogram[0][i]):
                    yield motion_vector, motion_histogram[1][i]
