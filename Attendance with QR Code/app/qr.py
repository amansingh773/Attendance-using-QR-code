import qrcode
import os
from PIL import Image

def Qr(url):
    print(url)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # Specify the directory and file name
    temp_dir = "static/tempqr"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    file_path = os.path.join(temp_dir, "qr_code.png")
    
    # Save the image to the specified file path
    img.save(file_path)
    
    print(file_path)
    return "ok"
