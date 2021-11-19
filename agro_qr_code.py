# Python program to generate QR code
from qrtools.qrtools import QR

# creates the QR object
my_QR = QR(data = [u"geeksforgeeks", u"https://www.geeksforgeeks.org/"],
									data_type = 'bookmark')

# encodes to a QR code
my_QR.encode()
