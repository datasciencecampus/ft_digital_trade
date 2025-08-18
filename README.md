# `repo_cookiecutter`

This is the suggested default template for ONS-fintrans repositories in following with best practice principles. This repository provides users with a quick and consistent way to develop projects that reduce set-up, onboarding, and development time.

The key features are consistent directory structures, simple documentation and AQA planning, pre-commit hooks to promote best practice and reduce data risk, and GIT integration as standard. For full overview please see below and other relevant read_me files under each project section. This is developed from the gov-cookiecutter basic template.

## Set-up
The set up instructions are important to ensure that you do not push data to the repository.

Git should only be used for code and not data, so code files including R files, R markdown files, python files and notebooks should be pushed. However, we need to ensure no data or graphs are included within commits. \
There are 2 ways in which data and charts can be commited to Git:
- Seperate files, for example .txt, .csv, .png etc.
- Within scripts, for example Notebooks etc.

### Git Ignore
Separate file management is done using a git ignore file in the repository. The git ignore file tells git to skip anything with certain file extensions. \
This repository has been created using the 'cookie cutter repo template', this means that a git ignore file already exists. \
**You should check the git ignore file contains all the types of data file in your project** \
If you require more file extensions to be ignored, these can be added within .gitignore

### Pre-commit hooks
Notebooks are a type of code file that allows you to view outputs, they contain information about these outputs. This information needs to be cleared before it is pushed to GitHub, this is done through Pre-commit hooks. \
This repository has been created using the 'cookie cutter repo template', therefore the pre-commit hooks are already setup, however they need to be "switched on". \
When this isn’t done, it will allow you to push notebooks to GitHub without clearing out the outputs.

#### Make pre-commit hooks
The following instructions should be followed to ensure pre-commit hooks are set up correctly:
These instructions need to be followed for every repository.

1) Clone the repository.

2) **IMPORTANT** Install Auto-setup pre-commit hooks by:
   - Opening the terminal
   - Type the following into the terminal to navigate to the correct directory:
```shell
 cd <repo_name>
```
   - Once in the correct directory type the following:

```shell
make pre_commit
```

3) Check pre commit hooks run when you push a commit. If you do not see a list of checks in the terminal, there may be a problem.

4) If you are unsure, create a notebook, create a graph using dummy data, run the notebook, push the changes to the repo. When you open GitHub in a browser you should only be able to see the code you created. If you can see the graph the setup is not correct.

### Create a virtual environment
It is strongly recommended that you create a new environment for each project, to avoid dependency issues. This is where the package requirements for the repo can be installed.

#### Create venv
The following instructions should be followed to create a virtual environment for a new repo using Python's venv:
1) Open the terminal
2) Type the following into the terminal to navigate to the root directory of the repo:
```shell
 cd <repo_name>
```
3) Once in the correct directory type the following:
```shell
 make venv
```

This will:
- create a venv in the new repo named after that repo
- Install the requirements.txt into that venv
- Install an ipykernel based on the new venv

#### Activate venv
If you want to install new packages into your virtual environment using `pip`, you have to activate it first. This has to be done every time a new terminal is opened. The terminal command to activate the venv is:
```shell
 source <venv_name>/bin/activate
```
#### Use correct kernel
In order to use your virtual environment in a jupyter notebook, a jupyter ipykernel is created. `make venv` automatically does this. You must select the correct kernel from the drop-down kernel list in jupyter lab.

#### Delete virtual environment
If you ever need to delete a virtual environment (for example, if something goes wrong and you want a fresh environment), do the following:
1) Open the terminal
2) Type the following into the terminal to navigate to the root directory of the repo:
```shell
 cd <repo_name>
```
3) Once in the correct directory type the following:
```shell
 make delete_venv
```
This will:
- delete the venv that is named after the repository (the default name when using `make venv`)
- delete the ipykernel associated to this venv


## Directory overview
- Data folder and all contents are untracked by GIT
- .gitignore default blocks popular data export file types due to data sensitivity
- Documents folder contains AQA plan, assumptions, caveats, project planning
- Notebooks stores notebooks
- Outputs stores outputs
- src for functions, modules, python scripts
- Use .env for consistent file paths
- Test for tests of src and coverage
- Secrets require .secrets and are not tracked by Git, see Secrets and credentials for more information

See /docs/structure/README.md for an overview of the project structure, and docs/contributor_guide/README.md for an overview on contributing for developers.

## Getting started

```{warning}
Where this documentation refers to the root folder we mean where this README.md is
located.
```

### Requirements

- Access to Google Cloud Platform, Vertex AI Notebooks, Google Big Query
- Permissions to access project datasets and personal notebook
- Python 3.6.1+ installed
- a `.secrets` file (if needed to manage credentials) with the needed secrets and credentials
- load environment variables from `.env`


## Loading environment variables

To load environment variables such as file paths from the `.env` hidden file you will need to use `dotenv` and `os` if using Python on windows.

1) Open your notebook and import modules
```python
from dotenv import load_dotenv
import os
```
2) Load `.env` file
```python
load_dotenv(override=True)
%env #returns all environment variables
```
3) Select the environment variable you require
```python
path_to_outputs = os.getenv("DIR_OUTPUTS")
print(path_to_outputs) #returns ./outputs
```

## Hidden Files & .Gitignore (if required)

For developers note that if using JuypterLabs that some files such as .gitignore are hidden by default. .Gitignore is set-up for both Python, R, and generally popular output methods. This limits the possibility to commit privileged data to Git through various filetypes but this is not a replacement for best practice.

These hidden files are accessed through GitHub or through changing JuypterLabs server config settings if required for individual users. This latter step is only recommended if developers require and is not recommended for standard or non-technical users. To enable hidden files:
1) To locate the jupyter config file, open the terminal and enter:
```shell
cd ~/.jupyter && nano jupyter_notebook_config.py
```
2) This will open the nano editor, under additional code at the bottom add this line
```shell
c.ContentsManager.allow_hidden = True
```
3) Press ctrl + O to save and hit enter to confirm the filename with agnostic file type saving. Press ctrl + x to exit.

4) Restart the notebook and kernels, any hidden . files will now be visible such as .secrets or .gitignore.

## Secrets and credentials (if required)

This is a recommended best practice to employ a `.secrets` file but may not be necessary for all projects where credential management is not required. For GCP Vertex AI Notebook work this step may be optional as credential management occurs at an earlier stage and external access is typically disallowed, users may wish to include project ID's and similar as secrets however.

To run this project, you need a `.secrets` file with secrets/credentials as environmental variables. The
secrets/credentials should have the following environment variable name(s):

| Secret/credential | Environment variable name | Description                                |
|-------------------|---------------------------|--------------------------------------------|
| Secret 1          | `SECRET_VARIABLE_1`       | Plain English description of Secret 1.     |
| Credential 1      | `CREDENTIAL_VARIABLE_1`   | Plain English description of Credential 1. |

Once added you can load these environment variables using `.env`. See docs/user_guide/loading_environment_variables.md for an overview.

## Loading secret variables (if required)

To load environment variables such as credentials from the `.secret` hidden file you will need to use `dotenv` and `os` if using Python on windows.

```{warning}
This is not the best practice solution and should be able to work without changing
directories or specifying the full directory similar to `.env` process.
Any contributions to fix this are welcome.
```

1) Create your `.secrets` file if it does not exist, open your terminal and type:
```shell
touch .secrets
```
2) Add your credentials into .secrets, this is untracked by GIT. Follow the format shown in Secrets and credentials (if required) section.

3) Open your notebook and import modules:
```python
from dotenv import load_dotenv
import os
```
2) Load `.secrets` file by either using the full file path or changing your directory to project root:
Using full file path:
```python
%pwd #this shows your full working directory, grab to the project root
load_dotenv("<full_directory_to_project_root>/.secrets", override=True)
%env #returns all environment variables
```

Alternatively change directory to root:
```python
#change directory to project root
cd ..
load_dotenv(".secrets", override=True)
%env #returns all environment variables
```
3) Select the environment variable you require
```python
my_secret = os.getenv("SECRET_1")
print(my_secret) #returns "yuki is a cute kitten"
```
