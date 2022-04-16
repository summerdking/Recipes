from flask_app import app
from flask_app.controllers import users, recipes

if __name__ == "__main__":
    app.run(debug = True)



# pipenv install flask pymysql
# pipenv shell
# pipenv install werkzeug==2.0.3 flask==2.0.3 flask-bcrypt
# <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">