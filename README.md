deploy on
https://3.21.241.51/

### Setup ###
- To connect to the database:
  - Install psql and in command line, run `psql 'postgres://postgres:ieqaBSdrnhRBOeuE3qo5@database-capstone-treatment.cns26sooon4s.ca-central-1.rds.amazonaws.com:5432/postgres?sslmode=require'`
  - OR:
    - From this repo, download pgConnect.json file
    - Install pgAdmin4
    - In pgAdmin4, click Tools -> Import/Export Servers
    - Import the downloaded json file
    - Click next and select all
    - Click finish
    - Enter password: ieqaBSdrnhRBOeuE3qo5