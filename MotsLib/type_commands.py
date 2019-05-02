import comms;
import time;

text = "";
while text!="exit":
    print(">", end = " ");
    text = input();
    cmd = list(map(int, text.split()));
    if text != "exit":
      comms.send(cmd);
