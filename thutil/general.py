import logging
import subprocess


def create_logger(
    logger_name: str = None,
    log_file: str = None,
    level: str = "INFO",
    level_logfile: str = None,
    format_="info",
) -> logging.Logger:
    ### ref: https://realpython.com/python-logging/#using-handlers
    """Create a logger"""
    # c_: means console; f_: means file

    ### Define variables
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    c_level = level_map.get(level)
    f_level = level_map.get(level_logfile) if level_logfile else c_level

    format_map = {
        "debug": "%(name)s - %(levelname)s: %(message)s | %(funcName)s:%(lineno)d",
        "info": "%(name)s - %(levelname)s: %(message)s",
        "file": "%(asctime)s | %(name)s - %(levelname)s: %(message)s",
    }

    format_console = format_map[format_]
    format_file = format_map["file"]

    ### Create a console logger
    if logger_name:
        logger_name = logger_name
    elif __file__:
        logger_name = __file__
    else:
        logger_name = __name__
    logger = logging.getLogger(logger_name)
    logger.setLevel(c_level)  # to show log in jupyter notebook

    # Create handlers
    c_handler = logging.StreamHandler()
    c_handler.setLevel(c_level)

    # Create formatters and add it to handlers
    c_format = logging.Formatter(format_console)
    c_handler.setFormatter(c_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)

    ### Add a file handler
    if log_file:
        f_handler = logging.FileHandler(log_file, mode="w")
        f_handler.setLevel(f_level)
        f_format = logging.Formatter(format_file, "%Y-%m-%d %H:%M:%S")
        f_handler.setFormatter(f_format)
        logger.addHandler(f_handler)

    return logger


def check_installation(
    package_name: str,
    git_repo: str = None,
    auto_install: bool = False,
    extra_commands: list[str] = None,
) -> None:
    """Check if the required packages are installed"""
    try:
        __import__(package_name)
    except ImportError:
        if auto_install:
            _install_package(package_name, git_repo)
            if extra_commands:
                for command in extra_commands:
                    subprocess.run(command, check=True)
        else:
            raise ImportError(
                f"Required package `{package_name}` is not installed. Please install the package.",
            )


def _install_package(package_name: str, git_repo: str = None) -> None:
    """Install the required package

    Args:
    ----
        package_name (str): package name
        git_repo (str): git path for the package

    """
    from .general_utils import create_logger

    logger = create_logger()

    try:
        logger.info(f"Installing the required packages: `{package_name}` ...")
        if git_repo:
            command = f"pip install -U git+{git_repo}"
        else:
            command = f"pip install -U {package_name}"

        subprocess.run(command, check=True)

        logger.info("Installation successful!")

    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred while installing the package: {e}")