echo \
"DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS stash;
CREATE TABLE users (
    username VARCHAR(35) UNIQUE NOT NULL,
    password VARCHAR(35) NOT NULL
);
CREATE TABLE stash (
    user INT NOT NULL,
    text TEXT
);


INSERT INTO users VALUES ('admin', '$FLAG1'); 
INSERT INTO stash (user, text) VALUES (1, '$FLAG1');
;" | /usr/bin/sqlite3 /tmp/my.db
chmod 777 /tmp/my.db
/usr/sbin/apachectl -D FOREGROUND