import requests, random, json, secrets, base64, time, execjs, re, string, hashlib, os
from urllib.parse import urlsplit
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from PIL import Image
from io import BytesIO
from Crypto.Cipher import AES



class Funcaptcha:
    def __init__(self, api_url, api_key, site_url):
        self.base_url = api_url,
        self.site_key = api_key,
        self.site_url = site_url

        self.session = requests.Session()
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
        
        if not os.path.exists("./fingerprint.js"):
            self.get_js()
            
        self.pyjs = execjs.compile(open("./fingerprint.js"))
        
    def get_js(self):
        javascript = """
var x64Add=function(t,r){t=[t[0]>>>16,65535&t[0],t[1]>>>16,65535&t[1]],r=[r[0]>>>16,65535&r[0],r[1]>>>16,65535&r[1]];var o=[0,0,0,0];return o[3]+=t[3]+r[3],o[2]+=o[3]>>>16,o[3]&=65535,o[2]+=t[2]+r[2],o[1]+=o[2]>>>16,o[2]&=65535,o[1]+=t[1]+r[1],o[0]+=o[1]>>>16,o[1]&=65535,o[0]+=t[0]+r[0],o[0]&=65535,[o[0]<<16|o[1],o[2]<<16|o[3]]},x64Multiply=function(t,r){t=[t[0]>>>16,65535&t[0],t[1]>>>16,65535&t[1]],r=[r[0]>>>16,65535&r[0],r[1]>>>16,65535&r[1]];var o=[0,0,0,0];return o[3]+=t[3]*r[3],o[2]+=o[3]>>>16,o[3]&=65535,o[2]+=t[2]*r[3],o[1]+=o[2]>>>16,o[2]&=65535,o[2]+=t[3]*r[2],o[1]+=o[2]>>>16,o[2]&=65535,o[1]+=t[1]*r[3],o[0]+=o[1]>>>16,o[1]&=65535,o[1]+=t[2]*r[2],o[0]+=o[1]>>>16,o[1]&=65535,o[1]+=t[3]*r[1],o[0]+=o[1]>>>16,o[1]&=65535,o[0]+=t[0]*r[3]+t[1]*r[2]+t[2]*r[1]+t[3]*r[0],o[0]&=65535,[o[0]<<16|o[1],o[2]<<16|o[3]]},x64Rotl=function(t,r){return 32===(r%=64)?[t[1],t[0]]:r<32?[t[0]<<r|t[1]>>>32-r,t[1]<<r|t[0]>>>32-r]:(r-=32,[t[1]<<r|t[0]>>>32-r,t[0]<<r|t[1]>>>32-r])},x64LeftShift=function(t,r){return 0===(r%=64)?t:r<32?[t[0]<<r|t[1]>>>32-r,t[1]<<r]:[t[1]<<r-32,0]},x64Xor=function(t,r){return[t[0]^r[0],t[1]^r[1]]},x64Fmix=function(t){return t=x64Xor(t,[0,t[0]>>>1]),t=x64Multiply(t,[4283543511,3981806797]),t=x64Xor(t,[0,t[0]>>>1]),t=x64Multiply(t,[3301882366,444984403]),t=x64Xor(t,[0,t[0]>>>1])},x64hash128=function(t,r){r=r||0;for(var o=(t=t||"").length%16,e=t.length-o,x=[0,r],c=[0,r],a=[0,0],h=[0,0],i=[2277735313,289559509],d=[1291169091,658871167],l=0;l<e;l+=16)a=[255&t.charCodeAt(l+4)|(255&t.charCodeAt(l+5))<<8|(255&t.charCodeAt(l+6))<<16|(255&t.charCodeAt(l+7))<<24,255&t.charCodeAt(l)|(255&t.charCodeAt(l+1))<<8|(255&t.charCodeAt(l+2))<<16|(255&t.charCodeAt(l+3))<<24],h=[255&t.charCodeAt(l+12)|(255&t.charCodeAt(l+13))<<8|(255&t.charCodeAt(l+14))<<16|(255&t.charCodeAt(l+15))<<24,255&t.charCodeAt(l+8)|(255&t.charCodeAt(l+9))<<8|(255&t.charCodeAt(l+10))<<16|(255&t.charCodeAt(l+11))<<24],a=x64Multiply(a,i),a=x64Rotl(a,31),a=x64Multiply(a,d),x=x64Xor(x,a),x=x64Rotl(x,27),x=x64Add(x,c),x=x64Add(x64Multiply(x,[0,5]),[0,1390208809]),h=x64Multiply(h,d),h=x64Rotl(h,33),h=x64Multiply(h,i),c=x64Xor(c,h),c=x64Rotl(c,31),c=x64Add(c,x),c=x64Add(x64Multiply(c,[0,5]),[0,944331445]);switch(a=[0,0],h=[0,0],o){case 15:h=x64Xor(h,x64LeftShift([0,t.charCodeAt(l+14)],48));case 14:h=x64Xor(h,x64LeftShift([0,t.charCodeAt(l+13)],40));case 13:h=x64Xor(h,x64LeftShift([0,t.charCodeAt(l+12)],32));case 12:h=x64Xor(h,x64LeftShift([0,t.charCodeAt(l+11)],24));case 11:h=x64Xor(h,x64LeftShift([0,t.charCodeAt(l+10)],16));case 10:h=x64Xor(h,x64LeftShift([0,t.charCodeAt(l+9)],8));case 9:h=x64Xor(h,[0,t.charCodeAt(l+8)]),h=x64Multiply(h,d),h=x64Rotl(h,33),h=x64Multiply(h,i),c=x64Xor(c,h);case 8:a=x64Xor(a,x64LeftShift([0,t.charCodeAt(l+7)],56));case 7:a=x64Xor(a,x64LeftShift([0,t.charCodeAt(l+6)],48));case 6:a=x64Xor(a,x64LeftShift([0,t.charCodeAt(l+5)],40));case 5:a=x64Xor(a,x64LeftShift([0,t.charCodeAt(l+4)],32));case 4:a=x64Xor(a,x64LeftShift([0,t.charCodeAt(l+3)],24));case 3:a=x64Xor(a,x64LeftShift([0,t.charCodeAt(l+2)],16));case 2:a=x64Xor(a,x64LeftShift([0,t.charCodeAt(l+1)],8));case 1:a=x64Xor(a,[0,t.charCodeAt(l)]),a=x64Multiply(a,i),a=x64Rotl(a,31),a=x64Multiply(a,d),x=x64Xor(x,a)}return x=x64Xor(x,[0,t.length]),c=x64Xor(c,[0,t.length]),x=x64Add(x,c),c=x64Add(c,x),x=x64Fmix(x),c=x64Fmix(c),x=x64Add(x,c),c=x64Add(c,x),("00000000"+(x[0]>>>0).toString(16)).slice(-8)+("00000000"+(x[1]>>>0).toString(16)).slice(-8)+("00000000"+(c[0]>>>0).toString(16)).slice(-8)+("00000000"+(c[1]>>>0).toString(16)).slice(-8)};function fc1(t){for(var r,o=2,e=1;1377706320!==B5X.l5P(e.toString(),e.toString().length,76698);e++)r=t.value,o+=2;-442158380!==B5X.l5P(o.toString(),o.toString().length,82275)&&(r=t.value),typeof t.value.join!==B5X.D0i(219)&&(r=t.value.join(B5X.w0i(82))),N4D.push(r)}"""
        with open('fingerprint.js', 'a') as file:
            file.write(javascript.strip())

    @staticmethod
    def _encrypt(data, key):
        # Padding
        data = data + chr(16 - len(data) % 16) * (16 - len(data) % 16)

        salt = b"".join(random.choice(string.ascii_lowercase).encode() for x in range(8))
        salted, dx = b"", b""
        while len(salted) < 48:
            dx = hashlib.md5(dx + key.encode() + salt).digest()
            salted += dx

        key = salted[:32]
        iv = salted[32:32 + 16]
        aes = AES.new(key, AES.MODE_CBC, iv)

        encrypted_data = {"ct": base64.b64encode(aes.encrypt(data.encode())).decode("utf-8"), "iv": iv.hex(), "s": salt.hex()}
        return json.dumps(encrypted_data, separators=(',', ':'))

    @staticmethod
    def _decrypt(data, key):
        data = json.loads(data)
        dk = key.encode() + bytes.fromhex(data["s"])

        md5 = [hashlib.md5(dk).digest()]
        result = md5[0]
        for i in range(1, 3 + 1):
            md5.insert(i, hashlib.md5((md5[i - 1] + dk)).digest())
            result += md5[i]

        aes = AES.new(result[:32], AES.MODE_CBC, bytes.fromhex(data["iv"]))
        data = aes.decrypt(base64.b64decode(data["ct"]))
        return data

    def get_browser_data(self):
        ts = time.time()
        timeframe = int(ts - (ts % 21600))
        key = self.user_agent + str(timeframe)

        data = []
        data.append({"key": "api_type", "value": "js"})
        data.append({"key": "p", "value": 1})

        fonts = "Arial,Arial Black,Arial Narrow,Book Antiqua,Bookman Old Style,Calibri,Cambria,Cambria Math,Century,Century Gothic,Century Schoolbook,Comic Sans MS,Consolas,Courier,Courier New,Garamond,Georgia,Helvetica,Impact,Lucida Bright,Lucida Calligraphy,Lucida Console,Lucida Fax,Lucida Handwriting,Lucida Sans,Lucida Sans Typewriter,Lucida Sans Unicode,Microsoft Sans Serif,Monotype Corsiva,MS Gothic,MS PGothic,MS Reference Sans Serif,MS Sans Serif,MS Serif,Palatino Linotype,Segoe Print,Segoe Script,Segoe UI,Segoe UI Light,Segoe UI Semibold,Segoe UI Symbol,Tahoma,Times,Times New Roman,Trebuchet MS,Verdana,Wingdings,Wingdings 2,Wingdings 3".split(",")
        plugins = "Chrome PDF Plugin,Chrome PDF Viewer,Native Client".split(",")
        canvas_fp = -1424337346

        fe = [
            "DNT:unknown", "L:en-US", "D:24", "PR:1", "S:1920,1080", "AS:1920,1040", "TO:-120", "SS:true", "LS:true", "IDB:true", "B:false", "ODB:true", "CPUC:unknown", "PK:Win32", f"CFP:{str(canvas_fp)}", "FR:false", "FOS:false", "FB:false", f"JSF:{', '.join(fonts)}", f"P:{', '.join(plugins)}", "T:0,false,false", "H:8", "SWF:false"
        ]

        fp = secrets.token_hex(16)
        ife_hash = self.pyjs.call("x64hash128", ", ".join(fe), 38)
        wh = secrets.token_hex(16) + "|" + secrets.token_hex(16)

        data.append({"key": "f", "value": fp})
        data.append({"key": "n", "value": base64.b64encode(str(int(ts)).encode("utf-8")).decode("utf-8")})
        data.append({"key": "wh", "value": wh})
        data.append({"key": "fe", "value": fe})
        data.append({"key": "ife_hash", "value": ife_hash})
        data.append({"key": "cs", "value": 1})
        data.append({"key": "jsbd", "value": '{"HL":28,"NCE":true,"DA":null,"DR":null,"DMT":31,"DO":null,"DOT":31}'})

        data = json.dumps(data, separators=(',', ':'))
        data = Funcaptcha._encrypt(data, key)
        data = base64.b64encode(data.encode("utf-8")).decode("utf-8")
        return data

    def get_request_id(self, session_token):
        key = f"REQUESTED{session_token}ID"
        data = json.dumps(self.metadata, separators=(',', ':'))
        return Funcaptcha._encrypt(data, key)

    def getkey(self):

        bda_value = self.get_browser_data()

        nc_resp = self.session.post(
            url=f"https://client-api.arkoselabs.com/fc/gt2/public_key/{self.site_key}",
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": self.site_url,
                "Referer": self.site_url
            },
            data={
                "bda": bda_value,
                "public_key": self.site_key,
                "site": self.site_url,
                "userbrowser": self.user_agent,
                "simulate_rate_limit": 0,
                "simulated": 0,
                "language": "en",
                "rnd": random.uniform(0, 1)
            }
        )

        full_token = nc_resp.json()["token"] if 'token' in nc_resp.text else print(' [ x ] Error getting token')

        """
        session_token = full_token.split('|')[0]
        region = full_token.split('|')[1].split("=")[1]
        lang = full_token.split('|')[4].split("=")[1]
        analytics_tier = full_token.split('|')[6].split("=")[1]
        """

        return full_token