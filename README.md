# Overview:
TEAL (TElegram ALgorithm) v1.0.1, Discord bot which helps scan for newly created nations and send them a recruitment telegram. Created by Jyezet (me).
# Commands:
1. The first command (#setRecruiter|s) requests the time between requests, the amount of batches it'll request (up to 5 batches, 8 nations per batch) and a %TELEGRAM-ID%. The same command will also prevent other users (apart from the recruiter) from using TEAL commands (hence the command's name, setRecruiter).

2. The second command (#recruit|r) will start the recruitment session. TEAL will wait the requested amount of time, after which it'll scan for the most recently created nations, format the list, paste it into NationStates links and send them to the recruiter. The recruiter will then manually open the links and send them. After doing this, the recruiter will confirm the sending of the telegrams with #recruit, and repeat.

3. The third command (#finish|f) will end the recruitment session and unlock the bot for others to make use of it.
# How to add TEAL to your server:
1. Download the latest version of the code.

2. Go to https://discord.com/developers/applications and click on "New Application", and pick a name for it.

3. On the left menu, click on "Bot" and then on "Add Bot".

4. On the "Privileged Gateway Intents" toggle on all 3 of the options, scroll up, click on "Reset Token" and then click on "Copy". (Keep this token, you'll need it later).

5. On the left menu, click on "OAuth2" > "URL Generator". There, pick the option "Bot", and on the table below pick the option "Administrator". Scroll down to the bottom and open the generated link.

6. On the newly opened webpage, pick your discord server, click on "Continue" and "Authorize".

7. Open TEAL's code, scroll down to the bottom, and replace "TOKEN" with your token (Don't remove the quotes!).

8. Run the code. If your bot does not respond to your commands, install the python modules listed on top with python -m pip install MODULE
