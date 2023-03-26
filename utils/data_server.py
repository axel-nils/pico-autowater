import uasyncio as asyncio
from utils.api_calls import get_datetime_str


class DataServer:
    def __init__(self, ip):
        self.ip = ip
        self.port = 80
        self.host = "0.0.0.0"

        self.files = {"html": "web/index.html", "error": "web/notfound.html",
                      "css": "web/style.css", "js": "web/app.js", "json": "data.json",
                      "png": "web/icon.png"}
        self.pages = self.preload_pages()
        self.system_status = dict()
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
        try:
            request_line = await reader.readline()
            while await reader.readline() != b"\r\n":
                pass

            header, response = self.handle_request(request_line)
            writer.write(header)
            writer.write(response)
            await writer.drain()
            await writer.wait_closed()
        except OSError as e:
            print(e)

    def handle_request(self, request_line):
        request = str(request_line)
        try:
            request = request.split()[1]
        except IndexError:
            pass

        print(get_datetime_str(), "Server got request:", request)

        html_requests = ["/", "//", "/index.html"]
        posts = ["/water_on", "/water_off"]

        if request in html_requests:
            header = self.ok_header("text/html", 60)
            response = self.create_html_response()
        elif request in posts:
            header = "HTTP/1.1 204 No content\r\n\r\n"
            response = ""
        elif "style.css" in request:
            header = self.ok_header("text/css", 86400)
            response = self.pages["css"]
        elif "app.js" in request:
            header = self.ok_header("application/javascript", 86400)
            response = self.pages["js"]
        elif "data.json" in request:
            header = self.ok_header("application/json", 600)
            response = self.pages["json"]
        elif "icon.png" in request:
            header = self.ok_header("image/png", 86400)
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
        for r in self.system_status:
            response = response.replace(r, str(self.system_status[r]))
        return response

    @staticmethod
    def ok_header(content_type, max_age):
        return f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nCache-Control: max-age={max_age}\r\n\r\n"
