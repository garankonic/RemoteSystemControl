#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse
from RemoteSystem_Genius_SW_HF_51_6000 import *

class GetHandler(BaseHTTPRequestHandler):

    # here we specify all used remote systems
    remote_systems = []
    remote_systems.append(RemoteSystem_Genius_SW_HF_51_6000())

    def do_GET(self):
        device_name = ""
        command = ""
        parameter = ""
        value = ""

        # process command
        parsed_path = urlparse.urlparse(self.path)
        if (parsed_path.path[1:] == "remote_control"):
            request = urlparse.parse_qs(parsed_path.query)
            for key in request:
                #print key, 'corresponds to', request[key]
                if key == "device":
                    device_name = request[key][0]
                elif key == "command":
                    command = request[key][0]
                elif key == "parameter":
                    parameter = request[key][0]
                elif key == "value":
                    value = request[key][0]
                    print value

        message_parts = []
        for device in self.remote_systems:
            if device.GetName() == device_name:
                if command == "status":
                    message_parts = device.GetStatus()
                elif command == "get_value":
                    message_parts.append("%s=%d" % (parameter, device.GetInterface().GetButton(parameter).GetValue()))
                elif command == "set_value":
                    button = device.GetInterface().GetButton(parameter)
                    button.SetValue(int(value))
                    message_parts.append("%s=%d" % (parameter, button.GetValue()))
                elif command == "toogle":
                    button = device.GetInterface().GetButton(parameter)
                    button.Toogle()
		    if parameter == "reset":
			message_parts = device.GetStatus()
		    else:
                    	message_parts.append("%s=%d" % (parameter, button.GetValue()))

        # response starts here
	message_parts.append('')
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)
        return

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('', 8080), GetHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
