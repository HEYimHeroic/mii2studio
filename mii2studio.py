import subprocess
import sys
import codecs
from binascii import hexlify
from os import remove
from requests import get, post
from struct import pack

if len(sys.argv) < 4:
    print("CLI Usage: python mii2studio.py <input mii file / qr code / cmoc entry number> <output studio mii file> <input type (wii/ds/3ds/wiiu/miitomo/switchdb/switch/studio)>\n")
    input_file = input("Enter the path to the input file (binary file or QR Code), a CMOC entry number, or a URL to a QR Code: ")
    output_file = input("Enter the path to the output file (which will be importable with Mii Studio): ")
    input_type = input("Enter the input type (wii/ds/3ds/wiiu/miitomo/switchdb/switch/studio): ")
    print("")
else:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    input_type = sys.argv[3]

if input_type == "wii":
    from gen1_wii import CoreDataWii
    try:
        if len(input_file.replace("-", "")) <= 12 and "." not in input_file:
            print("Detected that the input is a Check Mii Out Channel entry number.\n")

            num = int(format(int(input_file.replace("-", "")), '032b').zfill(40)[8:], 2) # the cmoc entry numbr is scrambled using a lot of bitwise operations
            num ^= 0x20070419
            num ^= (num >> 0x1D) ^ (num >> 0x11) ^ (num >> 0x17)
            num ^= (num & 0xF0F0F0F) << 4
            num ^= ((num << 0x1E) ^ (num << 0x12) ^ (num << 0x18)) & 0xFFFFFFFF

            query = get("https://miicontestp.wii.rc24.xyz/cgi-bin/search.cgi?entryno=" + str(num)).content

            if len(query) != 32: # 32 = empty response
                with open("qr.cfsd", "wb") as f:
                    f.write(query[56:130]) # cut the Mii out of the file
            else:
                print("Mii not found.")
            
            input_file = "qr.cfsd"
        else:
            input_file = input_file
    except ValueError:
        input_file = input_file
    
    orig_mii = CoreDataWii.from_file(input_file)

    if input_file == "qr.cfsd":
        try:
            remove("qr.cfsd")
        except PermissionError:
            print("Unable to remove temporary file.")
elif input_type == "ds":
    from gen1_ds import CoreDataDs
    orig_mii = CoreDataDs.from_file(input_file)
elif input_type == "3ds" or input_type == "wiiu" or input_type == "miitomo":
    from gen2_wiiu_3ds_miitomo import CoreData3ds
    from Crypto.Cipher import AES
    if ".png" in input_file.lower() or ".jpg" in input_file.lower() or ".jpeg" in input_file.lower(): # crappy way to detect if input is an mage
        if "http" in input_file.lower():
            print("Detected that the input is a URL to a Mii QR Code.\n")

            with open("temp", "wb") as f:
                f.write(get(input_file).content)
                f.close()
            
            input_file = "temp"
        else:
            print("Detected that the input is a Mii QR Code.\n")

        with open(input_file, "rb") as f:
            read = f.read()
            decoded_qr = post("https://qrcode.rc24.xyz/qrcode.php", {"image": read}).content # zbar sucks to run on a client so we use this api

        # https://gist.github.com/jaames/96ce8daa11b61b758b6b0227b55f9f78

        key = bytes([0x59, 0xFC, 0x81, 0x7E, 0x64, 0x46, 0xEA, 0x61, 0x90, 0x34, 0x7B, 0x20, 0xE9, 0xBD, 0xCE, 0x52])

        with open("qr.cfsd", "wb") as f:
            nonce = decoded_qr[:8]
            cipher = AES.new(key, AES.MODE_CCM, nonce + bytes([0, 0, 0, 0]))
            content = cipher.decrypt(decoded_qr[8:372])
            result = content[:12] + nonce + content[12:]
            f.write(result)

        input_file = "qr.cfsd"

    orig_mii = CoreData3ds.from_file(input_file)

    if input_file == "qr.cfsd":
        try:
            remove("qr.cfsd")
        except PermissionError:
            print("Unable to remove temporary file.")
elif input_type == "switchdb":
    from gen3_switch import CoreDataSwitch
    orig_mii = CoreDataSwitch.from_file(input_file)
elif input_type == "switch":
    from gen3_switchgame import CharInfoSwitch
    orig_mii = CharInfoSwitch.from_file(sys.argv[1])
elif input_type == "miistudio":
    from gen3_studio import MiidataStudio
    orig_mii = MiidataStudio.from_file(sys.argv[1])
else:
    print("Error: Invalid input type.")
    exit()

def u8(data):
    return pack(">B", data)

if input_type != "studio":
    print("Mii Info:\n")
    
    print("Mii Name: " + orig_mii.mii_name)
    
    if "switch" not in input_type:
        if orig_mii.creator_name != "\0" * 10:
            print("Creator Name: " + orig_mii.creator_name)
        if orig_mii.birth_month != 0 and orig_mii.birth_day != 0:
            print("Birthday: " + str(orig_mii.birth_month).zfill(2) +
                  "/" + str(orig_mii.birth_day).zfill(2) + " (MM/DD)")

    favorite_colors = {
        0: "Red",
        1: "Orange",
        2: "Yellow",
        3: "Lime Green",
        4: "Forest Green",
        5: "Royal Blue",
        6: "Sky Blue",
        7: "Pink",
        8: "Purple",
        9: "Brown",
        10: "White",
        11: "Black"
    }

    print("Favorite Color: " + favorite_colors[orig_mii.favorite_color])
    
    print("Height: " + str(orig_mii.body_height) + " out of 127")
    print("Build: " + str(orig_mii.body_weight) + " out of 127")

    mii_types = {
        0x00: "Special Mii - Gold Pants",
        0x20: "Normal Mii - Black Pants",
        0x40: "Special Mii - Gold Pants",
        0x60: "Normal Mii - Black Pants",
        0xC0: "Foreign Mii - Blue Pants (uneditable)",
        0xE0: "Normal Mii - Black Pants",
        0x100: "???"
    }
        
    print("Gender: Male" if orig_mii.gender == 0 else "Gender: Female")
    
    if "switch" not in input_type:
        print("Mingle: Yes" if orig_mii.mingle == 0 else "Mingle: No")
    
    if "switch" not in input_type and input_type != "wii" and input_type != "ds":
        print("Copying: Yes" if orig_mii.copying == 1 else "Copying: No")

    print("")

    studio_mii = {}

    makeup = { # lookup table
        1: 1,
        2: 6,
        3: 9,
        9: 10
    }

    wrinkles = { # lookup table
        4: 5,
        5: 2,
        6: 3,
        7: 7,
        8: 8,
        10: 9,
        11: 11
    }

    # ue generate the Mii Studio file by reading each Mii format from the Kaitai files.
    # unlike consoles which store Mii data in an odd number of bits,
    # all the Mii data for a Mii Studio Mii is stored as unsigned 8-bit integers. makes it easier.

    if "switch" not in input_type:
        if orig_mii.facial_hair_color == 0:
            studio_mii["facial_hair_color"] = 8
        else:
            studio_mii["facial_hair_color"] = orig_mii.facial_hair_color
    else:
        studio_mii["facial_hair_color"] = orig_mii.facial_hair_color
    studio_mii["beard_goatee"] = orig_mii.facial_hair_beard
    studio_mii["body_weight"] = orig_mii.body_weight
    if input_type == "wii" or input_type == "ds":
        studio_mii["eye_stretch"] = 3
    else:
        studio_mii["eye_stretch"] = orig_mii.eye_stretch
    if "switch" not in input_type:
        studio_mii["eye_color"] = orig_mii.eye_color + 8
    else:
        studio_mii["eye_color"] = orig_mii.eye_color
    studio_mii["eye_rotation"] = orig_mii.eye_rotation
    studio_mii["eye_size"] = orig_mii.eye_size
    studio_mii["eye_type"] = orig_mii.eye_type
    studio_mii["eye_horizontal"] = orig_mii.eye_horizontal
    studio_mii["eye_vertical"] = orig_mii.eye_vertical
    if input_type == "wii" or input_type == "ds":
        studio_mii["eyebrow_stretch"] = 3
    else:
        studio_mii["eyebrow_stretch"] = orig_mii.eyebrow_stretch
    if "switch" not in input_type:
        if orig_mii.eyebrow_color == 0:
            studio_mii["eyebrow_color"] = 8
        else:
            studio_mii["eyebrow_color"] = orig_mii.eyebrow_color
    else:
        studio_mii["eyebrow_color"] = orig_mii.eyebrow_color
    studio_mii["eyebrow_rotation"] = orig_mii.eyebrow_rotation
    studio_mii["eyebrow_size"] = orig_mii.eyebrow_size
    studio_mii["eyebrow_type"] = orig_mii.eyebrow_type
    studio_mii["eyebrow_horizontal"] = orig_mii.eyebrow_horizontal
    if input_type != "switchdb":
        studio_mii["eyebrow_vertical"] = orig_mii.eyebrow_vertical
    else:
        studio_mii["eyebrow_vertical"] = orig_mii.eyebrow_vertical + 3
    studio_mii["face_color"] = orig_mii.face_color
    if input_type == "wii" or input_type == "ds":
        if orig_mii.facial_feature in makeup:
            studio_mii["face_makeup"] = makeup[orig_mii.facial_feature]
        else:
            studio_mii["face_makeup"] = 0
    else:
        studio_mii["face_makeup"] = orig_mii.face_makeup
    studio_mii["face_type"] = orig_mii.face_type
    if input_type == "wii" or input_type == "ds":
        if orig_mii.facial_feature in wrinkles:
            studio_mii["face_wrinkles"] = wrinkles[orig_mii.facial_feature]
        else:
            studio_mii["face_wrinkles"] = 0
    else:
        studio_mii["face_wrinkles"] = orig_mii.face_wrinkles
    studio_mii["favorite_color"] = orig_mii.favorite_color
    studio_mii["gender"] = orig_mii.gender
    if "switch" not in input_type:
        if orig_mii.glasses_color == 0:
            studio_mii["glasses_color"] = 8
        elif orig_mii.glasses_color < 6:
            studio_mii["glasses_color"] = orig_mii.glasses_color + 13
        else:
            studio_mii["glasses_color"] = 0
    else:
        studio_mii["glasses_color"] = orig_mii.glasses_color
    studio_mii["glasses_size"] = orig_mii.glasses_size
    studio_mii["glasses_type"] = orig_mii.glasses_type
    studio_mii["glasses_vertical"] = orig_mii.glasses_vertical
    if "switch" not in input_type:
        if orig_mii.hair_color == 0:
            studio_mii["hair_color"] = 8
        else:
            studio_mii["hair_color"] = orig_mii.hair_color
    else:
        studio_mii["hair_color"] = orig_mii.hair_color
    studio_mii["hair_flip"] = orig_mii.hair_flip
    studio_mii["hair_type"] = orig_mii.hair_type
    studio_mii["body_height"] = orig_mii.body_height
    studio_mii["mole_size"] = orig_mii.mole_size
    studio_mii["mole_enable"] = orig_mii.mole_enable
    studio_mii["mole_horizontal"] = orig_mii.mole_horizontal
    studio_mii["mole_vertical"] = orig_mii.mole_vertical
    if input_type == "wii" or input_type == "ds":
        studio_mii["mouth_stretch"] = 3
    else:
        studio_mii["mouth_stretch"] = orig_mii.mouth_stretch
    if "switch" not in input_type:
        if orig_mii.mouth_color < 4:
            studio_mii["mouth_color"] = orig_mii.mouth_color + 19
        else:
            studio_mii["mouth_color"] = 0
    else:
        studio_mii["mouth_color"] = orig_mii.mouth_color
    studio_mii["mouth_size"] = orig_mii.mouth_size
    studio_mii["mouth_type"] = orig_mii.mouth_type
    studio_mii["mouth_vertical"] = orig_mii.mouth_vertical
    studio_mii["beard_size"] = orig_mii.facial_hair_size
    studio_mii["beard_mustache"] = orig_mii.facial_hair_mustache
    studio_mii["beard_vertical"] = orig_mii.facial_hair_vertical
    studio_mii["nose_size"] = orig_mii.nose_size
    studio_mii["nose_type"] = orig_mii.nose_type
    studio_mii["nose_vertical"] = orig_mii.nose_vertical

with open(output_file, "wb") as f:
    mii_data_bytes = ""
    mii_data = b""
    n = r = 256
    mii_dict = []
    if input_type == "miistudio":
        with open(input_file, "rb") as g:
            read = g.read()
            g.close()
        
        for i in range(0, len(hexlify(read)), 2):
            mii_dict.append(int(hexlify(read)[i:i+2], 16))
    else:
        mii_dict = studio_mii.values()
#    mii_data_bytes += hexlify(u8(0))
    mii_data += hexlify(u8(0))
    for v in mii_dict:
        eo = (7 + (v ^ n)) % 256 # encode the Mii, Nintendo seemed to have randomized the encoding using Math.random() in JS, but we removed randomizing
        n = eo
#        mii_data_bytes += hexlify(u8(mii_dict))
        mii_data += hexlify(u8(eo))
        f.write(u8(v))
        mii_data_bytes += str(hexlify(u8(v)), "ascii")

    f.close()
    
    #codecs.decode(mii_data_bytes, "hex")
    #mii_data_bytes = mii_data_bytes.decode("utf-8")
    
    url = "https://studio.mii.nintendo.com/miis/image.png?data=" + mii_data.decode("utf-8")

    print("Mii Render URLs:\n")
    print("Face: " + url + "&type=face&width=512")
    print("Body: " + url + "&type=all_body&width=512&instanceCount=1")
    print("Face (16x): " + url + "&type=face&width=512&instanceCount=16")
    print("Body (16x): " + url + "&type=all_body&width=512&instanceCount=16\n")
    print("Mii Studio code: " + mii_data_bytes)
    
    #print(f"URL: {url}")

    print("Mii Studio file written to " + output_file + ".\n")

    print("Completed Successfully")
