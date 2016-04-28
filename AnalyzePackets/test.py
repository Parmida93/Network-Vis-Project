from pcap_reader import my_pcap_reader

filename = "Video2_HTTPS"  # just name of the file, WITHOUT .pcap extension
# This file should be in "Samples" folder which is in the same folder as pcap_reader.py file
# Results will be in "traces" folder which is in the same folder as pcap_reader.py file
my_pcap_reader(filename)
