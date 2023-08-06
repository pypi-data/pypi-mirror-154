#!/usr/bin/python3

"""
This script will create the skeleton of a sepal-ui module

The script will extract the skeleton of a module from the sepal_ui_template GitHub repository. This template will be adapted based on the answsers to the questionnaire.
Placeholdre from the template will be replaced and the directory will be synced with a GitHub freshly created repository. Note that the repository need to be fully empty when the command is launched.
"""

import re
from pathlib import Path
import subprocess
import json
from distutils.util import strtobool
import argparse

from colorama import init, Fore

# init colors for all plateforms
init()

# init parser
parser = argparse.ArgumentParser(description=__doc__, usage="module_factory")


def set_default_readme(folder, module_name, description, url):
    """
    Write a default README.md file and overwrite the existing one.

    Args:
        folder (pathlib.Path): the module directory
        module_name (str): the module name used as title everywhere
        description (str): the description of the module
        url (str): the url of the module repository in GitHub
    """

    print("Write a default README.md file")

    license = f"{url}/blob/master/LICENSE"

    file = folder / "README.md"
    # write_text cannot handle append
    with file.open("w") as readme:
        readme.writelines(
            [
                f"# {module_name}\n",
                "\n",
                f"[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]({license})\n",
                "[![Black badge](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n",
                "\n",
                "# About\n",
                "\n",
                f"{description}\n",
            ]
        )

    return


def set_default_about(folder, description):
    """
    Write a default ABOUT.md file and overwrite the existing one

    Args:
        folder (pathlib.Path): the directory of the module
        description (str): the description of the module functions
    """

    print("Write a default ABOUT.md file")

    file = folder / "utils" / "ABOUT.md"

    with file.open("w") as about:
        about.write(f"{description}  \n")

    return


def set_module_name(folder, module_name):
    """
    Use the module name in the different translation dictionaries

    Args:
        folder (pathlib.Path): the directory of the module
        module_name (str): the module name
    """

    print("Update the module name in the json translation dictionaries")

    # loop in the available languages
    message_dir = folder / "component" / "message"
    json_files = [d / "locale.json" for d in message_dir.iterdir() if d.is_dir()]
    for file in json_files:

        with file.open("r") as f:
            data = json.load(f)

        data["app"]["title"] = module_name

        with file.open("w") as f:
            json.dump(data, f, indent=4)

    return


def set_contribute_file(folder, url, module_name):
    """
    Complete the contributing file with the appropriate informations

    Args:
        folder (pathlib.Path): the directory of the module
        url (str): the url of the GitHub repository
        module_name (str): the module name
    """

    print("Update the module name in the contribute file")

    contrib = folder / "CONTRIBUTE.md"

    with contrib.open() as f:
        data = f.read()

    data = data.replace("SEPAL_UI_TEMPLATE", module_name)
    data = data.replace("https://github.com/12rambau/sepal_ui_template.git", url)

    with contrib.open("w") as f:
        f.write(data)

    return


def set_module_name_doc(folder, url, module_name):
    """
    Set the module name in each documentation file and set the appropriate repository in the link

    Args:
        folder (pathlib.Path): the directory of the module
        url (str): the url of the GitHub repository
        module_name (str): the module name
    """

    # get the documentation folder
    doc_dir = folder / "doc"

    # loop in the available languages
    for file in doc_dir.glob("*.rst"):

        with file.open() as f:
            text = f.read()

        text = text.replace("Module_name", module_name)
        text = text.replace("===========", "=" * len(module_name))
        text = text.replace("https://github.com/12rambau/sepal_ui_template", url)

        with file.open("w") as f:
            f.write(text)
    return


def set_drawer_link(folder, url):
    """
    Replace the reference to the default repository to the one provided by the use

    Args:
        folder (pathlib.Path): the directory of the module
        url (str): the url of the GitHub repository
    """

    print("Update the drawers link with the new repository one")

    # get the ui file
    ui = folder / "ui.ipynb"

    # read the file
    with ui.open() as f:
        ui_content = f.read()

    # replace the target strings
    ui_content = ui_content.replace(
        "https://github.com/12rambau/sepal_ui_template", url
    )

    # write everything down again
    with ui.open("w") as f:
        f.write(ui_content)

    return


def main():

    # parse agruments
    parser.parse_args()

    # welcome the user
    print(f"{Fore.YELLOW}sepal-ui module factory{Fore.RESET}")

    print("Initializing module creation by setting up your module parameters")
    print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

    # ask the name of the module
    module_name = input(f"{Fore.CYAN}Provide a module name: \n{Fore.RESET}")
    if not module_name:
        raise Exception(f"{Fore.RED}A module name should be set")

    # set the module github URL
    github_url = input(
        f"{Fore.CYAN}Provide the URL of an empty github repository: \n{Fore.RESET}"
    )
    if not github_url:
        raise Exception(
            f"{Fore.RED}A module name should be set with an asociated github repository"
        )

    # ask for a short description
    description = input(
        f"{Fore.CYAN}Provide a short description for your module(optional): \n{Fore.RESET}"
    )

    # default to the default branch (obviously)
    branch = "default"

    # ask if the user need the default function
    default = input(
        f"{Fore.CYAN}Do you need to use the default function as a template [y]? \n{Fore.RESET}"
    )
    if not strtobool(default):
        branch = "no_default"

        # ask if the user need the aoi
        aoi = input(
            f"{Fore.CYAN}Do you need an AOI selector in your module (it will still be possible to add one afterward) [y]? \n{Fore.RESET}"
        )
        if not strtobool(aoi):
            branch = "no_aoi"

        else:

            gee = input(
                f"{Fore.CYAN}Do you need a connection to GEE in your module (it will still be possible to add one afterward) [y]? \n{Fore.RESET}"
            )
            if not strtobool(gee):
                branch = "no_gee"

    # adapt the name of the module to remove any special characters and spaces
    normalized_name = re.sub("[^a-zA-Z\d\-\_]", "_", module_name)

    print("Build the module init configuration")
    print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

    # clone the repository in a folder that has the normalized module name
    folder = Path.cwd() / normalized_name
    template_url = "https://github.com/12rambau/sepal_ui_template.git"
    subprocess.run(
        [
            "git",
            "clone",
            "--single-branch",
            "--branch",
            branch,
            template_url,
            str(folder),
        ],
        cwd=Path.cwd(),
    )

    # remove the .git folder
    subprocess.run(["rm", "rf", str(folder / ".git")], cwd=Path.cwd())

    # replace the placeholders
    url = github_url.replace(".git", "").replace(
        "git@github.com:", "https://github.com/"
    )

    set_default_readme(folder, module_name, description, url)
    set_default_about(folder, description)
    set_module_name(folder, module_name)
    set_drawer_link(folder, url)
    set_module_name_doc(folder, url, module_name)
    set_contribute_file(folder, url, module_name)

    # init the new git repository
    subprocess.run(["git", "init"], cwd=folder)

    # add the configuration of the git repository
    subprocess.run(["pre-commit", "install"], cwd=folder)

    # The dev version of black is used in sepal_ui_template so we cannot autoupdate yet
    # command = ["pre-commit", "autoupdate"]
    # res = subprocess.run(command, cwd=folder)

    # add all the files in the git repo
    subprocess.run(["git", "add", "."], cwd=folder)

    # first commit
    subprocess.run(["git", "commit", "-m", "first commit"], cwd=folder)

    # create a branch
    subprocess.run(["git", "branch", "-M", "master"], cwd=folder)

    # add the remote
    subprocess.run(["git", "remote", "set-url", "origin", str(github_url)], cwd=folder)

    # make the first push
    subprocess.run(["git", "push", "-u", "origin", "master"], cwd=folder)

    # create a release branch and push it to the server
    subprocess.run(["git", "checkout", "-b", "release"], cwd=folder)
    subprocess.run(["git", "push", "--set-upstream", "origin", "release"], cwd=folder)

    # checkout to master
    subprocess.run(["git", "checkout", "master"], cwd=folder)

    # exit message
    print(
        f"{Fore.YELLOW}Have a look to the git command executed in the process. if any of them is displaying an error, the final folder may not have been created{Fore.RESET}"
    )
    print(
        f"{Fore.YELLOW}If that's the case, delete the folder in your sepal instance (if there is any) and start the process again or contact us via github issues.{Fore.RESET}"
    )
    print(f"{Fore.GREEN}You created a new module named: {module_name}{Fore.RESET}")
    print(
        f"{Fore.GREEN}You can find its code in {folder} inside your sepal environment.{Fore.RESET}"
    )
    print()
    print("Let's code !")


if __name__ == "__main__":
    main()
