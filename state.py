from enum import Enum


class State(Enum):
    ASK_STEP_INITIAL = 0
    ASK_STEP_LOOP = 1
    ASK_ETA = 2
    TRACKING = 3
    COMPLETE = 4

