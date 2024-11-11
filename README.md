# Hire2

Team MDROFI's Junction 2024 project. 

Reimagining job hunting in an engaging and productive way!
## Video Presentation

https://youtu.be/0EDKDWhR2Do

## Screenshots:

![image](https://github.com/user-attachments/assets/c88d4a6e-df5d-4375-9b2e-e8b89d5b6da4)

## Running our project

Dependencies:

- [Python](https://www.python.org/) (developed on Python 3.11)
- [pip](https://pip.pypa.io/en/stable/installation/)

1. Download the `master` branch of this repository. Alternatively, you can clone the repository and run `git checkout master`.
2. Open the *hackproj* folder in your IDE or command line.
3. Using the terminal of your IDE or command line, run `pip install -r requirements.txt`
4. Run the **app.py** file in your IDE or use the terminal command `python app.py`.

### Modifying models

If you modify the models (User, Job, Notification) in **app.py**, you need to run migrations. To do this run:

1. `flask db migrate`
2. `flask db upgrade`

If you delete the migrations and want to manually re-create needed migrations, you can run `flask db init`.

