from http.server import HTTPServer,BaseHTTPRequestHandler     
import io,shutil,json,time,socket,socketserver,threading

# 并行server
class MyThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):  
    pass 
class HTTPServerV6(MyThreadingHTTPServer):
  address_family = socket.AF_INET6

class MyHttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        readdata = self.rfile.read(length).decode('utf-8')
        post_data = json.loads(readdata)
        cur_thread = threading.current_thread()
        #time.sleep(5)
        # 服务器操作处理
        print(cur_thread.name)
        print(post_data)
        data = json.dumps({'name':'wak'})
        enc="UTF-8"  
        encoded = ''.join(data).encode(enc)  
        f = io.BytesIO()  
        f.write(encoded)  
        f.seek(0)  
        self.send_response(200)  
        self.send_header("Content-type", "text/html; charset=%s" % enc)  
        self.send_header("Content-Length", str(len(encoded)))  
        self.end_headers()  
        shutil.copyfileobj(f,self.wfile)
    
httpd=HTTPServerV6(('::',9601),MyHttpHandler)     
print("Server started on 127.0.0.1,port 9601......")     
httpd.serve_forever() 
