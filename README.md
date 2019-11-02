Oil Analysis
===

This project includes a comprehensive platform for providing oil information from data fetching to information analysis.

The project can be mainly devided into 4 parts:
1. Data collection
2. Database
3. Flask back end + price analysis
3. Web-based front end

Prerequisite
---
1. Python 3.6 or above
2. MySQL

Optional for web deployment:
1. Apache
2. [Flask WSGI](http://flask.palletsprojects.com/en/1.1.x/deploying/mod_wsgi/) 

Recommended Software for development:
1. PyCharm
2. DataGrip

Installation
---

#### Installing MySQL db in macOS:

we strongly recommend using [homebrew](https://brew.sh) in installing mysql for the project since it is easy to use and easy to install.


```bash
brew install mysql
brew services start mysql
```

#### Installing MySQL in Linux:

skipped

#### Preparing MySQL user:

In mysql console, type: (usually accessed by `mysql -uroot -p`)
```mysql
CREATE USER 'oil'@'localhost' IDENTIFIED BY 'h1VHhQWour';
GRANT ALL PRIVILEGES ON *.* TO 'oil'@'localhost';
```

#### Preparing schema:

In mysql console, type:
```mysql
CREATE SCHEMA oil_analysis_test;  # test database
CREATE SCHEMA oil_analysis; # production database
```

### Preparing python prerequisites

at root of the project:

```bash
pip3 install -r requirements.txt
```

#### Preparing tables:

at root of the project:

```
python3 -m BackEnd.initialize_database
```

#### Preparing data:

In mysql console, type:
```mysql
source project/absolute/path/sample_data/news.sql
source project/absolute/path/sample_data/oilprice1_category.sql
source project/absolute/path/sample_data/oilprice2_indice.sql
source project/absolute/path/sample_data/oilprice3.sql
```


Using BackEnd API
---

api package and errors package are automatically included when doing:

```python
from BackEnd import *
```

