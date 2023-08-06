#import generator.base_generator
#from lib.data_analyser import DecodeSignal, DataAnalyser
import numpy as np
import numpy as np

WHITE_LIST=np.array([0x0,0x9100460]) # Keep 0x0 in WHITE_LIST!
SOURCE_SIGNAL_NAME = 'UDS_Signal_0x19020b'

def get_data():
        #times, values = self.get_signal_data_from_loader(SOURCE_SIGNAL_NAME)
        values=org_v=np.genfromtxt('out2.csv',delimiter=' ',dtype=np.int8)
        times=org_times=np.genfromtxt('out3.csv',delimiter=' ')


        VALUE_INDEX = 0x3
        HEADER_BYTE2 = 0x0
        START_POS2 = 0x1
        LENGTH2 = 0x0

        HEADER_BYTE = 0x10 if VALUE_INDEX == 0 else int(((VALUE_INDEX + 1) * 4) / 7) + 0x20
        START_POS = ((VALUE_INDEX + 1) * 4) % 7 + 1
        LENGTH = 3 if 8 - START_POS > 3 else 8 - START_POS

        if LENGTH < 3:
            LENGTH2 = 3 - LENGTH
            HEADER_BYTE2 = HEADER_BYTE + 1


        idxs = np.where(values[..., 0] == HEADER_BYTE)[0]
        if len(idxs)==0 or VALUE_INDEX < 0:
            values=np.array([],dtype=np.uint8)
            times=np.array([],dtype=np.uint64)
        else:
            # print(idxs)
            decoded_values1 = values[idxs][..., START_POS:(LENGTH + START_POS)]
            if HEADER_BYTE2!=0:
                idxs2 = np.where(values[..., 0] == HEADER_BYTE2)[0]
                decoded_values2 = values[idxs2][..., START_POS2:(LENGTH2 + START_POS2)]
                decoded_values = np.hstack((decoded_values1, decoded_values2))
                decoded_values = np.hstack([np.zeros(decoded_values.shape[0], dtype=np.uint8).reshape([decoded_values.shape[0], 1]),
                                            decoded_values.astype(np.uint8)])
            else:
                decoded_values = np.hstack([np.zeros(decoded_values1.shape[0], dtype=np.uint8).reshape([decoded_values1.shape[0], 1]),
                                            decoded_values1.astype(np.uint8)])

            values = np.frombuffer(decoded_values, np.uint32)
            values = values.byteswap()
            idx2 = np.where(np.isin(values, WHITE_LIST))
            times = times[idxs]
            values = np.delete(values, idx2)
            times = np.delete(times, idx2)
# print(times,decoded_values)
            return (times, values)

print(get_data())
