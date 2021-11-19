import qrcode
from qrcode import ERROR_CORRECT_L

qr = qrcode.QRCode(
    version=3,
    error_correction=ERROR_CORRECT_L,
    box_size=3,
    border=5
)

dic  = [
    """    
        BEGIN:VCARD \n
        VERSION:2.1 \n
        N:PARHETO;TOURE \n
        FN:PARHETO TOURE \n
        ORG:AGRO-MAP CI \n
        TITLE:DEVELOPPEUR \n
        TEL;WORK;VOICE:2250748566846 \n
        ADR;WORK:;;3800 Zanker Rd;San Jose;CA;95134;United States of America \n
        EMAIL;PREF;INTERNET:m.toure@agro-map.com \n
        END:VCARD
    """
# data_encode = {
# 	'text': lambda data: data,
# 	'url': encode_url,
# 	'email': lambda data: 'mailto:' + re.compile(
# 		r'^mailto:', re.IGNORECASE
# 	).sub('', data),
# 	'emailmessage': lambda data: 'MATMSG:TO:' + data[0] + ';SUB:' + data[1] +
# 						';BODY:' + data[2] + ';;',
# 	'telephone': lambda data: 'tel:' + re.compile(
# 		r'^tel:', re.IGNORECASE
# 	).sub('', data),
# 	'sms': lambda data: 'SMSTO:' + data[0] + ':' + data[1],
# 	'mms': lambda data: 'MMSTO:' + data[0] + ':' + data[1],
# 	'geo': lambda data: 'geo:' + data[0] + ', ' + data[1],
# 	'bookmark': lambda data: "MEBKM:TITLE:" + data[0] + ";URL:" +
# 									data[1] + ";;",
# 	# phonebook or meCard should be a list of tuples like this:
# 	# [('N', 'Name'), ('TEL', '231698890'), ...]
# 	'phonebook': lambda data: "MECARD:" + ";".join([":".join(i)
# 										for i in data]) + ";"
# }

    # "ADAYE KOUAME PATRICE",
    # "CEO AGRO-MAP",
    # "+225 07 09 29 50 60",
    # "+225 27 22 53 10 72",
    # "k.adaye@agro-map.com",
    # "AGRO-MAP",
]
qr.add_data(dic)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
#img = qr.make_image(fill_color="blue", back_color="white")
img.save("info_boss5.png")