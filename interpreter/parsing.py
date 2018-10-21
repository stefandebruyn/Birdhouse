import os
import re
import datetime
import time
import platform


# Db file locations
MODULE_PATH = os.path.abspath(__file__)
CWD = MODULE_PATH[0:MODULE_PATH.rfind("\\parsing.py" if platform.system() == "Windows" else "/parsing.py")]
FLAG_DB_DIR = CWD + "/flags/"
FLAG_SOURCES = ["price", "negation", "proximity"]
CITY_DB_SRC = "/data/us_cities.txt"
STATE_DB_SRC = "/data/us_states.txt"
NUMBER_DB_SRC = "/data/numbers.txt"


# Compile-time db collections to be filled
flag_db = {}
city_db = []
state_db = []
numbers_db = []
ts = time.time()


# Timestamps some telemetry and prints it
def tlm(data):
    timestamp = "[" + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') + "]"
    print(timestamp, data)


# Loads the flags into the flag map
def load_flags():
    tlm("Loading flagsets")

    for src in FLAG_SOURCES:
        flag_db[src] = []
        src_file = open(FLAG_DB_DIR + src)
        flags = [line.strip() for line in src_file.readlines()]

        for flag in flags:
            flag_db[src].append(flag)

    tlm("Finished loading " + str(len(flag_db.keys())) + " flagsets")


# src_path_end is appended to the cwd and the file at that location is emptied into db
def load_db(src_path_end, db):
    tlm("Loading " + src_path_end)

    with open(CWD + src_path_end, "r") as inp:
        for line in inp:
            db.append(line.strip())

    tlm("Finished loading" + str(len(db)) + "entries from" + src_path_end)


# Binary search for a value in a sorted database
def bin_search(db, item):
    lower = 0
    upper = len(db)

    while upper - lower > 1:
        mid = int(lower + (upper - lower) / 2)
        comp = db[mid].lower()

        if comp == item:
            return True
        else:
            if comp < item:
                lower = mid
            else:
                upper = mid

    return False


# Converts a number in English form into an int.
# Pulled from https://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers
def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current


# Parse a string of English text. Should be the transcribed string returned by Rev's API
def parse(src):
    tlm("Parser: running")

    # Process the text a bit
    words = re.split("[^A-Za-z]", src.strip().lower())
    words = list(filter(None, words))

    criteria = []
    in_negation = False
    pos = 0

    # Loop through the words and look for criteria
    while pos < len(words):
        word = words[pos]

        # User said a negation keyword
        if word in flag_db["negation"]:
            tlm("Parser: found negation flag")

            in_negation = True

        # User said something about a location
        if word in flag_db["proximity"]:
            tlm("Parser: found proximity flag")

            # Look for cities
            look_ahead = 1
            # Most cities are no more than 3 words
            max_city_length = 3
            city_name_pieces = words[pos+look_ahead:pos+look_ahead+max_city_length]
            city_compiled = None
            city_compiled_reach = 0

            for reach in range(1, len(city_name_pieces) + 1):
                compiled = " ".join(city_name_pieces[0:reach])
                if bin_search(city_db, compiled):
                    city_compiled = compiled
                    city_compiled_reach = reach

            # City was found
            if city_compiled is not None:
                crit = ("city", city_compiled, in_negation)
                criteria.append(crit)

            # Look for state
            state_potential_start = pos + look_ahead + city_compiled_reach - 1
            one_word_state = "not a state"
            two_word_state = "not a state"
            try:
                one_word_state = words[state_potential_start + 1]
            except Exception:
                pass
            try:
                two_word_state = words[state_potential_start + 1] + " " + words[state_potential_start + 2]
            except Exception:
                pass
            compiled_state = None

            # If one of the strings exists in the state database, make a note
            if bin_search(state_db, one_word_state):
                compiled_state = one_word_state
            if bin_search(state_db, two_word_state):
                compiled_state = two_word_state

            # Add a new criterion if the state was recognized
            if compiled_state is not None:
                crit = ("state", compiled_state, in_negation)
                criteria.append(crit)

            # Reset negation
            in_negation = False

        # User said something about price
        if word in flag_db["price"]:
            tlm("Parser: found price flag")

            look_ahead = 1
            number_words = []
            look_pos = pos + look_ahead

            # Look ahead and assemble a sequence of words denoting numbers
            while look_pos < len(words) and words[look_pos] in numbers_db:
                number_words.append(words[look_pos])
                look_pos += 1

            # If a sequence was found, convert the words to a number and add a price criterion
            if len(number_words) > 0:
                price = text2int(" ".join(number_words))
                crit = ("price", price, in_negation)
                criteria.append(crit)

        # Move on to the next word
        pos += 1

    tlm("Parser: done")

    return criteria


# Build the databases
load_db(CITY_DB_SRC, city_db)
load_db(STATE_DB_SRC, state_db)
load_db(NUMBER_DB_SRC, numbers_db)
load_flags()
v                                                              