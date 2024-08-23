# Propus
Repository for Calbright's Shared Python functions and helpers

## Table of Contents
- [Propus](#propus)
  - [Table of Contents](#table-of-contents)
  - [What](#what)
  - [Project Structure](#project-structure)
  - [Development](#development)
  - [Example Usages](#example-usages)
    - [AWS](#aws)
      - [SSM](#ssm)
        - [get\_param](#get_param)
    - [PandaDoc](#pandadoc)
        - [Create and Send a Document From Template](#create-and-send-a-document-from-template)
    - [GSuite](#gsuite)
      - [Fetch Sheet and Update Cell](#fetch-sheet-and-update-cell)
      - [Upload GDrive File](#upload-gdrive-file)
      - [Delete GDrive File](#delete-gdrive-file)


## What
This repository is a collection of tools that can be used in downstream processes. For example, instead of writing an anthology student update method accross multiple repositories you can simply import this project and call the necessary method.

## Project Structure
```
.
├── calbright                           # Main Project Repository
|   └── anthology                      	# Anthology Student API Integrations
├── tests                       		# All unit testing code
└── tools                       		# All tools used for testing/linting/deployment
```

## Development

QuickStart:
```
$ virtualenv -p python3 env
$ source env/bin/activate
$ pip install -e .
```

## Example Usages

### AWS

#### SSM
##### get_param
```
>>> from propus.aws.ssm import AWS_SSM
>>> ssm = AWS_SSM.build()
>>> print(ssm.get_param("anthology.test", param_type="json")) # Automatically converts JSON to dict
{'url': 'SOME_URL', 'application_key': 'ApplicationKey APP_KEY_SECRET'}
>>> print(ssm.get_param("anthology.test"))
{"url": "SOME_URL", "application_key": "ApplicationKey APP_KEY_SECRET"} # Raw text without JSON conversion
```
### PandaDoc
##### Create and Send a Document From Template
```
def send_panda_doc_from_template():
    from propus.panda_doc import PandaDoc
    import time

    ssm = AWS_SSM.build()
    pd = PandaDoc.build(ssm.get_param("pandadoc.sandbox"))
    resp = pd.create_document_from_template(
        template_id="RE3qvebjrcVivnvJNBZ5qY",
        email_name="CSEP Document!!!!!",
        recipient_first_name="John",
        recipient_last_name="Doe",
        recipient_email="john.doe@calbright.org",
        tokens=[
            {"name": "Student.Name", "value": "John Doe"},
            {"name": "Student.CCCID", "value": "CCC_TEST_9876"},
            {
                "name": "Student.CalbrightEmail",
                "value": "john.doe@calbright.org",
            },
            {"name": "Student.ProgramName", "value": "IT Support"},
            {
                "name": "Student.ProgramCourses",
                "value": """IT Support\nWF500 - College and Career Essential Skills""",
            },
            {"name": "Student.ProgramIndustryCert", "value": "CompTIA A+"},
            {"name": "Student.StreetAddress", "value": "123 Main Street"},
            {"name": "Student.City", "value": "Sacramento"},
            {"name": "Student.State", "value": "CA"},
            {"name": "Student.ZipCode", "value": "95123"},
        ],
    )
    time.sleep(5) # If you send a document too quickly with PandaDoc it will error because it needs time to process
    pd.send_document(
        doc_id=resp.get("id"),
        subject="CSEP Sign Me!!",
        message="Please complete the CSEP document",
    )
```

### GSuite
#### Fetch Sheet and Update Cell
For this fetch/update the sheet must allow view/editor access to this role user: `gsheet-operator@avian-foundry-394219.iam.gserviceaccount.com`
```
def fetch_and_update_gsheet():
    from propus.gsuite import Sheets

    gsheet = Sheets.build(AWS_SSM.build().get_param("gsuite.svc-engineering.sheets", param_type="json"))
    sheet = gsheet.fetch_sheet(
        "https://docs.google.com/spreadsheets/d/<GSHEET_ID>"
    )
    gsheet.update_cell(sheet, "X", a1_notation="D2")
```

#### Upload GDrive File
Using the parameter from SSM, shown below, will use the svc-engineering role account Google Drive Account
```
def upload_file():
    from propus.gsuite import Drive

    # GDrive must read the credentials information from a file
    param = AWS_SSM.build().get_param("gsuite.svc-engineering")
    fname = "/gsuite_token_from_ssm.json"
    f = open(fname, "w")
    f.write(param)
    f.close()

    g_drive = Drive.build("file", fname)
    g_drive.upload_file(
        "<FULL_FILE_NAME>",
        {
            "title": "<TITLE_ON_GDRIVE>.pdf",
            "parents": [{"id": "1iy6jggaVy71epoDXoYIvMZM9iO7qKgue"}], # Folder Location ID
        },
    )
```

#### Delete GDrive File
Using the parameter from SSM, shown below, will use the svc-engineering role account Google Drive Account
```
def delete_file():
    from propus.gsuite import Drive

    # GDrive must read the credentials information from a file
    param = AWS_SSM.build().get_param("gsuite.svc-engineering")
    fname = "/gsuite_token_from_ssm.json"
    f = open(fname, "w")
    f.write(param)
    f.close()

    g_drive.delete_file("15QrP6CDAcjnvy9Dy4isVkqFdpmPvwzPJTzHy_tiqZ_Q") # GDrive Doc ID
```