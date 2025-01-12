CREATE OR REPLACE PROCEDURE insert_user(
    IN age smallint,
    IN allergies TEXT[],
    IN bodyFat TEXT,
    IN budget_daily money,
    IN cookingDuration TEXT,
    IN dietType TEXT,
    IN goal TEXT,
    IN height_cm smallint,
    IN mealRepetition TEXT,
    IN breakfastTime time,
    IN snack1Time time,
    IN lunchTime time,
    IN snack2Time time,
    IN dinnerTime time,
    IN sex TEXT,
    IN weight smallint
)
LANGUAGE plpgsql
AS $$
DECLARE
    new_user_id smallint;  -- To hold the ID of the newly inserted user
    new_body_fat_id smallint;
    new_diet_type_id smallint;
    new_cooking_duration_id smallint;
    new_sex_id smallint;
	new_meal_repetition smallint;
    new_allergy_id smallint;
    allergy TEXT;  -- Declare the loop variable for allergies
    calories numeric;  -- Declare calories variable
BEGIN
    -- Retrieve foreign key IDs
    SELECT body_fat_id INTO new_body_fat_id FROM body_fat_types WHERE body_fat_descr = bodyFat LIMIT 1;
    SELECT diet_type_id INTO new_diet_type_id FROM diet_types WHERE diet_type_descr = dietType LIMIT 1;
    SELECT duration_id INTO new_cooking_duration_id FROM cooking_durations WHERE duration_descr = cookingDuration LIMIT 1;
    SELECT sex_id INTO new_sex_id FROM sex_types WHERE sex_descr = sex LIMIT 1;
	SELECT meal_repetition_id INTO new_meal_repetition FROM meal_repetition_types WHERE meal_repetition_descr = mealRepetition LIMIT 1;

    -- Compute calories based on sex
    calories := CASE 
        WHEN sex = 'male' THEN 13.397 * weight + 4.799 * height_cm - 5.677 * age + 88.362  -- Formula for men
        WHEN sex = 'female' THEN 9.247 * weight + 3.098 * height_cm - 4.330 * age + 447.593  -- Formula for women
        ELSE 0  -- Default value if sex is not specified
    END;

    -- Insert into users table
    INSERT INTO users (
        user_name, 
        email,
        password_hash,
        age,
        height_cm,
        weight_kg,
        sex,
        body_fat_type,
        diet_type,
        cooking_duration_weekday,
        cooking_duration_weekend,
        budget_daily,
        breakfast_time,
        snack1_time,
        lunch_time,
        snack2_time,
        dinner_time,
        meal_repetition,
        calories,
        carbs,
        fat,
        protein
    ) VALUES (
        'default',  -- Replace with actual logic for user_name
        'default_email@example.com',  -- Replace with actual logic for email
        'default_hash',  -- Replace with actual hash for password
        age,
        height_cm,
        weight,
        new_sex_id,
        new_body_fat_id,
        new_diet_type_id,
        new_cooking_duration_id,
        new_cooking_duration_id,
        budget_daily,
        breakfastTime,
        snack1Time,
        lunchTime,
        snack2Time,
        dinnerTime,
        new_meal_repetition,
        calories,
        calories * 0.55 / 4,  -- Carbs formula (55% of calories, 4 calories per gram)
        calories * 0.25 / 9,  -- Fat formula (25% of calories, 9 calories per gram)
        calories * 0.20 / 4   -- Protein formula (20% of calories, 4 calories per gram)
    ) RETURNING user_id INTO new_user_id;

    -- Insert into users_allergies table
    FOREACH allergy IN ARRAY allergies
    LOOP
        SELECT allergy_id INTO new_allergy_id FROM allergies WHERE allergy_descr = allergy LIMIT 1;
        INSERT INTO users_allergies (user_id, allergy_id) VALUES (new_user_id, new_allergy_id);
    END LOOP;
    
    RAISE NOTICE 'User and allergies inserted successfully with user_id: %', new_user_id;
END;
$$;

CALL insert_user(
    30::smallint,                                   -- Age
    ARRAY['gluten', 'dairy']::TEXT[],              -- Allergies
    'medium'::TEXT,                                 -- Body fat
    50.00::money,                                   -- Daily budget
    '30 - 1 hour'::TEXT,                            -- Cooking duration
    'vegetarian'::TEXT,                             -- Diet type
    'weight loss'::TEXT,                            -- Goal
    180::smallint,                                  -- Height in cm
    'none'::TEXT,                                    -- Meal repetition (assuming an ID from meal_repetition_types)
    '08:00:00'::time,                               -- Breakfast time
    '10:00:00'::time,                               -- Snack 1 time
    '12:00:00'::time,                               -- Lunch time
    '15:00:00'::time,                               -- Snack 2 time
    '18:00:00'::time,                               -- Dinner time
    'male'::TEXT,                                   -- Sex
    75::smallint                                    -- Weight in kg
);
---------------------------------------
CREATE OR REPLACE FUNCTION get_scheduled_meals(user_id_input INT)
RETURNS TABLE(
    recipe_name VARCHAR,
    date_time TIMESTAMPTZ,
    ingredients TEXT,
    nutrition_info TEXT,
    total_cook_time TEXT,  -- Changed to TEXT
    cost TEXT,             -- Changed to TEXT
    portions smallint,
    instructions TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.recipe_name,
        sm.date_time,
        STRING_AGG(i.ingredient_descr, ', ') AS ingredients,
        FORMAT('Calories: %skcal, Protein: %sg, Carbs: %sg, Fat: %sg', r.calories, r.protein, r.carbs, r.fat) AS nutrition_info,
        FORMAT('%s mins', (r.prep_time_minutes + r.cook_time_minutes)) AS total_cook_time,
        FORMAT('€%s', r.total_cost) AS cost,
        r.portions,
        r.instructions
    FROM scheduled_meals sm
    JOIN recipes r ON sm.recipe_id = r.recipe_id
    LEFT JOIN recipes_ingredients ri ON r.recipe_id = ri.recipe_id
    LEFT JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
    LEFT JOIN products p ON r.recipe_id = p.offer_id  -- Assuming offer_id corresponds to recipe_id for cost
    WHERE sm.user_id = user_id_input
      AND sm.date_time >= NOW()  -- Current time
      AND sm.date_time < NOW() + INTERVAL '7 days'  -- Next 7 days
    GROUP BY r.recipe_name, sm.date_time, r.calories, r.protein, r.carbs, r.fat, r.prep_time_minutes, r.cook_time_minutes, r.total_cost, r.portions, r.instructions
    ORDER BY sm.date_time ASC;  -- Order by date_time from oldest to newest
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_scheduled_meals(1);
