drop table if exists scheduled_meals;
drop table if exists users_allergies;
drop table if exists users;
drop table if exists body_fat_types;
drop table if exists sex_types;
drop table if exists allergies;
drop table if exists cooking_durations;
drop table if exists diet_types;
drop table if exists meal_repetition_types;
drop table if exists recipes_ingredients;
drop table if exists recipes;
drop table if exists ingredients;
drop table if exists products;
drop table if exists markets;

create table body_fat_types(
	body_fat_id serial primary key,
	body_fat_descr varchar(10)
);

create table sex_types(
	sex_id serial primary key, 
	sex_descr varchar(10)
);

create table diet_types( -- TODO: based on nutrition api response, we may need another table with exclusions) ~ carlos
	diet_type_id serial primary key, 
	diet_type_descr varchar(20)
);

create table allergies( --TODO: might need adjustments based on API responses ~ carlos
	allergy_id serial primary key, 
	allergy_descr varchar(20)
);

create table cooking_durations(
	duration_id serial primary key, 
	duration_descr varchar(30)
);

create table meal_repetition_types(
	meal_repetition_id serial primary key, 
	meal_repetition_descr varchar(100)
);

create table users(
	user_id serial primary key, --automatically generated
	email varchar(50),
	age smallint,
	height_cm smallint, 
	weight_kg smallint,
	sex smallint,
	body_fat_type smallint, -- TODO: check if needed based on formulas!
	diet_type smallint,
	cooking_duration_weekday smallint,
	cooking_duration_weekend smallint,
	budget_daily money,
	-- meal layout (NOTE : if any of the below is null, then not chosen by user!)
	breakfast_time time, 
	lunch_time time, 
	dinner_time time,
	snack1_time time,
	snack2_time time,
	meal_repetition smallint, -- null if no repetition
	-- nutrition targets
	calories smallint, 
	carbs smallint,
	fat smallint, 
	protein smallint,
	
	foreign key (sex) references sex_types(sex_id),
	foreign key (body_fat_type) references body_fat_types(body_fat_id),
	foreign key (diet_type) references diet_types(diet_type_id),
	foreign key (cooking_duration_weekday) references cooking_durations(duration_id),
	foreign key (cooking_duration_weekend) references cooking_durations(duration_id),
	foreign key (meal_repetition) references meal_repetition_types(meal_repetition_id)
);

create table users_allergies(
	user_id smallint, 
	allergy_id smallint,
	
	primary key (user_id, allergy_id),
	foreign key (user_id) references users(user_id),
	foreign key (allergy_id) references allergies(allergy_id)
);

create table markets(
	market_id serial primary key,
	market_name varchar(20)
);

create table products( -- TODO: discuss how to delete outdated ones (with trigger)
	offer_id serial primary key,
	product_title varchar(100),
	brand varchar(50),
	bonus_start_date date, --null if not offer
	bonus_end_date date, --null if not offer
	bonus_mechanism varchar(50), --bonus string
	initial_price money, --price if not offer
	final_price money, --null if not offer
	market_id smallint,
	
	foreign key (market_id) references markets(market_id)
);

create table ingredients(
	ingredient_id bigserial primary key,
	ingredient_descr varchar(100) -- note: w/ quantity
);

create table recipes( --TODO: to be adapted based on nutrition API
	recipe_id bigserial primary key,
	recipe_name varchar(100),
	image bytea,
	calories smallint,
	carbs smallint,
	protein smallint,
	fat smallint,
	prep_time_minutes smallint,
	cook_time_minutes smallint,
	instructions text,
	portions SMALLINT,
	total_cost money
);

create table recipes_ingredients(
	recipe_id bigint,
	ingredient_id bigint,
	
	primary key (recipe_id, ingredient_id),
	foreign key (recipe_id) references recipes(recipe_id),
	foreign key (ingredient_id) references ingredients(ingredient_id)
);

create table scheduled_meals(
	user_id int, 
	recipe_id bigint,
	date_time timestamptz, -- NOTE: with timezone
	
	primary key (user_id, recipe_id, date_time),
	foreign key (user_id) references users(user_id),
	foreign key (recipe_id) references recipes(recipe_id)
);

insert into body_fat_types(body_fat_descr)
values ('low'), ('medium'), ('high');

insert into sex_types(sex_descr)
values ('female'), ('male');

insert into diet_types(diet_type_descr)
values ('anything'), ('pescetarian'), ('vegetarian'), ('vegan'), ('keto'), ('paleo');

insert into allergies(allergy_descr)
values ('gluten'), ('peanuts'), ('eggs'), ('fish'), ('nuts'), ('dairy'), ('soy'), ('shellfish');

insert into cooking_durations(duration_descr)
values ('10-30 minutes'), ('30 minutes-1 hour'), ('1-1.5 hours'), ('1.5-2 hours'), ('2+ hours');

insert into meal_repetition_types(meal_repetition_descr)
values ('none'), ('repeatDinnerForNextLunch'), ('repeatLunchForSameDinner');

insert into markets(market_name)
values ('Jumbo'), ('Albert Heijn');
