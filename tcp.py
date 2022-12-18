import socket, ssl


class FalconHttps:
    def __init__(self):
        self.BufferSize = 4096
        self.Example()                                             
       
    def ParseRequest(self,Method : str,host : str,url: str, headers: dict,PostData : str, cookies={}) -> bytes:
        Method = Method.upper()
        Request = f'{Method} {url} HTTP/1.1\r\n'
        Headers = ''
        cookie = ''
        for key, value in headers.items():
            Headers += f"{key}: {value}\r\n"
        if 'Host' not in Headers.lower():
            Request += f"Host: {host}\r\n"
        if cookies:
            for key, value in cookies.items():
                cookie += f"{key}={value};"
            Headers += f"Cookie: {cookie}\r\n"
        if "Content-Length" not in Headers.lower():
                    Request += f"Content-Length: {len(PostData)}\r\n"
        if "Connection" not in Headers.lower():
            Request += f"Connection: close\r\n"
        if "Content-Type" not in Headers.lower():
            Request += f"Content-Type: application/x-www-form-urlencoded\r\n"
        Request += f"{Headers}\r\n"
        if Method == "POST":
            Request += PostData
        return bytes(Request, 'utf8')

    def Connect(self,Server):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            s.connect(Server)
            return s

    def SSL_Factory(self,Sockets , Host,Packets):
            Body = ""
            Context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)  
            client = Context.wrap_socket(Sockets, server_hostname=Host)
            client.send(Packets)
            while True:
                self.bufferBytes = client.recv(self.BufferSize)
                response = self.bufferBytes.decode()
                Body += response
                if len(self.bufferBytes) == 0:
                    client.close()
                    Sockets.close()
                    break
            return Body

    def SendRequest(self,method:str,Host:str,port : int , Endpoint:str,headers:dict,PostData:str,Cookies={}):
            packets = self.ParseRequest(method,Host,Endpoint,headers,PostData,Cookies) 
            return self.SSL_Factory(self.Connect((Host,port)),Host,packets)

    def Example(self):
        Response = self.SendRequest("post","i.instagram.com",443,"/api/v1/users/lookup/",{
        "X-Ig-App-Id":"567067343352427",
        "User-Agent":"Instagram 177.0.0.30.119 Android (21/5.0.2; 240dpi; 540x960; samsung; SM-G530H; fortunave3g; qcom; en_GB; 276028020)",
        },"q=kkk0",None)
        print(Response)
        input()

    
FalconHttps()
