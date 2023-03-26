import uasyncio as asyncio
from utils.api_calls import get_datetime


class DataServer:
    def __init__(self, ip):
        self.ip = ip
        self.port = 80
        self.host = "0.0.0.0"

        self.files = {"html": "web/index.html", "error": "web/notfound.html",
                      "css": "web/style.css", "js": "web/app.js", "json": "data/data.json",
                      "png": "web/icon.png"}
        self.pages = self.preload_pages()
        self.replacements = dict()
        self.water_on = False
        self.water_off = False

    def preload_pages(self) -> dict:
        pages = {}
        for name, file_name in self.files.items():
            if name == "png":
                with open(file_name, "rb") as f:
                    pages[name] = f.read()
            else:
                with open(file_name, "r") as f:
                    pages[name] = str(f.read())
        return pages

    async def run_server(self):
        await asyncio.start_server(self.serve, self.host, self.port)

    async def serve(self, reader, writer):
        request_line = await reader.readline()
        while await reader.readline() != b"\r\n":
            pass

        header, response = self.handle_request(request_line)
        writer.write(header)
        writer.write(response)
        await writer.drain()
        await writer.wait_closed()

    def handle_request(self, request_line):
        request = str(request_line)
        try:
            request = request.split()[1]
        except IndexError:
            pass

        print(get_datetime(), "Server got request:", request)

        html_requests = ["/", "//", "/index.html"]
        posts = ["/water_on", "/water_off"]

        if request in html_requests:
            header = self.create_standard_header("text/html")
            response = self.create_html_response()
        elif request in posts:
            header = "HTTP/1.1 204 No content\r\n\r\n"
            response = ""
        elif "style.css" in request:
            header = self.create_standard_header("text/css")
            response = self.pages["css"]
        elif "app.js" in request:
            header = self.create_standard_header("application/javascript")
            response = self.pages["js"]
        elif "data.json" in request:
            header = self.create_standard_header("application/json")
            response = self.pages["json"]
        elif "icon.png" in request:
            header = self.create_standard_header("image/png")
            response = self.pages["png"]
        else:
            header = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
            response = self.pages["error"]

        if "/water_on" in request:
            self.water_on = True
            self.water_off = False
        elif "/water_off" in request:
            self.water_off = True
            self.water_on = False

        return header, response

    def create_html_response(self):
        response = self.pages["html"]
        for r in self.replacements:
            response = response.replace(r, str(self.replacements[r]))
        return response

    @staticmethod
    def create_standard_header(content_type):
        return f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nCache-Control: max-age=60\r\n\r\n"
