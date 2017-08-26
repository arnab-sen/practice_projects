"""
* Initial version: a simple tool to check and log internet connectivity,
useful for monitoring the frequency of connection drops.
* Connectivity based on try/except with urllib.request
"""
import urllib.request, urllib.error, datetime, log_analysis
import time as TIME
import win32api, winsound

CONNECTED = [True, True]

def get_time(date_only = None):
    date_and_time = str(datetime.datetime.now())
    date = date_and_time[:11]
    time = date_and_time[11:]
    rest = time[time.find(":") : time.rfind(".")]
    hour = time[:time.find(":")]

    if date_only:
        return date
    else:
        return date + "-- " + hour + rest

def change_hour(hour, timezone_offset):
    hour = int(hour)
    hour = (hour + timezone_offset) % 24
    hour = str(hour)

    if len(hour) < 2:
        hour = "0" + hour

    return hour

def write_to_log(entry):
    return
    date = get_time(date_only = True)
    with open("log.txt", "a") as log:
        log.write(entry + "\n")

    # Complete a log analysis
    log_analysis.get_disconnects()

def beep(short = True):
    if short:
        for i in range(3):
            winsound.Beep(1000, 300)
    else:
        winsound.Beep(1000, 850)    

def alert():
    """
    Sounds a beep and creates an alert messagebox if the
    connection is now active after being disconnected
    """
    messages = {
                (False, True) : "Reconnected!",
                (True, False) : "Disconnected!"
                }
    
    if ALERTS:
        if CONNECTED in ([False, True], [True, False]):
            beep()
            win32api.MessageBox(0, messages[tuple(CONNECTED)], "")

    CONNECTED[0] = CONNECTED[1]
    
def run_monitor(wait_seconds, alerts):
    url = "https://google.com"
    
    try:
        with urllib.request.urlopen(url, timeout = 10) as response:
            packet = response.read(1)
        CONNECTED[1] = True
        time = get_time()
        entry = time + "\t" + "OK"
        print(entry)
        write_to_log(entry)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        CONNECTED[1] = False
        time = get_time()
        entry = time + "\t" + "DISCONNECTED"
        print(entry)
        write_to_log(entry)
    
    except Exception as e:
        print("Error:", e)        
    finally:
        alert()
        TIME.sleep(wait_seconds)

def main():
    alerts = {True : "Alerts are ON", False : "Alerts are OFF"}
    global ALERTS
    ALERTS = True
    while 1:
        try:
            run_monitor(3, alerts)
        except KeyboardInterrupt:
            ALERTS = not ALERTS
            print(alerts[ALERTS])
        

if __name__ == "__main__":
    main()
