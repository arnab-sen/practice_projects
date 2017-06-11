"""
Checks for and makes a log of all disconnects in the larger log file
"""

def get_disconnects(print_results = None):
    disconnects = []
    with open("log.txt") as log:
        entries = log.read().split("\n")

    for entry in entries:
        if "DISCONNECT" in entry:
            disconnects.append(entry)

    if print_results:
        for disc in disconnects:
            print(disc)

    log_disconnects(disconnects)

def log_disconnects(disconnects):
    with open("disconnects.txt", "w") as log:
        for disconnect in disconnects:
            log.write(disconnect + "\n")

if __name__ == "__main__":
    get_disconnects(print_results = True)

        
