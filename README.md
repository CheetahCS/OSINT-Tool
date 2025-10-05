# OSINT-Tool

A command-line OSINT tool designed to retrieve and present public information.

## Current functionality

* Takes an email as input and queries the Xposedornot api to identify if the provided email was in a data breach. It then displays it in a readable format in the terminal and makes a json copy of the information found in the the data folder (email_info.json)

## Planned functionality

* Given a username or email identify social media accounts with those details

* Utilise AI to provide a precise threat summary

* Utilise Machine learning to be able to identify and verify social medial accounts

## Usage

To use this tool, you will need Python 3.8+ and Git installed on your system.

### 1. Installation

First, clone the repository to your local machine and navigate into the project directory:

```bash
git clone https://github.com/CheetahCS/OSINT-Tool.git
cd OSINT-Tool/OSINT-Tool

pip install .
```
### 2. Usage

Now, run the following command with the desired email to get information on breaches associated with that email

```bash
python3 main.py --target SomeTarget --email example@gmail.com
```