-- Schema for web98 Facebook-style clone (MySQL 3.23 compatible)
CREATE DATABASE IF NOT EXISTS lovelink;
USE lovelink;

CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(32) NOT NULL,
  full_name VARCHAR(64) NOT NULL,
  email VARCHAR(96) NOT NULL,
  password_md5 CHAR(32) NOT NULL,
  bio TEXT,
  hometown VARCHAR(64),
  photo_url VARCHAR(128),
  created_at DATETIME NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uname (username),
  UNIQUE KEY email (email)
) TYPE=MyISAM;

CREATE TABLE sessions (
  id CHAR(32) NOT NULL,
  user_id INT NOT NULL,
  expires_at DATETIME NOT NULL,
  PRIMARY KEY (id),
  KEY user_idx (user_id)
) TYPE=MyISAM;

CREATE TABLE posts (
  id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  body TEXT NOT NULL,
  created_at DATETIME NOT NULL,
  PRIMARY KEY (id),
  KEY user_idx (user_id)
) TYPE=MyISAM;

CREATE TABLE friendships (
  id INT NOT NULL AUTO_INCREMENT,
  requester_id INT NOT NULL,
  addressee_id INT NOT NULL,
  status ENUM('pending','accepted') NOT NULL DEFAULT 'pending',
  created_at DATETIME NOT NULL,
  PRIMARY KEY (id),
  KEY req_idx (requester_id),
  KEY add_idx (addressee_id)
) TYPE=MyISAM;

CREATE TABLE messages (
  id INT NOT NULL AUTO_INCREMENT,
  sender_id INT NOT NULL,
  recipient_id INT NOT NULL,
  body TEXT NOT NULL,
  created_at DATETIME NOT NULL,
  is_read TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY to_idx (recipient_id)
) TYPE=MyISAM;

-- Seed users
INSERT INTO users (username, full_name, email, password_md5, bio, hometown, photo_url, created_at) VALUES
('zuck', 'Mark Elliot', 'mark@example.com', MD5('password'), 'Harvard sophomore; building cool stuff.', 'Dobbs Ferry, NY', 'img/zuck.jpg', NOW()),
('eduardo', 'Eduardo Saverin', 'eduardo@example.com', MD5('password'), 'I like growth graphs and chess.', 'Miami, FL', 'img/eduardo.jpg', NOW()),
('dustin', 'Dustin Moskovitz', 'dustin@example.com', MD5('password'), 'Bike commuter; hacking on PHP.', 'Gainesville, FL', 'img/dustin.jpg', NOW()),
('chris', 'Chris Hughes', 'chris@example.com', MD5('password'), 'Campus media guy; always online.', 'Hickory, NC', 'img/chris.jpg', NOW()),
('sheryl', 'Sheryl Sandberg', 'sheryl@example.com', MD5('password'), 'Ops brain. Loves efficiency.', 'North Miami Beach, FL', 'img/sheryl.jpg', NOW());

-- Seed friendships (accepted)
INSERT INTO friendships (requester_id, addressee_id, status, created_at) VALUES
(1,2,'accepted',NOW()), (2,1,'accepted',NOW()),
(1,3,'accepted',NOW()), (3,1,'accepted',NOW()),
(1,4,'accepted',NOW()), (4,1,'accepted',NOW());

-- Seed posts
INSERT INTO posts (user_id, body, created_at) VALUES
(1, 'Just launched our campus facebook. Tell me what you think!', DATE_SUB(NOW(), INTERVAL 2 DAY)),
(2, 'Met with Mark about monetization ideas.', DATE_SUB(NOW(), INTERVAL 1 DAY)),
(3, 'Pulled an all-nighter writing PHP3. Need sleep.', DATE_SUB(NOW(), INTERVAL 12 HOUR)),
(4, 'Interviewing editors for the site. Any leads?', DATE_SUB(NOW(), INTERVAL 6 HOUR));

-- Seed messages
INSERT INTO messages (sender_id, recipient_id, body, created_at, is_read) VALUES
(2,1,'We should add photo upload soon.', DATE_SUB(NOW(), INTERVAL 1 DAY),0),
(1,2,'Agree. Need mod_perl or fastcgi to scale?', DATE_SUB(NOW(), INTERVAL 23 HOUR),0);
