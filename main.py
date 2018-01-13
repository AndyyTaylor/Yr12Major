" Andy "
from src.framework.StateAppRunner import StateAppRunner

STATERUNNER = StateAppRunner.instance()

while not STATERUNNER.is_closed():
    STATERUNNER.run_loop()
