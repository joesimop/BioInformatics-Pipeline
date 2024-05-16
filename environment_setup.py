def setup_env():
    import os, sys

    root_dir = os.getenv("BI_PIPELINE")

    if not root_dir:
        print("Please set the BI_PIPELINE environment variable to the root directory of the pipeline")
        sys.exit(1)
    
    user = os.getenv("USER")

    if not user:
        user = os.getenv("USERNAME")
        if not user:
            user = input("Could not find user, please enter a user to store the pipeline under: ")
    
    return f"{root_dir}/{user}"
