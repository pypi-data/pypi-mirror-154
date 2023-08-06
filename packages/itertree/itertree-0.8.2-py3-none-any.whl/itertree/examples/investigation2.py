#import generator.base_generator
#from lib.data_analyser import DecodeSignal, DataAnalyser
import numpy as np


#times, values = self.get_signal_data_from_loader(SOURCE_SIGNAL_NAME)
values=org_v=np.genfromtxt('out_values.csv',delimiter=' ',dtype=np.int8)
times=org_times=np.genfromtxt('out_times.csv',delimiter=' ')

WHITE_LIST = np.array([0x0, 0x9100460])  # Keep 0x0 in WHITE_LIST!
SOURCE_SIGNAL_NAME = 'UDS_Signal_0x19020b'

start_idxs = np.where(values[..., 0] == 0x10)[0]
times = times[start_idxs]
number_of_rows = len(start_idxs)
# delete zeros
del_idxs = np.where(values[..., 0] == 0)[0]
values = np.delete(values, del_idxs, axis=0)
m_idxs = np.where(values[..., 0] == 0x10)[0]
result = []
end = number_of_rows - 1
max_l = 0
for i, idx in enumerate(m_idxs):
    # iter over all valid rows
    # create row wise array
    if i == end:
        items = values[idx:]
    else:
        items = values[idx:m_idxs[(i + 1)]]
    l = items.shape[0] * items.shape[1]
    items = items.reshape(l)
    # delete leading bytes
    del_idxs = np.array(range(0, l, 8))
    items = np.delete(items, del_idxs)
    # cut first 3 bytes and append last 4
    items = items[3:]
    l = len(items)
    m = l % 4
    if m!=0:
        items = items[:-m]
    # calc zero indexes to extend to mask the upper byte
    zero_idxs = np.array(range(0, l, 4))
    items[zero_idxs[:-1]] = 0
    # convert to unit32 and swap bytes
    v = np.frombuffer(items.astype(np.uint8), dtype=np.uint32)
    v = v.byteswap()
    # clean entries from WHITE_LIST
    del_idxs = np.where(np.isin(v, WHITE_LIST))[0]
    v = np.delete(v, del_idxs)
    # adapt array length of pre entries with zeros if required
    l = len(v)
    if max_l < l:
        diff = l - max_l
        for v2 in result:
            v2 = np.hstack([v2, np.zeros(diff, dtype=np.uint32)])
        max_l = l
    result.append(v)
if len(result) > 0:
    # reshape to target shape
    result = np.array(result).reshape(len(result), max_l)
    # delete zero entries
    del_idxs = np.where(result[..., 0] == 0)[0]
    if len(del_idxs) > 0:
        values = np.delete(result, del_idxs)
        times = np.delete(times, del_idxs)
    else:
        values = result
# print(times,decoded_values)
#return (times, values)
print(times,values)
