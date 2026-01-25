CREATE TABLE "profile" (
  "id" integer PRIMARY KEY,
  "phone" varchar(20),
  "user_id" integer UNIQUE NOT NULL
);

CREATE TABLE "auth_user" (
  "id" integer PRIMARY KEY,
  "password" varchar(128) NOT NULL,
  "last_login" datetime,
  "is_superuser" boolean NOT NULL,
  "username" varchar(150) UNIQUE NOT NULL,
  "first_name" varchar(150) NOT NULL,
  "last_name" varchar(150) NOT NULL,
  "email" varchar(254) NOT NULL,
  "is_staff" boolean NOT NULL,
  "is_active" boolean NOT NULL,
  "date_joined" datetime NOT NULL
);

CREATE TABLE "scooter_points" (
  "id" integer PRIMARY KEY,
  "name" varchar(100) NOT NULL,
  "latitude" float NOT NULL,
  "longitude" float NOT NULL
);

CREATE TABLE "scooters" (
  "id" integer PRIMARY KEY,
  "name" varchar(100) NOT NULL,
  "description" text NOT NULL,
  "rating" float DEFAULT 0,
  "is_available" boolean DEFAULT true,
  "battery_level" integer DEFAULT 100,
  "created_at" datetime NOT NULL,
  "latitude" float,
  "longitude" float,
  "point_id" integer
);

CREATE TABLE "rentals" (
  "id" integer PRIMARY KEY,
  "profile_id" integer NOT NULL,
  "scooter_id" integer NOT NULL,
  "start_time" datetime,
  "end_time" datetime,
  "start_latitude" float,
  "start_longitude" float,
  "end_latitude" float,
  "end_longitude" float,
  "total_price" decimal(8,2)
);

ALTER TABLE "profile" ADD FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id");

ALTER TABLE "scooters" ADD FOREIGN KEY ("point_id") REFERENCES "scooter_points" ("id");

ALTER TABLE "rentals" ADD FOREIGN KEY ("profile_id") REFERENCES "profile" ("id");

ALTER TABLE "rentals" ADD FOREIGN KEY ("scooter_id") REFERENCES "scooters" ("id");