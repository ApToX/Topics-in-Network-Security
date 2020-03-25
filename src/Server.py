import smtpd
import asyncore
import email
import re
import puremagic
import os


class Virus:
    def __init__(self, name, signature_size, signature):
        self.name = name
        self.signature_size = signature_size
        self.signature = signature


# Builds Viruses Database from existing file:
def virus_data_builder(filename):
    temp_virus_list = []

    with open(filename, "rb") as f:
        byte = f.read(2)
        while byte:
            virus_signature_size = int.from_bytes(byte, byteorder='little') - 18  # Int type
            # print(virus_signature_size)  # TESTING #
            virus_name = f.read(16).decode("utf-8")  # String type
            # print(virus_name)  # TESTING #
            virus_signature = f.read(virus_signature_size)  # Byte Type
            # print(virus_signature)  # TESTING #

            temp_virus_list.append(Virus(virus_name, virus_signature_size, virus_signature))

            byte = f.read(2)

    return temp_virus_list


VIRUS_LIST = virus_data_builder("Files/signatures")
BANNED_FILE_NAMES = ["virus", "spam"]


def validate_file_signature(data):
    for virus in VIRUS_LIST:
        if virus.signature in data:
            # print(virus.name)
            return False
    return True


def validate_file_name(filename):
    for expression in BANNED_FILE_NAMES:
        if re.search(expression, filename, re.IGNORECASE):
            return False
    return True


def get_file_type_match(filename):
    name, extension = os.path.splitext(filename)  # Check visible file extension
    binary_extension = puremagic.from_file(filename)  # Check file signature extension

    return extension, binary_extension


class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        if not self.validate_email(data.decode("utf-8")):
            return "554 Email validation failed"

        # Extract Email subject and text message
        msg = email.message_from_string(data.decode("utf-8"))
        msg_body = "None"
        msg_subject = "None"
        for part in msg.walk():
            if part["Subject"]:
                msg_subject = part["Subject"]
            if part.get_content_maintype() == 'text':
                msg_body = part.get_payload()

        # Print Email Message
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to  :', rcpttos)
        print('Message Subject:', msg_subject)
        # print('Message length        :', len(data))
        print('Message:\n' + msg_body)
        return

    @staticmethod
    def validate_email(data):
        msg = email.message_from_string(data)
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue

            payload = part.get_payload(decode=True)
            if not validate_file_signature(payload):
                print("Found banned file signature! Blocked email message.")
                return False

            filename = part.get_filename()
            if not filename:
                continue
            if not validate_file_name(filename):
                print("Found banned filename! Blocked email message.")
                return False
            # Validate File Extension Match
            expected, real = get_file_type_match(filename)
            if expected != real:
                print('WARNING!\nReceived email contains unexpected file. '
                      'Expected File Type: "{0}" | Real Type: "{1}".'.format(expected, real))

        print()  # For aesthetics purpose
        return True


server = CustomSMTPServer(('127.0.0.1', 1025), None)

asyncore.loop()
