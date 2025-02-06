# igate_frombot
Receives text from a telegram bot and sends it as a message to an iGate LoRa APRS<br><br>

The project, very simple, consists of a code that waits for a text from a telegram bot (it can be used the same bot used in igate_monitor or a new one) and if it starts with "/" it processes it to retrieve the recipient callsign of the message and the text to send via APRS. For this operation a second code is executed that prepares the frame and sends it on APRS using a connection in KISS to the TNC of an iGate.<br>

Edit the igate_frombot.py code and in the configuration section specify the token of the bot you are going to use, the ip of the tnc/igate, the port, etc. These parameters will be passed to the second code (igate_sender.py) that must reside in the same folder. **To work igate_frombot.py needs the telepot library that you will have to install with pip.**<br>

The igate_sender.py code does not need to be edited in its message sending function and receives parameters (and executes) from the previous code. It basically prepares the frame in the required AX.25 format, packages it in KISS and sends it to the LoRa gateway for forwarding in the APRS network.<br>

Syntax to send a message from the bot:
**/callsign-nn text of the message**<br>

Command to run and make the code operational in background:
**nohup igate_frombot.py &**<br>

![](https://github.com/ik5xmk/igate_frombot/blob/main/igate_frombot_01.jpg)<br>
![](https://github.com/ik5xmk/igate_frombot/blob/main/igate_frombot_02.jpg)



