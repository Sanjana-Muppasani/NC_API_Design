## Project Setup 

### Database Setup 
Start by creating the database and seeding it
```
psql -f db/setup.sql
```
Populate the database with 
```
python db/seed.py
``` 
NOTE to devs: ```.env.example``` file contains the details to enter into local .env to connect to the database 


### Test set up
Create the test database and seed it

```
psql -f db/test_setup.sql
```
Run pytest
```
pytest
```



