from scapy.all import sniff, Scapy_Exception
import collaborator.utils.utils as utils
import threading


class NetworkTracker(threading.Thread):
    """docstring for NetworkTracker."""
    def __init__(self, path_to_record, update_rate=60, filter="tcp or udp"):
        threading.Thread.__init__(self)
        self.__path_to_record = path_to_record
        self.__update_rate = update_rate
        self.__filter = filter
        self.__alive = False
        self.__records = {}
        utils.clearFile(self.__path_to_record)
        utils.writeLine(self.__path_to_record, 'NETWORK TRACKER')

    def run(self):
        self.__alive = True
        while self.__alive:
            begin_time = utils.getTime()

            try:
                packets = sniff(timeout=self.__update_rate,
                                filter=self.__filter)
            except Scapy_Exception:
                break

            except PermissionError:
                break

            end_time = utils.getTime()

            result_sum = 0
            for packet in packets:
                result_sum += len(packet.payload)

            average = result_sum / len(packets)

            timestamp = str(begin_time) + "-" + str(end_time)
            print(str(timestamp) + " " + str(average))
            self.__records[timestamp] = [str(average), str(len(packets))]
        print("end")
        utils.saveRecords(self.__path_to_record, self.__records)

    def kill(self):
        self.__alive = False
