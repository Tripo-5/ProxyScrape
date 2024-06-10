import paramiko

def create_ssh_client(server, user, password=None, key_filename=None):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, username=user, password=password, key_filename=key_filename)
    return client

def transfer_file(local_path, remote_path, server, user, password=None, key_filename=None):
    ssh = create_ssh_client(server, user, password, key_filename)
    sftp = ssh.open_sftp()
    sftp.put(local_path, remote_path)
    sftp.close()
    ssh.close()

if __name__ == "__main__":
    server = 'machine_b_ip'
    user = 'username_on_machine_b'
    local_path = 'live_proxies.txt'
    remote_path = '/path/to/destination/live_proxies.txt'

    transfer_file(local_path, remote_path, server, user, key_filename='/path/to/private/key')
