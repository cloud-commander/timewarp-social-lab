-- LoveLink 2000 Schema
-- Compatible with MySQL 3.23

CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  password VARCHAR(32) NOT NULL, -- MD5 hash
  age INT,
  gender CHAR(1), -- 'M' or 'F'
  bio VARCHAR(255),
  last_active INT, -- Unix timestamp
  created_at INT, -- Unix timestamp
  PRIMARY KEY (id),
  UNIQUE (username)
);

CREATE TABLE user_photos (
  id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  filename VARCHAR(255) NOT NULL,
  is_primary TINYINT(1) DEFAULT 0,
  PRIMARY KEY (id)
);

CREATE TABLE likes (
  from_user_id INT NOT NULL,
  to_user_id INT NOT NULL,
  action VARCHAR(10) NOT NULL, -- 'pass' or 'date'
  timestamp INT,
  PRIMARY KEY (from_user_id, to_user_id)
);

CREATE TABLE matches (
  user_id_1 INT NOT NULL,
  user_id_2 INT NOT NULL,
  timestamp INT,
  PRIMARY KEY (user_id_1, user_id_2)
);

CREATE TABLE messages (
  id INT NOT NULL AUTO_INCREMENT,
  match_id VARCHAR(50) NOT NULL, -- Composite key string "min_id-max_id" or similar logic, or just rely on sender/receiver query
  sender_id INT NOT NULL,
  receiver_id INT NOT NULL,
  body VARCHAR(160),
  timestamp INT,
  PRIMARY KEY (id)
);

CREATE TABLE blocks (
  user_id INT NOT NULL,
  blocked_user_id INT NOT NULL,
  timestamp INT,
  PRIMARY KEY (user_id, blocked_user_id)
);

-- Seed Data
INSERT INTO users (username, password, age, gender, bio, last_active, created_at) VALUES
('cool_guy', '5f4dcc3b5aa765d61d8327deb882cf99', 25, 'M', 'Just a cool guy looking for love.', 980000000, 980000000), -- password: password
('sweet_girl', '5f4dcc3b5aa765d61d8327deb882cf99', 23, 'F', 'Love to dance and travel!', 980000000, 980000000),
('tech_wiz', '5f4dcc3b5aa765d61d8327deb882cf99', 28, 'M', 'Building the future on WAP.', 980000000, 980000000),
('party_queen', '5f4dcc3b5aa765d61d8327deb882cf99', 21, 'F', 'Life is a party!', 980000000, 980000000),
('mystery_man', '5f4dcc3b5aa765d61d8327deb882cf99', 30, 'M', '...', 980000000, 980000000);

-- Note: Photos would need to be manually placed in img/ directory and referenced here if we had them.
-- For now, we assume no photos or placeholders.
