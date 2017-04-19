import rumps

import start
import stop

class Track(rumps.App):
    def __init__(self):
        super(Track, self).__init__("Track", None, 'data/icon.png')
        self.menu = ["Start", "Stop"]

    @rumps.clicked("Start")
    def start_tracking(self, _):
        start.main()    

    @rumps.clicked("Stop")
    def stop_tracking(self, _):
        stop.main()

if __name__ == "__main__":
    Track().run()