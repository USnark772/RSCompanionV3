import os
import zipfile
import tempfile

# Setup foldername and filename
zip_filename = "C:/Users/phill/Companion App Save Folder/exp1.rs"
output_folder = zip_filename[:zip_filename.rfind("/")]
#
# # Make a temporary directory to put data into. This temporary directory will be removed by calling temp.cleanup()
# temp = tempfile.TemporaryDirectory()
#
# # Create .csv file and write text to it.
# filename = "testoutput1.csv"
# text = "Hello World!"
# file = open(temp.name + "/" + filename, "w")
# file.write(text)
# file.close()
#
# # Add files from temp directory to .rs file
# with zipfile.ZipFile(zip_filename, "w") as zipper:
#     for file in os.listdir(temp.name):
#         print("Adding:", file, " to .rs")
#         zipper.write(temp.name + "/" + file, file)
#
# # remove temp folder
# temp.cleanup()

# Extract .rs to output_folder
zipper2 = zipfile.ZipFile(zip_filename, "r")
zipper2.extractall(output_folder)
