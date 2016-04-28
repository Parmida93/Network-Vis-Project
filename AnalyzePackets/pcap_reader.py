from pcapfile import savefile
from pcapfile.protocols.linklayer import ethernet
from pcapfile.protocols.network import ip
import binascii


# Just name of the file, WITHOUT .pcap extension
# This file should be in "Samples" folder which is in the same folder as pcap_reader.py file
# Results will be in "traces" folder which is in the same folder as pcap_reader.py file
def my_pcap_reader(filename):
    testcap = open('../Samples/' + filename + ".pcap", 'rb')
    capfile = savefile.load_savefile(testcap, verbose=True)
    f = open('Results/Traces/' + filename + ".txt", 'w')

    # eth_frame = ethernet.Ethernet(capfile.packets[0].raw())
    # print eth_frame

    # ip_packet = ip.IP(binascii.unhexlify(eth_frame.payload))
    # print ip_packet

    for i in range(len(capfile.packets)):
        eth_frame = ethernet.Ethernet(capfile.packets[i].raw())
        try:
            ip_packet = ip.IP(binascii.unhexlify(eth_frame.payload))
        except Exception as e:
            print e.message
            continue

        packet = capfile.packets[i]

        packet_type = ""
        if ip_packet.p == 6:
            packet_type = "TCP"
        elif ip_packet.p == 17:
            packet_type = "UDP"
        else:
            packet_type = "Unknown_type"

        milisecond = str(packet.timestamp_ms)
        while len(milisecond) < 6:
            milisecond = "0" + milisecond
        t1 = float(str(packet.timestamp%100000) + "." + milisecond)
        t2 = float(str(capfile.packets[0].timestamp%100000) + "." + str(capfile.packets[0].timestamp_ms))
        t3 = t1 - t2
        t3 = "{0:.6f}".format(t3)

        row = str(i+1)+ " " + str(t3) + " " + ip_packet.src + " " + ip_packet.dst + " " + packet_type + " " + str(packet.packet_len)
        print(row)
        f.write(row + "\n")
        print("------------------------------------------------")
    f.close()
