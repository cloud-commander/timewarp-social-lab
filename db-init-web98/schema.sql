-- Schema for web98 Facebook-style clone (MySQL 3.23 compatible)
CREATE DATABASE IF NOT EXISTS lovelink;
USE lovelink;

CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(32) NOT NULL,
  full_name VARCHAR(64) NOT NULL,
  email VARCHAR(96) NOT NULL,
  password_md5 CHAR(32) NOT NULL,
  school VARCHAR(64) DEFAULT 'Harvard University',
  class_year SMALLINT,
  dorm VARCHAR(64),
  concentration VARCHAR(64),
  gender ENUM('Male','Female','Other','Prefer not to say') DEFAULT 'Prefer not to say',
  status ENUM('Single','In a relationship','Engaged','Married','Rather not say') DEFAULT 'Rather not say',
  looking_for SET('Friendship','Dating','Networking') DEFAULT 'Friendship',
  phone VARCHAR(32),
  birthday DATE,
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
INSERT INTO users (username, full_name, email, password_md5, school, class_year, dorm, concentration, gender, status, looking_for, phone, birthday, bio, hometown, photo_url, created_at) VALUES
('zuck', 'Mark Zuckerberg', 'mark@harvard.edu', MD5('password'), 'Harvard University', 2006, 'Kirkland House', 'Computer Science', 'Male', 'Single', 'Friendship,Dating', '617-555-0101', '1984-05-14', 'Harvard sophomore; building thefacebook.', 'Dobbs Ferry, NY', 'img/zuck.jpg', NOW()),
('eduardo', 'Eduardo Saverin', 'eduardo@harvard.edu', MD5('password'), 'Harvard University', 2006, 'Eliot House', 'Economics', 'Male', 'Single', 'Friendship,Networking', '617-555-0102', '1982-03-19', 'I like growth graphs and chess.', 'Miami, FL', 'img/eduardo.jpg', NOW()),
('dustin', 'Dustin Moskovitz', 'dustin@harvard.edu', MD5('password'), 'Harvard University', 2006, 'Eliot House', 'Economics', 'Male', 'Single', 'Friendship', '617-555-0103', '1984-05-22', 'Bike commuter; hacking CGI at 2am.', 'Gainesville, FL', 'img/dustin.jpg', NOW()),
('chris', 'Chris Hughes', 'chris@harvard.edu', MD5('password'), 'Harvard University', 2006, 'Kirkland House', 'History', 'Male', 'Single', 'Friendship', '617-555-0104', '1983-11-26', 'Campus media guy; always online.', 'Hickory, NC', 'img/chris.jpg', NOW()),
('sheryl', 'Sheryl Sandberg', 'sheryl@harvard.edu', MD5('password'), 'Harvard University', 1991, 'Eliot House', 'Economics', 'Female', 'Married', 'Networking', '617-555-0105', '1969-08-28', 'Ops brain. Loves efficiency.', 'North Miami Beach, FL', 'img/sheryl.jpg', NOW());

-- Seed friendships (accepted)
INSERT INTO friendships (requester_id, addressee_id, status, created_at) VALUES
(1,2,'accepted',NOW()), (2,1,'accepted',NOW()),
(1,3,'accepted',NOW()), (3,1,'accepted',NOW()),
(1,4,'accepted',NOW()), (4,1,'accepted',NOW());

-- Seed posts
INSERT INTO posts (user_id, body, created_at) VALUES
(1, 'Just launched thefacebook for campus. Tell me what you think!', DATE_SUB(NOW(), INTERVAL 2 DAY)),
(2, 'Met with Mark about monetization ideas.', DATE_SUB(NOW(), INTERVAL 1 DAY)),
(3, 'Pulled an all-nighter wiring CGI + MySQL. Need sleep.', DATE_SUB(NOW(), INTERVAL 12 HOUR)),
(4, 'Interviewing editors for the site. Any leads?', DATE_SUB(NOW(), INTERVAL 6 HOUR));

-- Seed messages
INSERT INTO messages (sender_id, recipient_id, body, created_at, is_read) VALUES
(2,1,'We should add photo upload soon.', DATE_SUB(NOW(), INTERVAL 1 DAY),0),
(1,2,'Agree. Need mod_perl or fastcgi to scale?', DATE_SUB(NOW(), INTERVAL 23 HOUR),0);
