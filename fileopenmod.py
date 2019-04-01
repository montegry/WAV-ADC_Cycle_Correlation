import struct
import os


def file_open(file_name):
    """file_open function - read header of the file returns I,Q buffer and string with file info"""
    ext = os.path.splitext(file_name)[1]
    info_string = "No info"
    buff_out = []
    with open(file_name, 'rb') as for_read:
        if ext == '.adc':
            # ADC HEADER READER
            dt = struct.unpack('=d', for_read.read(8))[0]
            dsp = struct.unpack('l', for_read.read(4))[0]
            block_count = struct.unpack('l', for_read.read(4))[0]
            flag1 = struct.unpack('l', for_read.read(4))[0]
            datatype = struct.unpack('l', for_read.read(4))[0]
            info = for_read.read(8)
            # ADC HEADER READER
            info_string = 'File:{0}; DT:{1}; DSP:{2}; Number of blocks:{3}; INFO:{4}'.format(os.path.split(file_name)[1]
                                                                                             , dt, dsp, block_count,
                                                                                             info)

        elif ext == '.wav':
            # WAV HEADER READER
            chunckId = for_read.read(4)
            chunckSize = struct.unpack('l', for_read.read(4))[0]
            format = for_read.read(4)
            sub_chunk = for_read.read(4)
            sub_chunk_1 = struct.unpack('l', for_read.read(4))[0]
            audio_format = struct.unpack('h', for_read.read(2))[0]
            num_channels = struct.unpack('h', for_read.read(2))[0]
            dt = 1 / (struct.unpack('l', for_read.read(4))[0])
            byte_rate = struct.unpack('l', for_read.read(4))[0]
            block_align = struct.unpack('h', for_read.read(2))[0]
            bit_per_sec = struct.unpack('h', for_read.read(2))[0]
            sub_chunk_2 = for_read.read(4)
            sub_chunk_2_size = struct.unpack('l', for_read.read(4))[0]
            datatype = 2
            block_count = int(sub_chunk_2_size / 4)
            # print("DT:", dt)
            # WAV HEADER READER

        # DATATYPE BEGIN
        if datatype == 3:
            set_type = ['f', 4]
        else:
            set_type = ['h', 2]
        # DATATYPE END

        for block in range(block_count):
            try:
                buff_out.append(float(struct.unpack(set_type[0], for_read.read(set_type[1]))[0]))
            except Exception as e:
                print("ERROR in file openmod:%s".format(e))

        # for i in range(10):
            
        return buff_out, info_string


def file_counter(file_name):
    ext = os.path.splitext(file_name)[1]
    size = os.path.getsize(file_name)
    if ext == ".wav":
        return size - 44
    elif ext == ".adc":
        return size - 32


if __name__ == "__main__":
    print("file_open function - read header of the file returns I,Q buffer and string with file info")
    print("Supported file types: ADC, WAV")
    file_name = input("To test enter file path:")
    file_open(file_name)
