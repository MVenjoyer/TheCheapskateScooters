Table auth_user as User {
  id integer [primary key]
  password varchar(128) [not null]
  last_login datetime
  is_superuser boolean [not null]
  username varchar(150) [not null, unique]
  first_name varchar(150) [not null]
  last_name varchar(150) [not null]
  email varchar(254) [not null]
  is_staff boolean [not null]
  is_active boolean [not null]
  date_joined datetime [not null]
}

Table profile as Profile {
  id integer [primary key]
  phone varchar(20) [null]
  user_id integer [ref: > auth_user.id, not null, unique]
}

Table scooter_points as ScooterPoint {
  id integer [primary key]
  name varchar(100) [not null]
  latitude float [not null]
  longitude float [not null]
}

Table scooters as Scooter {
  id integer [primary key]
  name varchar(100) [not null]
  description text [not null]
  rating float [default: 0.0]
  is_available boolean [default: true]
  battery_level integer [default: 100]
  created_at datetime [not null]
  latitude float [null]
  longitude float [null]
  point_id integer [ref: > scooter_points.id, null]
}

Table rentals as Rental {
  id integer [primary key]
  profile_id integer [ref: > profile.id, not null]
  scooter_id integer [ref: > scooters.id, not null]
  start_time datetime [null]
  end_time datetime [null]
  start_latitude float [null]
  start_longitude float [null]
  end_latitude float [null]
  end_longitude float [null]
  total_price decimal(8, 2) [null]
}