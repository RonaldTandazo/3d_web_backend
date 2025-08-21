import user_agents
from datetime import datetime, timezone
from app.config.logger import logger
import base64
import uuid
import os

class Helpers:
    async def getIp(request) -> str:
        client_host = request.client.host
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        x_real_ip = request.headers.get("X-Real-IP")

        if x_forwarded_for:
            client_host = x_forwarded_for.split(",")[0]
        elif x_real_ip:
            client_host = x_real_ip

        return client_host

    async def getRequestAgents(request):
        user_agents_string = request.headers.get("user-agent")
        ua = user_agents.parse(user_agents_string)

        return {
            "device": ua.device.family,
            "os": ua.os.family,
            "browser": ua.browser.family,
        }
    
    async def getDateTime():
        now_utc = datetime.now(timezone.utc)
        formatted_now_utc = now_utc.strftime("%Y-%m-%d %H:%M:%S")

        return formatted_now_utc
    
    async def prepareAccessTokenData(user):
        structure = {
            "sub": user.username,
            "userId": user.user_id,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "email": user.email,
            "username": user.username,
            "professionalHeadline": user.professional_headline,
            "summary": user.summary,
            "city": user.city,
            "countryId": user.country_id,
            "location": f"{user.city}, {user.country.name}" if user.country else None,
            "since": user.created_at.isoformat() if user.created_at else None,
            "avatar": user.avatar
        }
        
        return structure
    
    async def generateRandomFilename(extension):
        filename = f"{uuid.uuid4()}{extension}"
        return filename
    
    async def decodedAndSaveImg(filename: str, img_base64: str, type: str):
        try:
            img_data  = base64.b64decode(img_base64.split(',')[1])
            upload_folder = "app/public"

            if type == "thumbnail":
                upload_folder += "/artworks/thumbnails"

            if type == "avatar":
                upload_folder += "/users/avatars"

            if type == "image":
                upload_folder += "/artworks/multimedia/images"

            if type == "video":
                upload_folder += "/artworks/multimedia/videos"

            os.makedirs(upload_folder, exist_ok=True)

            file_path = os.path.join(upload_folder, filename)

            with open(file_path, "wb") as f:
                f.write(img_data)

            return {"ok": True, "message": "File Saved Successfully", "code": 201, "data": None}
        except Exception as e:
            logger.error(e)
            return {"ok": False, "error": "Error Saving File", "code": 500}
        
    async def deleteImage(filename: str, type: str):
        try:
            base_folder = "app/public"
            target_folder = base_folder

            if type == "thumbnail":
                target_folder += "/artworks/thumbnails"
            elif type == "avatar":
                target_folder += "/users/avatars"

            file_path_to_delete = os.path.join(target_folder, filename)

            if os.path.exists(file_path_to_delete):
                os.remove(file_path_to_delete)

            return {"ok": True, "message": "File Deleted Successfully", "code": 200}
        except Exception as e:
            logger.error(e)
            return {"ok": False, "error": "Error Deleting File", "code": 500}