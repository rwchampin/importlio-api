import os
import subprocess

def start_chromedriver():
    # Command to start ChromeDriver in a new terminal window
    cmd = "open -a Terminal ./chromedriver"

    # Execute the command in a separate terminal window
    subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    start_chromedriver()
