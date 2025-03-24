from storage import PasswordStorage
from crypto import generate_share_key, encrypt_share, decrypt_share
from codegen import generate_code
from decode import image_to_binary, binary_to_data

def main():
    storage = PasswordStorage()
    
    while True:
        print("\n1. Add Password\n2. Share Password\n3. Decode Shared Code\n4. Exit")
        choice = input("Choose: ")

        if choice == "1":
            alias = input("Enter alias: ")
            password = input("Enter password: ")
            storage.add_password(alias, password)
            print("Password saved!")

        elif choice == "2":
            alias = input("Enter alias to share: ")
            password = storage.get_password(alias)
            if not password:
                print("Alias not found!")
                continue
            share_key = generate_share_key()
            encrypted_data, share_key = encrypt_share(password, share_key)
            code_path = generate_code(encrypted_data)
            print(f"Code saved as {code_path}")
            print("Share this key with recipient:", share_key.hex())

        elif choice == "3":
            image_path = input("Enter code image path: ")
            share_key = bytes.fromhex(input("Enter share key (hex): "))
            binary = image_to_binary(image_path)
            encrypted_data = binary_to_data(binary)
            try:
                password = decrypt_share(encrypted_data, share_key)
                print("Decrypted password:", password)
            except Exception as e:
                print("Error:", str(e))

        elif choice == "4":
            break

if __name__ == "__main__":
    main()