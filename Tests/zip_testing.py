import zipfile

foldername = "C:/Users/phill/Companion App Save Folder/testZip1.rs"
filename = "testoutput1.csv"
text = "Hello World!"
x = zipfile.ZipFile(foldername, "w")
print(x)
x.writestr(filename, text)

x.close()

y = zipfile.ZipFile(foldername, "r")
y.printdir()
outtext = y.read(filename)
print(type(outtext))
finaltext = outtext.decode("utf-8")
print(type(finaltext))
print(finaltext)
