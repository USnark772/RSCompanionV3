import zipfile
import tempfile

temp_folder_name = "C:/Users/phill/Companion App Save Folder/test_name/"
x = tempfile.TemporaryDirectory(dir=tempfile.tempdir)
print(x.name)
#
# foldername = "C:/Users/phill/Companion App Save Folder/testZip1.rs"
# filename = "testoutput1.csv"
# text = "Hello World!"
# x = zipfile.ZipFile(foldername, "w")
# print(x)
# x.writestr(filename, text)
# x.close()
# a = zipfile.ZipFile(foldername, "a")
# print(a)
# a.writestr(filename, ", this is more text")
#
# x.close()
#
# y = zipfile.ZipFile(foldername, "r")
# z = zipfile.ZipFile(foldername, "r")
# outtext = y.read(filename)
# finaltext = outtext.decode("utf-8")
