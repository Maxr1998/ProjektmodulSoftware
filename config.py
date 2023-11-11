import pytz

TZ = pytz.timezone('Europe/Berlin')  # hardcoded because otherwise things would get ugly

USER_COUNT = 3

MOTOR_PINS = [
    [9, 11, 8, 7],
    [16, 19, 20, 21],
    [5, 6, 12, 13],
]

SENSOR_PINS = [4, 18, 17]

STEPS_PER_REVOLUTION = 512
