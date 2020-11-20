import pyautogui as ag
import sys
import time

COLORS = {
        (143, 188, 143): 8,
        (128, 0, 0): 7,
        (224, 255, 255): 6,
        (147, 112, 219): 5,
        (176, 196, 222): 4,
        (255, 160, 122): 3
        }

def pre():
    x, y = ag.locateCenterOnScreen('tile_small.png')

    ag.click(x, y - 100)
    ag.moveTo(x, y)

# debug mode
    ag.press("enter", interval=0.1)
    ag.write("xyzzy", interval=0.1)
    ag.hotkey("shiftleft", "return", interval=0.1)
    ag.press("return", interval=0.1)

# switch to max difficulty
    ag.hotkey("ctrl", "7")

    time.sleep(1)

pre()

# required for cleaner measurements
ag.PAUSE = 0.02

x_topleft, y_topleft = ag.locateCenterOnScreen('tile_small.png')
x_free, y_free = x_topleft - 50, y_topleft - 40

# known good settings over RDP for local Windows Server 2019 vbox: 4/3/6/1/50
# known good settings for the remote server: 5/17/18/1/50

SAMPLES_PER_TILE = 4    # increase to prevent false negatives
TOLERANCE = 3           # low-pass filter, script detects lower as clear
CUTOFF = 6              # hi-pass filter, script detects higher as mines
EXTRA_CHECKS = 1        # increase to prevent false positives (re-check clear)
TOO_LONG_RETRY = 50     # take another measurement if a single one takes too long

found = 0
to_skip = []
known_negative = []

#W, H, MINES = 20, 20, 360
W, H, MINES = 22, 22, 436

while True:
    x = x_topleft - 30

    for tile_x in range(W):
        y = y_topleft
        searching_stage = 0
        x += 20
        while True:
            x = x + (2 if searching_stage == 0 else 1)
            p = tuple(ag.pixel(x, y))
            if searching_stage == 0:
                if (p == (255, 255, 255)) or (p == (255, 0, 0)):
                    searching_stage = 1
            else:
                if not ((p == (255, 255, 255)) or (p == (255, 0, 0))):
                    break
        
        y = y_topleft - 30

        for tile_y in range(H):
            y += 20
            searching_stage = 0
            while True:
                y = y + (2 if searching_stage == 0 else 1)
                #print(x, y)
                p = tuple(ag.pixel(x, y))
                if searching_stage == 0:
                    if (p == (255, 255, 255)) or (p == (255, 0, 0)):
                        searching_stage = 1
                else:
                    if not ((p == (255, 255, 255)) or (p == (255, 0, 0))):
                        break
            
            if not (ag.pixelMatchesColor(x, y, (0, 0, 255))):
                print ("Already checked")
                continue
            
            if (tile_x, tile_y) in to_skip:
                continue

            check_positive = False
            for check in range(1 + EXTRA_CHECKS):
                tries = []
                for i in range(SAMPLES_PER_TILE):
                    while True:
                        ag.moveTo(x_free, y_free)
                        while True:
                            if (ag.pixelMatchesColor(x, y - 1, (255, 255, 255))):
                                break
                        ag.moveTo(x, y)
                        ag.PAUSE = 0.01
                        for t in range(1000):
                            if (ag.pixelMatchesColor(x, y - 1, (255, 0, 0))):
                                break
                        ag.PAUSE = 0.02

                        if t < TOO_LONG_RETRY:
                            break
                    tries += [t]
                    if t < TOLERANCE:
                        break
                
                print(tile_x, tile_y, tries)
                
                if min(tries) < TOLERANCE:
                    check_positive = True
                    continue

                if min(tries) > CUTOFF:
                    to_skip += [(tile_x, tile_y)]
                    
                check_positive = False
                break

            if check_positive:
                ag.click(x, y)
                known_negative += [(tile_x, tile_y)]
                time.sleep(0.1)
                p = tuple(ag.pixel(x + 5, y))
                negative_neighbors = 0
                if (p in COLORS):
                    for i in range(tile_x - 1, tile_x + 1 + 1, 1):
                        for j in range(tile_y - 1, tile_y + 1 + 1, 1):
                            if (i, j) == (tile_x, tile_y):
                                continue
                            if ((i, j) in known_negative) or i < 0 or j < 0 or i == W or j == H:
                                negative_neighbors += 1

                    if negative_neighbors == (8 - COLORS[p]):
                        for i in range(tile_x - 1, tile_x + 1 + 1, 1):
                            for j in range(tile_y - 1, tile_y + 1 + 1, 1):
                                if (i, j) != (tile_x, tile_y):
                                    to_skip += [(i, j)]
                elif (p == (255, 0, 0)):
                    print ("Failed!")
                    sys.exit()

                found += 1

            if found == (W * H - MINES):
                print("All tiles cleared")
                sys.exit()

