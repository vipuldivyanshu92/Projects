class PacketReadError(Exception):
    def __str__(self):
        return "Unable to read the full packet"