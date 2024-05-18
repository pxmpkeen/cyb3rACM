import socketserver
import struct

class SyslogHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        if not data:
            return

        # Parse syslog message header (assuming UDP)
        facility, severity, timestamp = struct.unpack('!BBH', data[:7])
        print(f"Facility: {facility}, Severity: {severity}, Timestamp: {timestamp}")
        message = data[7:].decode('utf-8').strip()
        print(message)

if __name__ == '__main__':
    HOST, PORT = '0.0.0.0', 514  # Standard syslog port

    with socketserver.UDPServer((HOST, PORT), SyslogHandler) as server:
        print(f"Syslog server listening on {HOST}:{PORT}")
        server.serve_forever()
