import binascii
import os


elements_per_line = 16
bytes_per_element = 4
chars_per_element = bytes_per_element * 2
append_name = "in.bin"
out_name = "out.txt"

out_buffer = ""
append_buffer = "\n{"
in_buffer = ""

dir_items = os.listdir()
for v in dir_items:
    if(v.find(".exe") != -1):
        append_name = v


with open(append_name, "rb") as app_f:
    in_buffer = app_f.read()

arr_str_unparsed = binascii.hexlify(in_buffer)



for i in range(int(len(arr_str_unparsed) / chars_per_element)):
    if(i % elements_per_line == 0):
        append_buffer += "\n"
    start_index = i * chars_per_element
    #reverse endianness
    bytes_block_raw = []
    for j in range(bytes_per_element):
        index = start_index + j * 2
        bytes_block_raw.append(bytes.decode(arr_str_unparsed[index:index + 2]))

    bytes_block = ""
    for j in range(bytes_per_element):
        bytes_block += bytes_block_raw[bytes_per_element - j - 1]
    append_buffer += "0x" + bytes_block + ","
    
 



append_buffer += "\n}"
out_buffer += append_buffer
with open(out_name,"w") as out:
    out.write(out_buffer)
