import nfc
from nfc.clf import RemoteTarget
import pygame
import time

pygame.mixer.init(44100, -16, 1, 128)
sound = pygame.mixer.Sound('sound.wav')
clf = nfc.ContactlessFrontend('usb')
print(clf)
service_code = 0x008b

def play():
    sound.play()
    return

while True:
    try:
        target = clf.sense(RemoteTarget('212F'))
        if target is None:
            continue;
        tag = nfc.tag.activate(clf, target)
        sc = nfc.tag.tt3.ServiceCode(service_code >> 6 ,service_code & 0x3f)
        bc = nfc.tag.tt3.BlockCode(0, service=0)
        data = tag.read_without_encryption([sc], [bc])
        print(str(ord(data[11:12]) + ord(data[12:13]) * 256) + '円')
        play()
        while pygame.mixer.get_busy() == True:
            time.sleep(0.1)
        time.sleep(0.7)
    except KeyboardInterrupt:
        exit()
    except nfc.tag.tt3.Type3TagCommandError:
        time.sleep(0.7)
