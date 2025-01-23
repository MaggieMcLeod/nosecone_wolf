import time
import paramiko
from scp import SCPClient

# host1 = 'raspberrypi.local'
# port = 22
# username1 = 'pi'
# password1 = 'raspberry'

def execute_ssh_command(host, port, username, password, keyfilepath, keyfiletype, command):
    """
    execute_ssh_command(host, port, username, password, keyfilepath, keyfiletype, command) -> tuple

    Executes the supplied command by opening a SSH connection to the supplied host
    on the supplied port authenticating as the user with supplied username and supplied password or with
    the private key in a file with the supplied path.
    If a private key is used for authentication, the type of the keyfile needs to be specified as DSA or RSA.
    :rtype: tuple consisting of the output to standard out and the output to standard err as produced by the command
    """
    ssh = None
    key = None
    try:
        if keyfilepath is not None:
            if keyfiletype == 'DSA':
                key = paramiko.DSSKey.from_private_key_file(keyfilepath)
            else:
                key = paramiko.RSAKey.from_private_key(keyfilepath)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key is not None:
            ssh.connect(host, port, username, None, key)
        else:
            ssh.connect(host, port, username, password)
        stdin, stdout, stderr = ssh.exec_command(command)
        while not stdout.channel.exit_status_ready() and not stdout.channel.recv_ready():
            time.sleep(1)
        stdoutstring = stdout.readlines()
        stderrstring = stderr.readlines()
        return stdoutstring, stderrstring
    finally:
        if ssh is not None:
            ssh.close()

def scp_get_image(host, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port, user, password)
    scp = SCPClient(client.get_transport())
    scp.get("/home/"+user+"/scripts/image.jpg", "/home/raspi/Desktop")
    scp.close()
    client.close()

def scp_get_video(host, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port, user, password)
    scp = SCPClient(client.get_transport())
    scp.get("/home/"+user+"/scripts/video.h264", "/home/raspi/Desktop")
    scp.close()
    client.close()
            
class camera_control:

    def __init__(self) -> None:

        self.port = 22
        self.CAMERA_HOST_INFO = [("raspberrypi.local", "pi", "raspberry")]

        for cameraNum in range(self.CAMERA_HOST_INFO):
            execute_ssh_command(self.CAMERA_HOST_INFO[cameraNum][0], self.port, self.CAMERA_HOST_INFO[cameraNum][1], self.CAMERA_HOST_INFO[cameraNum][2], None, None, "python scripts/control.py")

    def start_recording(self, cameraNum:int = -1):
        
        if cameraNum == -1:
            for cn in self.CAMERA_HOST_INFO:
                execute_ssh_command(self.CAMERA_HOST_INFO[cn][0], self.port, self.cn[cameraNum][1], self.cn[cameraNum][2], None, None, "touch scripts/record.txt")
        else:
            execute_ssh_command(self.CAMERA_HOST_INFO[cameraNum][0], self.port, self.CAMERA_HOST_INFO[cameraNum][1], self.CAMERA_HOST_INFO[cameraNum][2], None, None, "touch scripts/record.txt")

    def stop_recording(self, cameraNum:int = -1):
        
        if cameraNum == -1:
            for cn in self.CAMERA_HOST_INFO:
                execute_ssh_command(self.CAMERA_HOST_INFO[cn][0], self.port, self.cn[cameraNum][1], self.cn[cameraNum][2], None, None, "rm scripts/record.txt")
                scp_get_video(self.CAMERA_HOST_INFO[cn][0], self.port, self.cn[cameraNum][1], self.cn[cameraNum][2])
        else:
            execute_ssh_command(self.CAMERA_HOST_INFO[cameraNum][0], self.port, self.CAMERA_HOST_INFO[cameraNum][1], self.CAMERA_HOST_INFO[cameraNum][2], None, None, "rm scripts/record.txt")
            scp_get_video(self.CAMERA_HOST_INFO[cameraNum][0], self.port, self.CAMERA_HOST_INFO[cameraNum][1], self.CAMERA_HOST_INFO[cameraNum][2])

    def take_picture(self, cameraNum:int = -1):

        if cameraNum == -1:
            for cn in self.CAMERA_HOST_INFO:
                execute_ssh_command(self.CAMERA_HOST_INFO[cn][0], self.port, self.cn[cameraNum][1], self.cn[cameraNum][2], None, None, "touch scripts/picture.txt")
                scp_get_image(self.CAMERA_HOST_INFO[cn][0], self.port, self.cn[cameraNum][1], self.cn[cameraNum][2])
        else:
            execute_ssh_command(self.CAMERA_HOST_INFO[cameraNum][0], self.port, self.CAMERA_HOST_INFO[cameraNum][1], self.CAMERA_HOST_INFO[cameraNum][2], None, None, "touch scripts/picture.txt")
            scp_get_image(self.CAMERA_HOST_INFO[cameraNum][0], self.port, self.CAMERA_HOST_INFO[cameraNum][1], self.CAMERA_HOST_INFO[cameraNum][2])