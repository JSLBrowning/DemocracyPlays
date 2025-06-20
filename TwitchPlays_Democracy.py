import random
import keyboard
import pydirectinput
import pyautogui
import time
import TwitchPlays_Connection
from TwitchPlays_KeyCodes import *
from collections import defaultdict

##################### GAME VARIABLES #####################

# Replace this with your Twitch username. Must be all lowercase.
TWITCH_CHANNEL = 'dougdougw'

# If streaming on Youtube, set this to False
STREAMING_ON_TWITCH = True

# If you're streaming on Youtube, replace this with your Youtube's Channel ID
# Find this by clicking your Youtube profile pic -> Settings -> Advanced Settings
YOUTUBE_CHANNEL_ID = "YOUTUBE_CHANNEL_ID_HERE"

# If you're using an Unlisted stream to test on Youtube, replace "None" below with your stream's URL in quotes.
# Otherwise you can leave this as "None"
YOUTUBE_STREAM_URL = None

##################### MESSAGE QUEUE VARIABLES #####################

VOTE_INTERVAL = 1.0  # Time window for counting votes (in seconds)
pyautogui.FAILSAFE = False

##########################################################

# Count down before starting, so you have time to load up the game
countdown = 5
while countdown > 0:
    print(countdown)
    countdown -= 1
    time.sleep(1)

if STREAMING_ON_TWITCH:
    t = TwitchPlays_Connection.Twitch()
    t.twitch_connect(TWITCH_CHANNEL)
else:
    t = TwitchPlays_Connection.YouTube()
    t.youtube_connect(YOUTUBE_CHANNEL_ID, YOUTUBE_STREAM_URL)


def execute_command(cmd):
    try:
        print(f"Executing winning command: {cmd}")

        # Now that you have the winning command, this is where you add your game logic
        # Example GTA V Code
        if cmd == "left":
            HoldAndReleaseKey(A, 2)
        elif cmd == "right":
            HoldAndReleaseKey(D, 2)
        elif cmd == "drive":
            ReleaseKey(S)
            HoldKey(W)
        elif cmd == "reverse":
            ReleaseKey(W)
            HoldKey(S)
        elif cmd == "stop":
            ReleaseKey(W)
            ReleaseKey(S)
        elif cmd == "brake":
            HoldAndReleaseKey(SPACE, 0.7)
        elif cmd == "shoot":
            pydirectinput.mouseDown(button="left")
            time.sleep(1)
            pydirectinput.mouseUp(button="left")
        elif cmd == "aim up":
            pydirectinput.moveRel(0, -30, relative=True)
        elif cmd == "aim right":
            pydirectinput.moveRel(200, 0, relative=True)

    except Exception as e:
        print("Encountered exception: " + str(e))


# Main loop
command_counts = defaultdict(int)
last_vote_time = time.time()

while True:
    # Check for new messages
    new_messages = t.twitch_receive_messages()
    if new_messages:
        for message in new_messages:
            cmd = message['message'].lower().strip()
            command_counts[cmd] += 1

    # Check if it's time to process votes
    current_time = time.time()
    if current_time - last_vote_time >= VOTE_INTERVAL:
        if command_counts:
            # Find the command with highest votes
            max_count = max(command_counts.values())
            winning_commands = [
                cmd for cmd, count in command_counts.items() if count == max_count]

            # Randomly select a winner if there's a tie
            winning_command = random.choice(winning_commands)

            # Execute the winning command
            execute_command(winning_command)

            # Reset counts for next interval
            command_counts.clear()

        last_vote_time = current_time

    # Check for exit key
    if keyboard.is_pressed('shift+backspace'):
        exit()
