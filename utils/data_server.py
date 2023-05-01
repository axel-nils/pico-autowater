import uasyncio as asyncio


class WaterSettings(enumerate):
    auto = -1
    off = 0
    on = 1

    @staticmethod
    def to_str(setting):
        if setting == WaterSettings.auto:
            return "auto"
        elif setting == WaterSettings.on:
            return "on"
        elif setting == WaterSettings.off:
            return "off"


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
        self.water_setting = WaterSettings.auto

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
        await asyncio.start_server(self.serve_client, self.host, self.port)

    async def serve_client(self, reader, writer):
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

        print("Server got request:", request)

        html_requests = ["/", "/index.html"]
        posts = ["/water=auto", "/water=on", "/water=off"]

        if request in html_requests:
            header = self.ok_header("text/html", 60)
            response = self.create_html_response()
        elif request in posts:
            header = "HTTP/1.1 204 No content\r\n\r\n"
            response = ""
        elif "//" in request:
            header = "HTTP/1.1 301 Moved Permanently\r\nLocation: /\r\n\r\n"
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

        if "/water=auto" in request:
            self.water_setting = WaterSettings.auto
        elif "/water=on" in request:
            self.water_setting = WaterSettings.on
        elif "/water=off" in request:
            self.water_setting = WaterSettings.off

        return header, response

    def create_html_response(self):
        response = self.pages["html"]
        for r in self.system_status:
            response = response.replace(r, str(self.system_status[r]))
        return response

    @staticmethod
    def ok_header(content_type, max_age):
        return f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nCache-Control: max-age={max_age}\r\n\r\n"
