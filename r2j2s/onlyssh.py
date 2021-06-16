import paramiko

# ----------------------------------------------------------
IP_ADDRESS = '192.168.1.1'
USER_NAME = 'admin'
PWD = "admin"
CMD = 'sudo -S qmicli -d /dev/cdc-wdm1 --nas-get-signal-strength'
# ----------------------------------------------------------

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(IP_ADDRESS,
               username=USER_NAME,
               password=PWD,
               timeout=10.0)

stdin, stdout, stderr = client.exec_command(CMD)

stdin.write('admin\n')
stdin.flush()

cmd_result = ''
for line in stdout:
    cmd_result += line
print(cmd_result)

client.close()
del client, stdin, stdout, stderr
