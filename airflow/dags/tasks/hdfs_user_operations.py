from airflow.providers.apache.hdfs.hooks.webhdfs import WebHDFSHook

def create_and_manage_user_hdfs_directory(username: str, proxy_user: str='root'):
    """
    Creates an HDFS directory and sets ownership and permissions.

    :param username: The username for the HDFS directory.
    """
    hdfs_hook = WebHDFSHook(webhdfs_conn_id='hdfs_default', proxy_user=proxy_user)
    hdfs_client = hdfs_hook.get_conn()

    # Define HDFS path
    hdfs_path = f"/user/{username}"

    # Check if the directory already exists
    if not hdfs_hook.check_for_path(hdfs_path):
        # Create the directory
        hdfs_client.makedirs(hdfs_path)
        print(f"Created directory: {hdfs_path}")
    else:
        print(f"Directory already exists: {hdfs_path}")

    # Set ownership
    hdfs_client.set_owner(hdfs_path, owner=username, group="supergroup")
    print(f"Ownership set to {username}:supergroup for {hdfs_path}")

    # Set permissions
    hdfs_client.set_permission(hdfs_path, permission=0o777)  # 777 in octal
    print(f"Permissions set to 777 for {hdfs_path}")
