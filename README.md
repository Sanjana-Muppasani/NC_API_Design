## Project Setup 

### Database Setup 
Start by creating the database and seeding it
```
psql -f db/setup.sql
```
Populate the database by with 
```
python db/seed.py
``` 
NOTE to devs: ```.env.example``` file contains the details to enter into local .env to connect to the database 





