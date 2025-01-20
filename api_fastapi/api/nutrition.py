from fastapi import APIRouter, Query, HTTPException, Cookie
from services.fatsecret import get_fatsecret_service
from services.calendar import get_calendar_service
from core.config import POSTGRES_DB_CONNECTION
import requests
import psycopg2
from datetime import datetime, timedelta
from uuid import uuid4

router = APIRouter()


@router.get("/recipe/")
async def get_recipes(search_expression: str = Query(...)):
    auth_token = get_fatsecret_service()
    params = {
        "search_expression": search_expression,  # Replace with your search term
        "format": "json",
    }
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }
    response = requests.get("https://platform.fatsecret.com/rest/recipes/search/v3", headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

@router.post("/user/recipes/")
async def create_recipes(email: str = Query(...)):
    auth_token = get_fatsecret_service()
    conn = psycopg2.connect(POSTGRES_DB_CONNECTION)
    cursor = conn.cursor()
    cursor.execute(f"SELECT user_id FROM users WHERE email = '{email}' LIMIT 1")
    user_id = cursor.fetchone()
    user_id = int(user_id[0])
    try:
        cursor.execute(f"SELECT diet_type, calories, carbs, fat, protein, breakfast_time, lunch_time, dinner_time, cooking_duration_weekday, snack1_time, snack2_time FROM users WHERE email = '{email}'" ) # where user_id = 1
        preferences = cursor.fetchone()
        breakfast_time = preferences[5]
        lunch_time = preferences[6]
        dinner_time = preferences[7]
        snack1_time = preferences[9]
        snack2_time = preferences[10]
        cooking_duration_weekday = preferences[8]
        eatings_times = [breakfast_time, lunch_time, dinner_time, snack1_time, snack2_time]
        print(eatings_times)
        eatings_times = [(item.hour, item.minute) for item in eatings_times]
        # need to get the diet type from the other table
        cursor.execute(f"SELECT diet_type_descr FROM diet_types WHERE diet_type_id = {preferences[0]}")
        diet_type = cursor.fetchall()

        # need to get the allegeries from other table, then use these as parameters or to filter
        cursor.execute("SELECT allergy_id FROM users_allergies")
        allergies = cursor.fetchall()
        # after making the calls to the fatsecret api
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

    params = {
        "format": "json",
        "max_results": 7,
        "prep_time.to": cooking_duration_weekday
    }
    # for preference in preferences:# change this to the user columns
    #     params[preference[0]] = preference[1]

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }
    response = requests.get("https://platform.fatsecret.com/rest/recipes/search/v3", headers=headers, params=params)
    if response.status_code == 200:
        # insert into db
        today = datetime.now()
        service = get_calendar_service()
        response_json = response.json()
        print(response_json)
        recipes = response_json['recipes']['recipe'] # may need to change
        # recipe_ids = []
        for index, recipe in enumerate(recipes):
            recipe_id = int(recipe['recipe_id'])
            # recipe_ids.append(recipe_id)
            cursor.execute(
            """
            INSERT INTO recipes (recipe_id, recipe_name, calories, carbs, fat, protein)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (recipe_id) DO NOTHING
            """,
            (
                recipe_id,
                recipe['recipe_name'],
                int(float(recipe['recipe_nutrition']['calories'])),
                int(float(recipe['recipe_nutrition']['carbohydrate'])),
                int(float(recipe['recipe_nutrition']['fat'])),
                int(float(recipe['recipe_nutrition']['protein'])),
            )
            )
            conn.commit()
            for item in recipe['recipe_ingredients']['ingredient']:
                cursor.execute(
                """
                INSERT INTO ingredients (ingredient_descr)
                VALUES (%s)
                ON CONFLICT (ingredient_id) DO NOTHING
                RETURNING ingredient_id
                """,
                (
                    item,
                )
                )
                result = cursor.fetchone()
                conn.commit()
                cursor.execute(
                """
                INSERT INTO recipes_ingredients (recipe_id, ingredient_id)
                VALUES (%s, %s)
                ON CONFLICT (recipe_id, ingredient_id) DO NOTHING
                """,
                (
                    recipe_id,
                    result[0],
                )
                )
                conn.commit()
            # create events
            event_payload = {
                'summary': recipe['recipe_name'], # change to recipe name
                'location': "Google Meet",
                'description': recipe['recipe_description'], # change to recipe description
                "start": {
                    "dateTime": "",
                    "timeZone": "Europe/Amsterdam"
                },
                "end": {
                    "dateTime": "",
                    "timeZone": "Europe/Amsterdam"
                },
                'attendees': [],
                'conferenceData': {
                    'createRequest': {
                        'conferenceSolutionKey': {
                            'type': 'hangoutsMeet'
                        },
                        'requestId': '1'
                    }
                }
            }
            custom_date = today + timedelta(days=index)
            for index, item in enumerate(eatings_times):
                custom_datetime = custom_date.replace(hour=item[0], minute=item[1], second=0, microsecond=0)
                # add description and recipe details
                event_payload['start']['dateTime'] = custom_datetime.isoformat()
                event_payload['end']['dateTime'] = (custom_datetime + timedelta(hours=1)).isoformat() # change to duration of the recipe
                conn.commit()
                cursor.execute(
                """
                INSERT INTO scheduled_meals (user_id, recipe_id, date_time)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id, recipe_id, date_time) DO NOTHING
                """,
                (
                    user_id,
                    recipe_id,
                    custom_datetime.isoformat(),
                )
                )
                conn.commit()
                created_event = service.events().insert(calendarId='primary', body=event_payload, conferenceDataVersion=1).execute()
        return {"event": "created_events"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


