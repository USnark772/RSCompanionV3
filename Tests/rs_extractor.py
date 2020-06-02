import zipfile

zip_filename = "C:/Users/phill/Companion App Save Folder/test.rs"
output_folder = zip_filename[:zip_filename.rfind("/")]

zipper2 = zipfile.ZipFile(zip_filename, "r")
zipper2.extractall(output_folder)
