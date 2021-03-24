/*Used to instantiate the database the first time*/
CREATE TABLE IF NOT EXISTS followed_users
(
  follower_name varchar(255) NOT NULL,
  followed_id BIGINT NOT NULL,
  followed_name varchar(255) NOT NULL,
  PRIMARY KEY (follower_name, followed_id)
);
