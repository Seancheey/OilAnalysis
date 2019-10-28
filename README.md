Oil Analysis
===

This project includes a comprehensive platform for providing oil information from data fetching to information analysis.

The project can be mainly devided into 4 parts:
1. Data collection
2. Database Back End
3. Web Front End
4. Information clustering and regression

Prerequisite
---
Python 3.6 or above


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

In mysql console, type: (usually accessed by `mysql -uroot`)
```mysql
CREATE USER 'oil'@'localhost' IDENTIFIED BY 'h1VHhQWour';
GRANT ALL PRIVILEGES ON *.* TO 'oil'@'localhost';
```

#### Preparing schema:

In mysql console, type:
```mysql
CREATE SCHEMA test;  # test database
CREATE SCHEMA oil_analysis; # production database
```

#### Preparing tables:

at root of project:

```
python3 -m python3 -m BackEnd.initialize_database
```

Using BackEnd
---

Import API's by simply:

```python
from BackEnd import *
```

