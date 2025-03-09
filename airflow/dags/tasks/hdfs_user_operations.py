from airflow.providers.apache.hdfs.hooks.webhdfs import WebHDFSHook

def create_and_manage_user_hdfs_directory(username: str, folder: str, proxy_user: str='root'):
    """
    Creates an HDFS directory and sets ownership and permissions.

    :param username: The username for the HDFS directory.
    :param folder: The folder to be created inside the user's HDFS directory.
    :param proxy_user: The proxy user to connect with WebHDFS.
    """
    hdfs_hook = WebHDFSHook(webhdfs_conn_id='hdfs_default', proxy_user=proxy_user)
    hdfs_client = hdfs_hook.get_conn()

    # Define HDFS path
    folder_path = f"/user/{username}/{folder}"

    # Check if the directory already exists
    if not hdfs_hook.check_for_path(folder_path):
        # Create the directory
        hdfs_client.makedirs(folder_path)
        print(f"Created directory: {folder_path}")
    else:
        print(f"Directory already exists: {folder_path}")

    parts = folder_path.split('/')
    paths = ['/'.join(parts[:i+1]) for i in range(2, len(parts))]

    for path in paths:
        hdfs_client.set_owner(path, owner=username, group="supergroup")
        hdfs_client.set_permission(path, permission=770) 
