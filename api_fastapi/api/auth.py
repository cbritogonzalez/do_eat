from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi import Query
from core.auth_flow import get_google_flow
from services.calendar import user_creds
from fastapi.responses import JSONResponse
from fastapi import Response
from googleapiclient.discovery import build

router = APIRouter()


@router.get("/login")
def login():
    flow = get_google_flow()
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    return RedirectResponse(url=authorization_url)


@router.get("/redirect")
async def auth_redirect(code: str = Query(...)):
    flow = get_google_flow()
    flow.fetch_token(code=code)
    credentials = flow.credentials
    response = RedirectResponse(url="http://localhost:5173/setup")
    user_info_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()
    user_creds['token'] = credentials.to_json()
    response.set_cookie(key="email", value=user_info['email'], samesite="Lax")

    return response
    # return RedirectResponse(url="http://localhost:5173/setup")
    # return {"message": "Authentication successful", "token": credentials.token} # change to redirect to homepage
