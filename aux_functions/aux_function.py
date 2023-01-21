def pkt_to_json(pkt):
    """
    Serializes a :param pkt: into easily accessible json format
    """
    json_packet = {}
    c_layer = None
    for line in pkt.split('\n'):
        if line.startswith("###["):
            c_layer = line.replace("###[", '').replace("]###", '').strip().lower()
        else:
            keyval = line.split("=")
            if len(keyval) == 2:
                if c_layer not in json_packet:
                    json_packet[c_layer] = {}
                json_packet[c_layer][keyval[0].strip()] = keyval[1].strip()
    return json_packet