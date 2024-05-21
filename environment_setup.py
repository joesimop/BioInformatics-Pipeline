def setup_env():
    import os, sys

    root_dir = os.getenv("BI_PIPELINE")

    if not root_dir:
        root_dir = "/Users/joesimop/Desktop/Classes/BI_Pipeline"
        # print("Please set the BI_PIPELINE environment variable to the root directory of the pipeline")
        # sys.exit(1)
    
    user = os.getenv("USER")

    if not user:
        user = os.getenv("USERNAME")
        if not user:
            user = input("Could not find user, please enter a user to store the pipeline under: ")

    #Check fo user directory and create if it doesn't exist
    if not os.path.exists(f"{root_dir}/{user}"):
        os.mkdir(f"{root_dir}/{user}")
        os.mkdir(f"{root_dir}/{user}/pipelines")
        os.mkdir(f"{root_dir}/{user}/data")
    
    return root_dir, f"{root_dir}/{user}"

program_root, user_root = setup_env()
