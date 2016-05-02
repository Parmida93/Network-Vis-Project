__author__ = 'ghahr'
import os

def read_traces():
    path = './Results/Traces'
    dirs = os.listdir( path )
    for file in dirs:
        f = open((path + "/" + file), 'r')
        f2 = open("./Results/Object Number Through Time/" + file, 'w')
        counter = 0
        str1 = ''
        if 'QUIC' in file:
            str2 = 'QUIC'
        else:
            str2 = 'HTTPS'
        print file
        for line in f:
            splitted = line.split(" ")
            if ('QUIC' in file and splitted[4] == 'UDP') or ('HTTPS' in file and splitted[4] == 'TCP'):
                counter += 1
                if counter != 1 and counter != 0 and ((counter & (counter - 1)) == 0):
                    str1 += " {0}".format(counter)
                    str2 += " {0}".format(splitted[1])
        out_str = "{0}\n{1}".format(str1.strip(), str2)
        print out_str
        f2.write(out_str)

        f.close()
        f2.close()

def test():
    f2 = open("./Results/Object Number Through Time/Video1_HTTPS.txt", 'r')
    print f2.readline()
    print f2.readline()
    f2.close()

if __name__ == "__main__":
    read_traces()
    # test()