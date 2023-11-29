from channel import Channel
import struct
class Data(object): 
    def __init__(self, data):
        self.header = self.__unpack_header(data[:20])
        #print(self.header)
        self.channel1 = Channel(data[20:])
        self.channel2 = Channel(data[20 + 20 + 2 * (self.channel1.sub_header['nPoints']):])
        self.channel3 = Channel(data[20 + 20 * 2 + 2 * (self.channel1.sub_header['nPoints'] + self.channel2.sub_header['nPoints']):])
        self.channel4 = Channel(data[20 + 20 * 3 + 2 * (self.channel1.sub_header['nPoints'] + self.channel2.sub_header['nPoints'] + self.channel3.sub_header['nPoints']):])
        

    def __unpack_header(self, header): 
        header_format = '<IIIII'
        (
            main_header_size,
            protocol_version,
            duts,
            reserved,
            counter,
            
        ) = struct.unpack(header_format, header)

        unpacked_header = {
            'Main header size': main_header_size,
            'Protocol version': protocol_version,
            'Number of DUTs': duts,
            'Reserved bytes':reserved,
            'Counter':counter,
        }
        return unpacked_header
