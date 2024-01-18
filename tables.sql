-- Let's drop the tables in case they exist from previous runs
drop table if exists includes;
drop table if exists lists;
drop table if exists retweets;
drop table if exists mentions;
drop table if exists hashtags;
drop table if exists tweets;
drop table if exists follows;
drop table if exists users;

create table users (
  usr         int,
  name        text,
  email       text,
  city        text,
  timezone    float,
  primary key (usr)
);
create table follows (
  flwer       int,
  flwee       int,
  start_date  date,
  primary key (flwer,flwee),
  foreign key (flwer) references users,
  foreign key (flwee) references users
);
create table tweets (
  writer      int,
  tdate       date,
  text        text,
  replyto_w   int,
  replyto_d   date,
  primary key (writer,tdate),
  foreign key (writer) references users,
  foreign key (replyto_w,replyto_d) references tweets
);
create table hashtags (
  term        text,
  primary key (term)
);
create table mentions (
  writer      int,
  tdate       date,
  term        text,
  primary key (writer,tdate,term),
  foreign key (writer,tdate) references tweets,
  foreign key (term) references hashtags
);
create table retweets (
  usr         int,
  writer      int,
  tdate       date,
  rdate       date,
  primary key (usr,writer,tdate),
  foreign key (usr) references users,
  foreign key (writer,tdate) references tweets
);
create table lists (
  lname        text,
  owner        int,
  primary key (lname),
  foreign key (owner) references users
);
create table includes (
  lname       text,
  member      int,
  primary key (lname,member),
  foreign key (lname) references lists,
  foreign key (member) references users
);