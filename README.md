# TodoApp
 A Todo app made with flask, VueJS for WorkIndia assessment
 
### Clone the Repository
```
git clone git@github.com:karthik540/TodoApp.git
```

### Creating the Tables for MySQL
#### Execute the following sql queries on your MySql server
```
show databases;
```
```
create database deku;
```
```
use deku;
```
```
create table agent(
    agent_id INT NOT NULL AUTO_INCREMENT,
    password varchar(300),
    primary key(agent_id)
);
```
```
create table todo(
    id INT NOT NULL AUTO_INCREMENT,
    title varchar(50),
    description varchar(300),
    category varchar(50),
    due_date varchar(50),
    agent_id INT,
    primary key(id),
    FOREIGN KEY (agent_id) REFERENCES agent(agent_id)
);
```
### Installing the dependencies
```
pip install -r requirements.txt
```

### Running the server
```
python main.py
```
