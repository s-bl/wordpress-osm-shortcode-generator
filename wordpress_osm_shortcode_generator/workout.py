from constants import workout_mappings

class Workout:

    def __init__(self, *, workout, path):
        self.workout = workout
        self.workout_type = self.workout.tracks[0].type.lower()
        self.workout_type = workout_mappings[self.workout_type] if self.workout_type in workout_mappings else self.workout_type
        self.path = path

        self.length_2d = self.workout.length_2d()
        self.length_3d = self.workout.length_3d()
        self.duration = self.workout.get_duration()

        fst_point = self.workout.tracks[0].segments[0].points[0]

        self.time = fst_point.time
        self.longitude = fst_point.longitude
        self.latiude = fst_point.latitude

    def __getstate__(self):
        exclude = ['workout']
        state = {key: value for key, value in self.__dict__.items() if key not in exclude}

        return state
