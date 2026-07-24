from PIL import Image
from cryptography.fernet import Fernet
import base64
import hashlib
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(SCRIPT_DIR, "img.jpg")

END_MARKER = " <--END--> "   # marks where the hidden message stops


# STEP 1: Turn a password into a valid encryption key
def get_key_from_password(password):
    # hash the password to always get 32 bytes, then encode for Fernet
    hashed = hashlib.sha256(password.encode()).digest()
    key = base64.urlsafe_b64encode(hashed)
    return key


# STEP 2: Encrypt / Decrypt the message using the password
def encrypt_message(message, password):
    key = get_key_from_password(password)
    f = Fernet(key)
    encrypted_bytes = f.encrypt(message.encode())
    return encrypted_bytes.decode()  # convert to plain text so we can hide it


def decrypt_message(encrypted_text, password):
    key = get_key_from_password(password)
    f = Fernet(key)
    decrypted_bytes = f.decrypt(encrypted_text.encode())
    return decrypted_bytes.decode()


# STEP 3: Convert text to a string of 0s and 1s
def text_to_bits(text):
    bits = ""
    for char in text:
        bits += format(ord(char), "08b")   # each character -> 8 bits
    return bits


# STEP 4: Convert bits back into text
def bits_to_text(bits):
    text = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        text += chr(int(byte, 2))
    return text


# STEP 5: Hide the message inside the image
def hide_message(image_path, message, password, output_path=None):
    if output_path is None:
        output_path = os.path.join(SCRIPT_DIR, "img_encoded.png")
    image = Image.open(image_path).convert("RGB")
    pixels = image.load()

    encrypted_message = encrypt_message(message, password)
    full_message = encrypted_message + END_MARKER
    bits = text_to_bits(full_message)

    if len(bits) > image.width * image.height * 3:
        print("Message is too long to fit in this image.")
        return

    bit_index = 0
    for y in range(image.height):
        for x in range(image.width):
            if bit_index >= len(bits):
                break

            r, g, b = pixels[x, y]
            new_r, new_g, new_b = r, g, b

            if bit_index < len(bits):
                new_r = (r & ~1) | int(bits[bit_index])  # change last bit of red
                bit_index += 1
            if bit_index < len(bits):
                new_g = (g & ~1) | int(bits[bit_index])  # change last bit of green
                bit_index += 1
            if bit_index < len(bits):
                new_b = (b & ~1) | int(bits[bit_index])  # change last bit of blue
                bit_index += 1

            pixels[x, y] = (new_r, new_g, new_b)

        if bit_index >= len(bits):
            break

    image.save(output_path)
    print(f"Message hidden successfully! Saved as: {output_path}")


# STEP 6: Reveal the message from the image
def reveal_message(image_path, password):
    image = Image.open(image_path).convert("RGB")
    pixels = image.load()

    all_text = ""
    current_bits = ""
    found_marker = False

    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]
            for value in (r, g, b):
                current_bits += str(value & 1)
                if len(current_bits) == 8:
                    all_text += chr(int(current_bits, 2))
                    current_bits = ""
                    if END_MARKER in all_text:
                        found_marker = True
                        break
            if found_marker:
                break
        if found_marker:
            break

    if not found_marker:
        print("No hidden message found in this image.")
        return

    encrypted_message = all_text.split(END_MARKER)[0]

    try:
        message = decrypt_message(encrypted_message, password)
        print("Hidden message:", message)
    except Exception:
        print("Wrong password, or the image has no valid hidden message.")


# STEP 7: Simple menu to use the program
def main():
    print("=== Image Steganography ===")
    print("1. Hide a message in img.jpg")
    print("2. Reveal a message from an image")
    choice = input("Choose 1 or 2: ")

    if choice == "1":
        password = input("Set a password: ").strip()
        confirm = input("Confirm password: ").strip()

        if password != confirm:
            print("Passwords do not match.")
            return

        message = input("Enter your secret message: ").strip()
        hide_message(IMAGE_PATH, message, password)

    elif choice == "2":
        image_name = input("Enter the image filename (e.g. img_encoded.png): ").strip()
        # if user just types a filename, look for it next to this script
        image_path = image_name if os.path.isabs(image_name) else os.path.join(SCRIPT_DIR, image_name)

        if not os.path.exists(image_path):
            print(f"[!] Could not find: {image_path}")
            return

        password = input("Enter the password: ").strip()
        reveal_message(image_path, password)

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()