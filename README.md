<h1 align="center">OPEN ENDED LAB: 01</h1>
<p><strong>Create a python program that simulates secure login system for a web application should have following features:
<li>user registeration</li>
<li>password hashing</li>
<li>login authentication</li>
<li>session management</li>
</strong></p>

<h2>Explaination Of Code:</h2>
<p>Here is a quick explaination of code by which you will understand each and every line of code easily.</p>

<h4>Required Libraries for this program:</h4>

```py
import sqlite3
import hashlib
import os
import uuid
```


<b>sqlite3:</b>
<p>This module provides an interface to interact with SQLite databases in Python. It allows you to create, query, and modify SQLite database files.</p>
<b>hashlib:</b>
<p>This library contains cryptographic hashing functions. In this code, it's used to hash passwords before storing them in the database. Specifically, the sha256 algorithm is used to securely hash passwords.</p>
<b>os:</b>
<p>The os module provides a way to interact with the operating system. In this case, it's used to generate random salts (a random string used to secure passwords).</p>
<b>uuid:</b>
<p>This module generates universally unique identifiers (UUIDs). In this code, it's used to generate unique session tokens.</p>

<h4> Database Connection and Setup:</h4>

```py
conn = sqlite3.connect('secure_login_system.db')
cursor = conn.cursor()
```

sqlite3.connect('secure_login_system.db'):
This line establishes a connection to the SQLite database. The secure_login_system.db file is created in the current working directory if it doesn't already exist.
conn.cursor():
After connecting to the database, a cursor object is created using conn.cursor(). The cursor allows us to execute SQL queries (such as SELECT, INSERT, etc.) on the database.
