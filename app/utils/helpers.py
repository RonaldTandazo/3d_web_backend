import user_agents
from datetime import datetime, timezone
from app.config.logger import logger

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