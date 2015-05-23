Instructions
============

  - Copy etc/mongod.conf to <some magical path> (for example sake, I'm copying it to /opt/local/etc/mongodb/mongod.conf)
  - Start mongodb by passing in the <magical path> where your mongod.conf lives
    - `mongod -f /opt/local/etc/mongodb/mongod.conf --httpinterface --noauth`
  - Create geospatial indices
    - db.phones.ensureIndex({location:"2dsphere"})
  - `pip install -r requirements.txt`
  - python run.py
  - PROFIT
