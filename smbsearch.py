from impacket.smbconnection import SMBConnection
import getpass

def search_smb_share(server, share, file_patterns):
    try:
        # Attempt anonymous login
        conn = SMBConnection(server, server)
        conn.login('', '')
        print("Successfully connected anonymously")
        find_files(conn, share, file_patterns)
    except Exception as e:
        print(f"Anonymous login failed: {e}")
        # Prompt for username, password, or hash
        username = input("Enter username: ")
        password = getpass.getpass("Enter password (leave empty if using NTLM hash): ")
        lmhash = ""
        nthash = ""
        if not password:
            nthash = input("Enter NTLM hash: ")

        try:
            conn = SMBConnection(server, server)
            conn.login(username, password, lmhash, nthash)
            print("Successfully connected with provided credentials")
            find_files(conn, share, file_patterns)
        except Exception as e:
            print(f"Login failed: {e}")

def find_files(conn, share, file_patterns):
    try:
        search_path = '\\'
        search_files_recursive(conn, share, search_path, file_patterns)
    except Exception as e:
        print(f"Error finding files: {e}")

def search_files_recursive(conn, share, path, file_patterns):
    try:
        files = conn.listPath(share, path + '*')
        for file in files:
            file_name = file.get_longname()
            if file.is_directory() and file_name not in ['.', '..']:
                search_files_recursive(conn, share, path + file_name + '\\', file_patterns)
            elif any(file_name.endswith(pattern) for pattern in file_patterns):
                print(f"Found file: {path + file_name}")
    except Exception as e:
        print(f"Error accessing path {path}: {e}")

if __name__ == "__main__":
    server = input("Enter the SMB server IP or hostname: ")
    share = input("Enter the share name: ")
    file_patterns = input("Enter the file patterns to search for (comma-separated, e.g., .kdbx,.txt,.log): ").split(',')
    search_smb_share(server, share, file_patterns)
