import binascii
import os


elements_per_line = 16
bytes_per_element = 8
chars_per_element = bytes_per_element * 2
#unit is element NOT byte
null_padding_length = 131072
append_name = "in.bin"
out_name = "out.txt"

out_buffer = ""
append_buffer = ""
in_buffer = ""

arr_type = ""
if(bytes_per_element == 1):
    arr_type = "unsigned char"
elif(bytes_per_element == 2):
    arr_type = "unsigned short"
elif(bytes_per_element == 4):
    arr_type = "unsigned int"
elif(bytes_per_element == 8):
    arr_type = "unsigned __int64"

append_buffer += arr_type + " PAYLOAD[] = "
append_buffer += "{"
dir_items = os.listdir()
for v in dir_items:
    if(v.find(".exe") != -1):
        append_name = v


with open(append_name, "rb") as app_f:
    in_buffer = app_f.read()


#make sure the buffer is full
if(len(in_buffer) % bytes_per_element != 0):
    in_buffer += b"\x00" * (bytes_per_element - len(in_buffer) % bytes_per_element)


#should be bytes_per_element in length
def reverse_endianness(bytes_arr : bytes):
    #reverse endianness
    bytes_block = bytearray([0] * 8)

    for j in range(bytes_per_element):
        bytes_block[j] = bytes_arr[bytes_per_element - j - 1]
    return bytes_block

def get_formatted_element(bytes_block : bytes):
    return "0x" + bytes.decode(binascii.hexlify(bytes_block)) + ","

#index that handles the indentation
g_index = 0

elements_len = int(len(in_buffer) / bytes_per_element)


#element at end may require padding
for i in range(elements_len - 1):
    if(g_index % elements_per_line == 0):
        append_buffer += "\n"
    start_index = i * bytes_per_element
    bytes_arr = in_buffer[start_index:start_index + bytes_per_element]
    
    append_buffer += get_formatted_element(reverse_endianness(bytes_arr))
    g_index += 1



EMPTY_ELEMENT = get_formatted_element(b"\x00" * bytes_per_element)
for i in range(null_padding_length):
    if(g_index % elements_per_line == 0):
        append_buffer += "\n"
    append_buffer += EMPTY_ELEMENT
    g_index += 1





append_buffer += "\n};"
out_buffer += append_buffer
with open(out_name,"w") as out:
    out.write(out_buffer)
