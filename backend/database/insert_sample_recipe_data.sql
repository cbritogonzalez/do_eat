INSERT INTO ingredients (ingredient_descr) VALUES 
('500 g Chicken Breast'),
('20g Broccoli'),
('1 cup Rice'),
('1 teaspoon Olive Oil'),
('3 Eggs'),
('50g Spinach'),
('1/2 cup Quinoa'),
('5 Tomatos'),
('10g Cheddar Cheese'),
('5 Almonds');

INSERT INTO recipes (recipe_name, image, calories, carbs, protein, fat, prep_time_minutes, cook_time_minutes, instructions, portions) VALUES 
('Grilled Chicken with Broccoli', NULL, 400, 30, 40, 10, 10, 20, 'Grill the chicken and steam the broccoli. Serve with rice.', 2),
('Veggie Omelette', NULL, 300, 5, 20, 15, 5, 10, 'Whisk eggs, cook with spinach and cheddar cheese.', 1),
('Quinoa Salad', NULL, 250, 40, 8, 5, 15, 0, 'Mix quinoa with diced tomatoes and almonds.', 2);

INSERT INTO recipes_ingredients (recipe_id, ingredient_id) VALUES 
(1, 1), -- Grilled Chicken with Chicken Breast
(1, 2), -- Grilled Chicken with Broccoli
(1, 3), -- Grilled Chicken with Rice
(2, 5), -- Veggie Omelette with Eggs
(2, 6), -- Veggie Omelette with Spinach
(2, 9), -- Veggie Omelette with Cheddar Cheese
(3, 8), -- Quinoa Salad with Tomato
(3, 10), -- Quinoa Salad with Almonds
(3, 3); -- Quinoa Salad with Rice

-- Assuming user_id = 1 for demonstration purposes
DO $$
DECLARE 
    r RECORD;
BEGIN
    FOR d IN 0..6 LOOP
        -- Schedule Grilled Chicken with Broccoli
        INSERT INTO scheduled_meals (user_id, recipe_id, date_time) VALUES 
        (1, 1, NOW() + (d * INTERVAL '1 day') + INTERVAL '18 hours'); -- Dinner

        -- Schedule Veggie Omelette
        INSERT INTO scheduled_meals (user_id, recipe_id, date_time) VALUES 
        (1, 2, NOW() + (d * INTERVAL '1 day') + INTERVAL '8 hours'); -- Breakfast

        -- Schedule Quinoa Salad
        INSERT INTO scheduled_meals (user_id, recipe_id, date_time) VALUES 
        (1, 3, NOW() + (d * INTERVAL '1 day') + INTERVAL '12 hours'); -- Lunch
    END LOOP;
END $$;