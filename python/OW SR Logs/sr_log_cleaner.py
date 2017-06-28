"""
* This creates a dictionary of SR changes, where each entry pertains to a
  unique day
* Win/loss, SR change, and games played summaries are created, along with
  averages of SR gain/loss
"""

def get_log_dict(path = "", filename = "sr_log.txt"):
    """Returns a dict of lists where element d[key_n][0] is the starting SR,
    and the rest of d[key_n][2:m] are the SR entries with times
    """
    with open(path + filename, 'r') as file:
        raw_list = file.read().split("\n")

    for i, line in enumerate(raw_list):
        if line == "":
            raw_list.pop(i)

    log_dict = {}

    key = raw_list[0]
    #print(key.split())

    for line in raw_list[1:]:
        if "---" in line:
            key = line
        else:
            if key in log_dict:
                log_dict[key].append(line)
            else:
                log_dict[key] = [line]

    #print(raw_list)
    for key, val in log_dict.items():
        print(key, val, "", sep = "\n")
        #pass

def main():
    #get_log_dict(filename = "season 4.txt")
    get_log_dict()

if __name__ == "__main__":
    main()
