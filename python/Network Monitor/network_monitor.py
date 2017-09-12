"""
* Initial version: a simple tool to check and log internet connectivity,
useful for monitoring the frequency of connection drops.
* Connectivity based on try/except with urllib.request
"""
import urllib.request, urllib.error, datetime, log_analysis
import time as TIME
import win32api, winsound

CONNECTED = [True, True]
CURRENT_TIME = None
LAST_DISCONNECT_TIME = None

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

def beep(mode):
    if mode == "Disconnected!":
        winsound.Beep(1000, 300)
        winsound.Beep(750, 400)
    elif mode == "Reconnected!":
        winsound.Beep(750, 300)
        winsound.Beep(1000, 400)
    else:
        winsound.Beep(1000, 300)

def alert():
    """
    Sounds a beep and creates an alert messagebox if the current
    connection state is different from the previous one
    """
    messages = {
                (False, True) : "Reconnected!",
                (True, False) : "Disconnected!"
                }
    
    if ALERT_MODE in (0, 1):
        if CONNECTED in ([False, True], [True, False]):
            message = messages[tuple(CONNECTED)]
            beep(message)
            if ALERT_MODE == 0:
                win32api.MessageBox(0, message, "")

    CONNECTED[0] = CONNECTED[1]

def time_to_seconds(time):
    """ Converts a string time of form HH:MM:SS into int seconds
    """
    time = time.split(" -- ")
    time = time[-1]
    time = time.split(":")
    time = [int(i) for i in time]

    return time[0] * 3600 + time[1] * 60 + time[2]

def segment_num(val, sep):
    return val // sep, val % sep

def get_uptime(start, stop, pref = " -- Uptime: "):
    uptime = time_to_seconds(stop) - time_to_seconds(start)
    time = uptime
    hours, time = segment_num(time, 3600)
    minutes, time = segment_num(time, 60)
    seconds, time = segment_num(time, 1)

    return pref + "{}h {}m {}s".format(hours, minutes, seconds)
    
def run_monitor(wait_seconds):
    url = "https://google.com"
    global CURRENT_TIME, LAST_DISCONNECT_TIME
    
    try:
        with urllib.request.urlopen(url, timeout = 10) as response:
            packet = response.read(1)
        CONNECTED[1] = True
        CURRENT_TIME = get_time()
        if not LAST_DISCONNECT_TIME or CONNECTED == [False, True]:
            LAST_DISCONNECT_TIME = CURRENT_TIME
        entry = CURRENT_TIME + "\t" + "OK" + \
                get_uptime(LAST_DISCONNECT_TIME, CURRENT_TIME)
        print(entry)
        write_to_log(entry)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        CONNECTED[1] = False
        CURRENT_TIME = get_time()
        if CONNECTED == [True, False]:
            LAST_DISCONNECT_TIME = CURRENT_TIME
        entry = CURRENT_TIME + "\t" + "DISCONNECTED" + \
                get_uptime(LAST_DISCONNECT_TIME, CURRENT_TIME, pref = " -- Downtime: ")
        print(entry)
        write_to_log(entry)
    except Exception as e:
        print("Error:", e)        
    finally:
        alert()
        TIME.sleep(wait_seconds)

def main():
    global ALERT_MODE
    ALERT_MODE = 1
    alert_message = "\nMode {}/3 - Alert Messages {}, Sound {}"
    alert_params = {
                        0 : (1, "ON", "ON"),
                        1 : (2, "OFF", "ON"),
                        2 : (3, "OFF", "OFF")
                        }
    print("Current mode:" + alert_message.format(*alert_params[ALERT_MODE]))
    
    while 1:
        try:
            run_monitor(3)
        except KeyboardInterrupt:
            ALERT_MODE = (ALERT_MODE + 1) % 3
            print(alert_message.format(*alert_params[ALERT_MODE]))        

if __name__ == "__main__":
    main()
