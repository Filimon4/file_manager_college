import base64
from typing import List
import json
import os
import random
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QSpinBox,
    QCheckBox
)

class CipherDialog(QDialog):
    def __init__(self, selectedFile='', parentOfSelectedFile=''):
        super().__init__()
        self.setWindowTitle("Cipher Parameters")

        self.selectedFile = selectedFile
        self.parentOfSelected = parentOfSelectedFile

        self.fileSelected = self.selectedFile.split('/')[-1]

        self.file_to_cipher_edit = QLineEdit()
        if self.selectedFile:
            self.file_to_cipher_edit.setText(self.selectedFile)
        self.output_file_edit = QLineEdit()
        if self.parentOfSelected:
            outputFileName = f"{self.fileSelected.split('.')[0]}-CipherText.b64"
            self.output_file_edit.setText(f"{self.parentOfSelected}/{outputFileName}")
        self.b1_box = QLineEdit()
        self.b1_box.setInputMask("HHHHHHHH")
        self.b1_box.setMaxLength(8)
        self.b2_box = QLineEdit()
        self.b2_box.setInputMask("HHHHHHHH")
        self.b2_box.setMaxLength(8)
        self.b3_box = QLineEdit()
        self.b3_box.setInputMask("HHHHHHHH")
        self.b3_box.setMaxLength(8)
        self.b4_box = QLineEdit()
        self.b4_box.setInputMask("HHHHHHHH")
        self.b4_box.setMaxLength(8)

        self.rewriteKeys = QCheckBox('Перезаписать ключи')
        self.rewriteKeys.setChecked(False)


        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        file_to_cipher_layout = QVBoxLayout()
        file_to_cipher_input = QHBoxLayout()
        file_to_cipher_layout.addWidget(QLabel("Зашифровать данные из:"))
        file_to_cipher_input.addWidget(self.file_to_cipher_edit)
        file_to_cipher_layout.addLayout(file_to_cipher_input)
        browse_button = QPushButton("Выбрать") # change to created input file
        browse_button.clicked.connect(self.browse_file_to_cipher)
        file_to_cipher_input.addWidget(browse_button)
        layout.addLayout(file_to_cipher_layout)

        output_file_layout = QVBoxLayout()
        output_file_layout.addWidget(QLabel("Сохранить зашифрованные данные в:"))
        output_file_layout.addWidget(self.output_file_edit)
        layout.addLayout(output_file_layout)

        cipher_params_layout = QVBoxLayout()
        cipher_params_layout.addWidget(QLabel("Ключи для шифрования:"))
        generate_button = QPushButton('Сгенерировать новые ключи')
        generate_button.clicked.connect(self.set_generate_keys)
        use_prev_keys_button = QPushButton('Использовать предыдущие ключи')
        use_prev_keys_button.clicked.connect(self.set_prev_keys)
        cipher_params_layout.addWidget(generate_button)
        cipher_params_layout.addWidget(use_prev_keys_button)
        for label_text, spinbox in zip(["K1:", "K2:", "K3:", "K4:"], [self.b1_box, self.b2_box, self.b3_box, self.b4_box]):
            cipher_keys_layout = QHBoxLayout()
            cipher_keys_layout.addWidget(QLabel(label_text), 1)
            cipher_keys_layout.addWidget(spinbox, 100)
            cipher_params_layout.addLayout(cipher_keys_layout)
        cipher_params_layout.addWidget(self.rewriteKeys)
        layout.addLayout(cipher_params_layout)
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.ok_clicked)
        layout.addWidget(ok_button)
        self.setLayout(layout)

    def set_prev_keys(self):
        keys = []
        with open('./keys.json', 'r') as f:
            data = json.load(f)
            for i in data:
                keys.append(data[i])
        print(keys)
        self.b1_box.setText(keys[0])
        self.b2_box.setText(keys[1])
        self.b3_box.setText(keys[2])
        self.b4_box.setText(keys[3])

    def set_generate_keys(self):
        keys = self.generate_hex_keys()
        self.b1_box.setText(keys[0])
        self.b2_box.setText(keys[1])
        self.b3_box.setText(keys[2])
        self.b4_box.setText(keys[3])

    def generate_hex_keys(self):
        keys = []
        def generate_random_hex():
            return '{:08x}'.format(random.randint(0, 2**32-1))

        for i in range(4):
            random_hex = generate_random_hex()
            if random_hex:
                keys.append(str(random_hex))
            else:
                keys.append('11111111')

        return keys


    def browse_file_to_cipher(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.file_to_cipher_edit.setText(selected_files[0])

    def is_file_path_available(self, file_path):
        return not os.path.exists(file_path)

    def ok_clicked(self):
        file_to_cipher = self.file_to_cipher_edit.text().strip()
        output_file_path = self.output_file_edit.text().strip()
        b1 = self.b1_box.text()
        b2 = self.b2_box.text()
        b3 = self.b3_box.text()
        b4 = self.b4_box.text()

        if not file_to_cipher or not output_file_path:
            print("Please provide both input and output file paths.")
            return

        if not self.is_file_path_available(output_file_path):
            print("Output file path already exists. Choose a different one.")
            return

        # Call your cipher algorithm function with the provided parameters here
        print("Ciphering...")
        print(f"File to Cipher: {file_to_cipher}")
        print(f"Output File Path: {output_file_path}")
        print(f"Cipher Parameters: {b1}, {b2}, {b3}, {b4}")
        self.accept()

class CipherAlgo:
    defaultKeys = []
    with open('./keys.json', "r") as f:
        data = json.load(f)
        for i in data:
            defaultKeys.append(data[i])
    def __init__(self):
        self.input = ''
        self.output = ''

    def feistel_round(self, left: int, right: int, key: int) -> tuple:
        new_right = left ^ key
        return right, new_right

    def feistel_cipher(self, plaintext: bytes, keys: List[int] = defaultKeys) -> bytes:
        padding_length = 8 - (len(plaintext) % 8)
        plaintext += bytes([padding_length] * padding_length)

        blocks = [plaintext[i:i+8] for i in range(0, len(plaintext), 8)]
        ciphertext = b''

        for block in blocks:
            block_int = int.from_bytes(block, byteorder='big')
            left = block_int >> 32
            right = block_int & 0xFFFFFFFF

            for key in keys:
                left, right = self.feistel_round(left, right, key)

            left, right = right, left

            cipher_block = (left << 32 | right).to_bytes(8, byteorder='big')
            ciphertext += cipher_block

        return ciphertext

    def feistel_decipher(self, ciphertext: bytes, keys: List[int] = defaultKeys) -> bytes:
        blocks = [ciphertext[i:i+8] for i in range(0, len(ciphertext), 8)]
        plaintext = b''

        for block in blocks:
            block_int = int.from_bytes(block, byteorder='big')
            left = block_int >> 32
            right = block_int & 0xFFFFFFFF

            for key in reversed(keys):
                left, right = self.feistel_round(left, right, key)

            left, right = right, left

            plain_block = (left << 32 | right).to_bytes(8, byteorder='big')
            plaintext += plain_block

        padding_length = plaintext[-1]
        plaintext = plaintext[:-padding_length]

        return plaintext

class Encrypt(CipherAlgo):

    def __init__(self, app):
        super().__init__()
        self.app = app

        self.actionCipher = self.app.ui.actionCipher
        self.actionCipher.triggered.connect(self.actionClicked)

    def actionClicked(self):
        selectedFile = self.app.FileV.getSingleSelectedFile()

        filePath = ''
        fileParentPath = ''
        if selectedFile:
            filePath = self.app.FileS.engine.filePath(selectedFile)
            fileParentPath = self.app.FileS.engine.filePath(selectedFile.parent())
        dialog = CipherDialog(filePath, fileParentPath)
        result = dialog.exec_()


        # fileName = self.app.FileS.engine.fileName(selectedFile)
        # readBinary = self.app.FileO.readBinaryFile(selectedFile)
        # plain_text = base64.b64encode(readBinary)
        # ciphertext = str.encode(f"{fileName}") + str.encode("\n") + super().feistel_cipher(plain_text)
        # self.app.FileO.newFileBinarySilent(f"{fileName.split('.')[0]}.b64", ciphertext)


class Decrypt(CipherAlgo):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.actionDecipher = self.app.ui.actionDecipher
        self.actionDecipher.triggered.connect(self.actionClicked)

    def actionClicked(self):
        selectedFile = self.app.FileV.getSingleSelectedFile()
        readBinary = self.app.FileO.readBinaryFile(selectedFile)
        fileName, cipher = readBinary.split(b'\n')
        deciphertext = super().feistel_decipher(cipher)
        self.app.FileO.newFileBinarySilent(f"{fileName.decode()}", base64.b64decode(deciphertext))

