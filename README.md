# Star Wars API Data Download

## Setup

- Install Python 3

- Setup python virtual environment from root directory

```bash
# install virtual env
pip install virtualenv

# create virtual environment
virtualenv venv

# activate virtual environment
source ./venv/bin/activate

# install packages
pip install -r requirements.txt
```

- docker / docker-compose is used for running postgres locally
    - [Download docker](https://docs.docker.com/desktop/#download-and-install)


## Running Locally

- Run docker compose from root directory

```bash
docker-compose down && docker-compose up
```

- Activate virtual environment

```bash
source ./venv/bin/activate
```

- Run application from root directory

```bash
python application.py
```

## Decisions
- I used docker and docker compose to run postgres database locally
- I used pip freeze to declare all dependencies in a requirements.txt, instead of installing packages individually

- Database design:

![ERD](./images/ERD.png)


## Verifying Results

"adminer" is a postgres client, and it is setup already inside docker-compose. It can be accessed thorugh [http://localhost:7000](http://localhost:7000)

Use the following credentails:

- User: starwars
- Password: stat
- Database: starwars

After running the application, three tables should be created:

![result_tables](./images/result_tables.png)

And the three tables should contain data:

![result_people_table](./images/result_people_table.png)

![result_starships_table](./images/result_starships_table.png)

![result_relation_table](./images/result_relation_table.png)
