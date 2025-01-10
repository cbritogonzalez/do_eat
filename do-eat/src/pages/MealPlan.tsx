import Layout from '../components/Layout';
import './MealPlan.css';

const mealPlan = [
  {
    day: 'Monday',
    meals: [
      {
        time: '08:00',
        name: 'Breakfast - Oatmeal',
        description: 'Pre-heat oven to 400 °F (200 °C). Coat a small baking sheet with cooking spray. Coat a large non-stick skillet with cooking spray and heat over medium-low heat.\
In a large bowl, add egg substitute, bacon, oregano, salt, pepper and salsa; stir well.\
Pour egg mixture into prepared skillet; increase heat to medium. Let eggs partially set and then scramble using a spatula. When eggs are set but still slightly glossy, remove from heat.\
Spoon half of egg mixture into center of each tortilla. Roll tortilla to conceal filling, making sure to fold in ends. Place burritos, seam-side down, on prepared baking sheet.\
Bake until burritos are very hot, about 5 minutes. Remove from oven and serve each burrito with 1 tablespoon sour cream and 1 slice avocado.\
Note: for a breakfast on the go, fill a toasted whole-wheat pita half with the scrambled egg mixture, sour cream and avocado.',
        nutrition: 'Calories: 150, Protein: 5g, Carbs: 27g, Fat: 3g',
        cookTime: '10 mins',
        cost: '$2',
        ingredients: ['Oats', 'Milk', 'Fruits', 'Honey'],
        portions: '1 serving',
      },
      {
        time: '10:00',
        name: 'Snack - Apple',
        description: 'A fresh apple.',
        nutrition: 'Calories: 95, Protein: 0.5g, Carbs: 25g, Fat: 0.3g',
        cookTime: '0 mins',
        cost: '$1',
        ingredients: ['Apple'],
        portions: '1 apple',
      },
      // ... other meals
    ],
  },
  {
    day: 'Tuesday',
    meals: [
      {
        time: '08:00',
        name: 'Breakfast - Smoothie',
        description: 'A refreshing fruit smoothie.',
        nutrition: 'Calories: 200, Protein: 5g, Carbs: 45g, Fat: 2g',
        cookTime: '5 mins',
        cost: '$3',
        ingredients: ['Banana', 'Berries', 'Yogurt', 'Honey'],
        portions: '1 serving',
      },
      {
        time: '10:00',
        name: 'Snack - Banana',
        description: 'A ripe banana.',
        nutrition: 'Calories: 105, Protein: 1g, Carbs: 27g, Fat: 0.3g',
        cookTime: '0 mins',
        cost: '$0.5',
        ingredients: ['Banana'],
        portions: '1 banana',
      },
      // ... other meals
    ],
  },
  {
    day: 'Wednesday',
    meals: [
      {
        time: '08:00',
        name: 'Breakfast - Pancakes',
        description: 'Fluffy pancakes with syrup.',
        nutrition: 'Calories: 350, Protein: 8g, Carbs: 60g, Fat: 10g',
        cookTime: '15 mins',
        cost: '$4',
        ingredients: ['Flour', 'Eggs', 'Milk', 'Syrup'],
        portions: '2 servings',
      },
      {
        time: '10:00',
        name: 'Snack - Orange',
        description: 'A juicy orange.',
        nutrition: 'Calories: 62, Protein: 1.2g, Carbs: 15.4g, Fat: 0.2g',
        cookTime: '0 mins',
        cost: '$0.7',
        ingredients: ['Orange'],
        portions: '1 orange',
      },
      // ... other meals
    ],
  },
  {
    day: 'Thursday',
    meals: [
      {
        time: '08:00',
        name: 'Breakfast - Yogurt with Granola',
        description: 'Greek yogurt with granola and honey.',
        nutrition: 'Calories: 250, Protein: 10g, Carbs: 35g, Fat: 8g',
        cookTime: '5 mins',
        cost: '$3',
        ingredients: ['Greek Yogurt', 'Granola', 'Honey'],
        portions: '1 serving',
      },
      {
        time: '10:00',
        name: 'Snack - Carrot Sticks',
        description: 'Fresh carrot sticks.',
        nutrition: 'Calories: 50, Protein: 1g, Carbs: 12g, Fat: 0.2g',
        cookTime: '0 mins',
        cost: '$0.5',
        ingredients: ['Carrots'],
        portions: '1 cup',
      },
      // ... other meals
    ],
  },
  {
    day: 'Friday',
    meals: [
      {
        time: '08:00',
        name: 'Breakfast - Avocado Toast',
        description: 'Whole grain toast with avocado.',
        nutrition: 'Calories: 300, Protein: 7g, Carbs: 40g, Fat: 15g',
        cookTime: '10 mins',
        cost: '$3.5',
        ingredients: ['Whole Grain Bread', 'Avocado', 'Salt', 'Pepper'],
        portions: '1 serving',
      },
      {
        time: '10:00',
        name: 'Snack - Berries',
        description: 'A mix of fresh berries.',
        nutrition: 'Calories: 70, Protein: 1g, Carbs: 18g, Fat: 0.3g',
        cookTime: '0 mins',
        cost: '$2',
        ingredients: ['Berries'],
        portions: '1 cup',
      },
      // ... other meals
    ],
  },
  {
    day: 'Saturday',
    meals: [
      {
        time: '08:00',
        name: 'Breakfast - Scrambled Eggs',
        description: 'Scrambled eggs with toast.',
        nutrition: 'Calories: 250, Protein: 15g, Carbs: 20g, Fat: 12g',
        cookTime: '10 mins',
        cost: '$2.5',
        ingredients: ['Eggs', 'Toast', 'Butter'],
        portions: '1 serving',
      },
      {
        time: '10:00',
        name: 'Snack - Grapes',
        description: 'A bunch of grapes.',
        nutrition: 'Calories: 60, Protein: 0.6g, Carbs: 15g, Fat: 0.2g',
        cookTime: '0 mins',
        cost: '$1.5',
        ingredients: ['Grapes'],
        portions: '1 cup',
      },
      // ... other meals
    ],
  },
  {
    day: 'Sunday',
    meals: [
      {
        time: '08:00',
        name: 'Breakfast - French Toast',
        description: 'French toast with maple syrup.',
        nutrition: 'Calories: 400, Protein: 10g, Carbs: 60g, Fat: 15g',
        cookTime: '20 mins',
        cost: '$4',
        ingredients: ['Bread', 'Eggs', 'Milk', 'Maple Syrup'],
        portions: '2 servings',
      },
      {
        time: '10:00',
        name: 'Snack - Pear',
        description: 'A ripe pear.',
        nutrition: 'Calories: 100, Protein: 0.5g, Carbs: 27g, Fat: 0.2g',
        cookTime: '0 mins',
        cost: '$1',
        ingredients: ['Pear'],
        portions: '1 pear',
      },
      // ... other meals
    ],
  },
];

function MealPlan() {
  return (
    <Layout>
      {mealPlan.map((dayPlan) => (
        <div key={dayPlan.day} className="day-plan">
          <h2 className="day-title">{dayPlan.day}</h2>
          {dayPlan.meals.map((meal) => (
            <div key={meal.time} className="meal">
              <h3 className="meal-time">{meal.time} - {meal.name}</h3>
              <p className="meal-nutrition">{meal.nutrition}</p>
              <p className="meal-cook-time">Cook Time: {meal.cookTime}</p>
              <p className="meal-cost">Cost: {meal.cost}</p>
              <p className="meal-portions">Portions: {meal.portions}</p>
              <ul className="meal-ingredients">
                {meal.ingredients.map((ingredient, index) => (
                  <li key={index}>{ingredient}</li>
                ))}
              </ul>
              <p className="meal-description">{meal.description}</p>
            </div>
          ))}
        </div>
      ))}
    </Layout>
  );
}

export default MealPlan;