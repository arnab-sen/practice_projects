"""
* Initial version: a simple tool to check and log internet connectivity,
useful for monitoring the frequency of connection drops.
* Connectivity based on try/except with urllib.request
"""
import urllib.request, datetime, log_analysis
import time as TIME

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
    date = get_time(date_only = True)
    with open("log.txt", "a") as log:
        log.write(entry + "\n")

    # Complete a log analysis
    log_analysis.get_disconnects()

def run_monitor(wait_seconds):
    url = "https://google.com"
    while 1:
        try:
            with urllib.request.urlopen(url) as response:
                packet = response.read(1)
                
            time = get_time()
            entry = time + "\t" + "OK"
            print(entry)
            write_to_log(entry)
        except:
            time = get_time()
            entry = time + "\t" + "DISCONNECTED"
            print(entry)
            write_to_log(entry)

        TIME.sleep(wait_seconds)

def main():
    run_monitor(10)

if __name__ == "__main__":
    main()
