#!/bin/bash
mongoimport -d projects -c projects /tmp/database.json --jsonArray
mongoimport -d users -c users /tmp/users.json --jsonArray