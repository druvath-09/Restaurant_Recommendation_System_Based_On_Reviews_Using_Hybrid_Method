CREATE DATABASE restaurant;
USE restaurant;
CREATE TABLE customer (
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15)
);
