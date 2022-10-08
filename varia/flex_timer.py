import pathlib
from threading import Timer
from time import sleep
from functools import partial
from black import format_str, FileMode
from pathlib import Path

""" This is a helper tool which just formats the source code with black every N seconds.
    It was an interesting experiment. However, retrospectively it's unnecessary 
    complicated. I'd rather use a pre-commit hook or something like that. 
"""
class RepeatedTimer:
    def __init__(self, *args, **kwargs):  # Autostarts

        for key, value in kwargs.items():
            print(f"{key}, {value}")
            if key == "function":
                self.function = value
            if key == "interval_seconds":
                self.interval = value

        self._timer = None
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def main():
    def format(placeholder, **kwargs):
        """Determines the function that will actually run every N seconds"""
        project_dir = Path("/home/cyrill/panopto-puller/")
        all_directories = [f.resolve() for f in project_dir.rglob("*.py")]
        for py in all_directories:
            format_this_file = str(py.resolve())
            print(format_this_file)
            with open(format_this_file, "r+") as f:
                source_code = f.read()
                formatted_code = format_str(source_code, mode=FileMode())
                print(f"I'm {placeholder} the following file://{format_this_file}")
                f.seek(0)
                f.write(formatted_code)
                f.truncate()

    # Config:
    kwargs = {
        "interval_seconds": 2,
        "function": format,
    }
    args = {"formatting"}

    print("starting...")
    rt = RepeatedTimer(*args, **kwargs)
    lifetime = 3600
    # Run till finito
    try:
        sleep(lifetime)  # your long-running job goes here...
    finally:
        rt.stop()  # better in a try/finally block to make sure the program ends!
        print(f"Timer signing off after {lifetime}")


if __name__ == "__main__":
    main()
