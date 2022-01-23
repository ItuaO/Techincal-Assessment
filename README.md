# Techical Assessment

## Setup + Installation:
Complete the setup described on this page to configure and run this program.

### Prerequisites:

- Python Version = 3.9.6
- Access to the internet and a web browser in order to authorize

### Step 1: Get the code

Clone the git repository at [https://github.com/ItuaO/Techincal-Assessment](https://github.com/ItuaO/Techincal-Assessment)

### Step 2: Setup Credentials

Move your credentials file (https://cloud.google.com/docs/authentication) into the same directory as the cloned repo. Rename your file if necessary to "credentials.json"


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

pip install -r requirements.txt

## Files

runassessments.py: main script file to run assessments 1-3.

Google.py: sets up authentication and the google drive service.

assessments.py: class object for assessments containg the methods.

requirements.txt: required packages to run program

readme.md: information about the program



```bash
pip install foobar
```

## Usage
runassessments.py leverages the assessments class to run assessments 1-3

```python
from assessment import assessment

#authenticates user and instantiates class
myassessment = assessment()

source_folder = "1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V"

#https://drive.google.com/drive/folders/1iM-wF0npATGCubWwQtb6bhpWisCNx5Jl
destination_folder = "1iM-wF0npATGCubWwQtb6bhpWisCNx5Jl"

#generates a timestamped report in the cwd with the number of
#files and folders in source dir
myassessment.assessment1(source)

#generates a timestamped report in the cwd with the number of
#files and folders for each folder under the source folder
myassessment.assessment2(source)

#Copies content from google drive source folder
#to google drive destination folder. Maintains directory structure,
#files and folder attributes excluding parent and
#file/folder ids
myassessment.assessment3(source_folder,destination_folder)
```
