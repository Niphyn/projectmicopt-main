import struct

company = b"Gabriela"
day, month, year = 22, 4, 2021
v = True

print(struct.calcsize("i")) #tamamho de um inteiro

byte_stream = struct.pack("8s3i?", company, day, month, year, v)

name, day, month, year, v = struct.unpack("8s 3i ?", byte_stream)
print("name: ", name.decode("ascii"))
print("day: ", day)
print("month: ", month)
print("year: ", year)
print("v: ", v)

#testando string

string = "Gabriela tem "+str(21)+" anos e "+str(-50)
print(string)