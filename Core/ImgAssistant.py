from g4f.client import AsyncClient
from g4f.cookies import set_cookies

from config import _Secure1PSID, _U

client = AsyncClient()
set_cookies(".bing.com", {
    "_U": _U
})
set_cookies(".google.com", {
    "__Secure-1PSID": _Secure1PSID
})


async def get_dalle_response(prompt):
    try:
        response = await client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1920x1080",
            quality="hd",
            n=4,
        )
        image_urls = [image.url for image in response.data]
    except Exception as e:
        print(e)
        image_urls = []
    return image_urls
