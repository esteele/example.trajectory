
## Setting up the database

Start the PostgreSQL interactive terminal using
```
psql -U postgres
```

And then create the example user, giving it the permissions required to create new databases.

> CREATE USER example WITH PASSWORD 'example!';
> ALTER USER example CREATEDB;
```

The initialization code will take care of creating the database itself.