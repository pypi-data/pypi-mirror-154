from getpass import getpass
from os import getcwd
from os.path import join


def tutorial():
    print("""\033[33mYou are now in the tutorial, in which the data you input will not be saved.\033[0m
[Press Ctrl+C to exit the tutorial]
Span is an easy-to-use tool for creating and managing IKEv2 VPN servers in your Vultr account.
\033[1;34m[Task 1]\033[0m Before using Span, make sure you have a Vultr account \033[1mwith a valid payment method\033[0m.
Then go to https://my.vultr.com/settings/#settingsapi to get your API key.
In a Span shell, use this command to set API key:
    key
In this case, \033[7mLVGXWIIO6US43SR41U4KG3P552MHIDC5LURT\033[0m is your API key. Now try out the new command you have learnt!""")
    while 1:
        if (cmd := input('(tutorial) span\033[32m$\033[0m ')) == 'key':
            if getpass('API Key: ') == 'LVGXWIIO6US43SR41U4KG3P552MHIDC5LURT':
                print('\033[32mWell done!\033[0m')
                break
        elif cmd == '':
            print('\033[33mTask 1 skipped.\033[0m')
            break
        print('\033[33mPlease read task 1 carefully and try again.\033[0m')
    print("""\033[1;34m[Task 2]\033[0m Now set your beloved username for VPN connection, using this command:
    user <username> (e.g. `user john`)
In this case, \033[7madmin\033[0m will be your username.""")
    while 1:
        if (cmd := input('(tutorial) span\033[32m$\033[0m ')) == 'user admin':
            print('\033[32mWell done!\033[0m')
            break
        elif cmd == '':
            print('\033[33mTask 2 skipped.\033[0m')
            break
        print('\033[33mPlease read task 2 carefully and try again.\033[0m')
    print("""\033[1;34m[Task 3]\033[0m Now set a strong password for VPN connection, using this command:
    pwd
In this case, \033[7m3QJ2Mj2yCH98P8Lz\033[0m will be your password.""")
    while 1:
        if (cmd := input('(tutorial) span\033[32m$\033[0m ')) == 'pwd':
            while 1:
                tmp = getpass('Password: ')
                if tmp == '':
                    print('Error: Password cannot be empty.')
                    continue
                if tmp == getpass('Confirm Password: '):
                    break
                print('Error: Passwords do not match.')
            if tmp == '3QJ2Mj2yCH98P8Lz':
                print('\033[32mWell done!\033[0m')
                break
        elif cmd == '':
            print('\033[33mTask 3 skipped.\033[0m')
            break
        print('\033[33mPlease read task 3 carefully and try again.\033[0m')
    print("""\033[1;34m[Task 4]\033[0m Above are steps to initialize Span. Once you have finished those steps, there is no need to do it again, even if you reinstall Span.
It is time to introduce one of the most important commands. To create \033[1mand\033[0m setup a new instance, use this command:
    create <name> <region> <plan> (e.g. `create myinstance sjc vhp-1c-1gb-amd`)
You may be curious about where to find the region ID and plan ID. Use `regions` for a list of all regions and `plans` for a list of all plans (not included in the tutorial).
Supposing you would like to create a instance named \033[7mtest\033[0m in Singapore (whose ID is \033[7msgp\033[0m) with the plan \033[7mvhp-1c-1gb-intel\033[0m, try out the new command you have learnt.""")
    while 1:
        if (cmd := input('(tutorial) span\033[32m$\033[0m ')) == 'create test sgp vhp-1c-1gb-intel':
            print('\033[32mWell done!\033[0m')
            break
        elif cmd == '':
            print('\033[33mTask 4 skipped.\033[0m')
            break
        print('\033[33mPlease read task 4 carefully and try again.\033[0m')
    print(f"""\033[1;34m[Task 5]\033[0m Now you have a new instance named \033[7mtest\033[0m. However, in a real-world scenario, the creation process can be interrupted unexpectedly (by user, by network outage, etc.). If so, you can use `setup <name>` to setup an existing instance manually (not included in the tutorial).
For a list of all your instances, use `ls`; for information about a specific instance, use `info <name>` (e.g. `info myinstance`). Neither is included in the tutorial.
To connect VPNs created with Span, provide the following information to your VPN client:
    VPN Type: IKEv2
    Server Address: <instance_ip> (can be found via `info <name>`)
    Remote ID: <instance_ip>
    Authentication: Username
    Username: <username> (the one you set via `user <username>`)
    Password: <password> (the one you set via `pwd`)
Plus, you need to have Span VPN CA (at \033[7m{join(getcwd(), 'span.data', 'ca.cert.pem')}\033[0m) installed on your device.
The method of connecting VPNs varies from OS to OS. Please google if you are unclear about what to do.
Now, let's try deleting the instance we just created, using this command:
    del <name> (e.g. `del myinstance`)""")
    while 1:
        if (cmd := input('(tutorial) span\033[32m$\033[0m ')) == 'del test':
            print('\033[32mWell done!\033[0m')
            break
        elif cmd == '':
            print('\033[33mTask 5 skipped.\033[0m')
            break
        print('\033[33mPlease read task 5 carefully and try again.\033[0m')
    print("""\033[1;34m[Finished]\033[0m Congratulations! You have successfully completed the tutorial.
Type `help` whenever you forget the usage of a command, and `tutorial` to restart the interactive tutorial.
To exit Span gracefully, use `exit` or press Ctrl+D. That's all!
\033[33mYou have quit the tutorial.\033[0m""")
