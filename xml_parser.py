def xml_parse(src_path):
    src = open(src_path, "r")
    lines = src.readlines()
    pos = 0
    regions = []

    while pos < len(lines):
        line = lines[pos].strip()

        if line == "<region>":
            data = []
            property = {}

            for i in range(6):
                if pos + 1 < len(lines):
                    data.append(lines.pop(pos+1).strip())

            try:
                for entry in data:
                    key = entry[entry.index("<")+1:entry.index(">")].split()[0]
                    value = entry[entry.index(">")+1:entry.rfind("<")]
                    property[key] = value
            except Exception:
                pass

            if property is not None:
                regions.append(property)

        pos += 1

    return regions[1:len(regions)]


#results = parse(os.getcwd() + "/zillow.xml")
#for r in results:
#    print(r)
