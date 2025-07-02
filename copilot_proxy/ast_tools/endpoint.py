#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import threading
import json
import platform


class ReadPipe(threading.Thread):

    def __init__(self, pipe):
        threading.Thread.__init__(self)
        self.pipe = pipe

    def run(self):
        line = self.pipe.readline().decode('utf-8')
        while line:
            print(line)
            line = self.pipe.readline().decode('utf-8')


JSON_RPC_REQ_FORMAT = "Content-Length: {json_string_len}\r\n\r\n{json_string}"
LEN_HEADER = "Content-Length: "
TYPE_HEADER = "Content-Type: "
LANGUAGE_LIST = ["python", "c", "javascript", "typescript", "golang", "java", "cpp", "csharp", "rust"]


class MyEncoder(json.JSONEncoder):
    """
    Encodes an object in JSON
    """

    def default(self, o):  # pylint: disable=E0202
        return o.__dict__


class JsonRpcEndpoint(object):
    '''
    Thread safe JSON RPC endpoint implementation. Responsible to recieve and send JSON RPC messages, as described in the
    protocol. More information can be found: https://www.jsonrpc.org/
    '''

    def __init__(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout
        self.read_lock = threading.Lock()
        self.write_lock = threading.Lock()

    @staticmethod
    def __add_header(json_string):
        '''
        Adds a header for the given json string

        :param str json_string: The string
        :return: the string with the header
        '''
        return JSON_RPC_REQ_FORMAT.format(json_string_len=len(json_string), json_string=json_string)

    def send_request(self, message):
        '''
        Sends the given message.

        :param dict message: The message to send.
        '''
        json_string = json.dumps(message, cls=MyEncoder)
        jsonrpc_req = self.__add_header(json_string)
        with self.write_lock:
            self.stdin.write(jsonrpc_req.encode())
            self.stdin.flush()

    def recv_response(self):
        '''
        Recives a message.

        :return: a message
        '''
        with self.read_lock:
            message_size = None
            while True:
                # read header
                line = self.stdout.readline()
                if not line:
                    # server quit
                    return None
                line = line.decode("utf-8")
                if not line.endswith("\r\n"):
                    raise Exception("Bad header: missing newline")
                # remove the "\r\n"
                line = line[:-2]
                if line == "":
                    # done with the headers
                    break
                elif line.startswith(LEN_HEADER):
                    line = line[len(LEN_HEADER):]
                    if not line.isdigit():
                        raise Exception("Bad header: size is not int")
                    message_size = int(line)
                elif line.startswith(TYPE_HEADER):
                    # nothing todo with type for now.
                    pass
                else:
                    raise Exception("Bad header: unkown header")
            if not message_size:
                raise Exception("Bad header: missing size")

            jsonrpc_res = self.stdout.read(message_size).decode("utf-8")
            return json.loads(jsonrpc_res)


class MyEndpoint(threading.Thread):
    def __init__(self, json_rpc_endpoint, timeout=2):
        threading.Thread.__init__(self)
        self.json_rpc_endpoint = json_rpc_endpoint
        self.event_dict = {}
        self.response_dict = {}
        self.next_id = 0
        self._timeout = timeout
        self.shutdown_flag = False

    def stop(self):
        self.json_rpc_endpoint.send_request({
            "method": "exit"
        })
        self.shutdown_flag = True

    def handle_result(self, rpc_id, result, error):
        self.response_dict[rpc_id] = (result, error)
        cond = self.event_dict[rpc_id]
        cond.acquire()
        cond.notify()
        cond.release()

    def send_message(self, method_name, params, new_id=None):
        message_dict = {}
        # message_dict["jsonrpc"] = "2.0"
        if new_id is not None:
            message_dict["id"] = new_id
        message_dict["method"] = method_name
        message_dict["params"] = params
        self.json_rpc_endpoint.send_request(message_dict)

    def call_method(self, method_name, params):
        current_id = self.next_id
        self.next_id += 1
        cond = threading.Condition()
        self.event_dict[current_id] = cond

        cond.acquire()
        self.send_message(method_name, params, current_id)
        if self.shutdown_flag:
            return None

        if not cond.wait(timeout=self._timeout):
            raise TimeoutError()
        cond.release()

        self.event_dict.pop(current_id)
        result, error = self.response_dict.pop(current_id)
        if error:
            raise Exception(f"{error.get('code')}, {error.get('message')}, {error.get('data')}")
        return result

    def run(self):
        while not self.shutdown_flag:
            # print("agent loop")
            try:
                jsonrpc_message = self.json_rpc_endpoint.recv_response()
                if jsonrpc_message is None:
                    print("server quit")
                    break
                # method = jsonrpc_message.get("method")
                result = jsonrpc_message.get("result")
                error = jsonrpc_message.get("error")
                rpc_id = jsonrpc_message.get("id")
                # params = jsonrpc_message.get("params")

                # print(jsonrpc_message, end='\n\n')

                self.handle_result(rpc_id, result, error)

                if isinstance(error, dict) and (error.get("code") == -1):
                    print("server exit")
                    break

            except Exception as e:
                # self.send_response(rpc_id, None, e)
                print(f"get error: {e}")


def get_endpoint(language: str, code, cursor_position):
    language = language.lower()
    if language not in LANGUAGE_LIST:
        return {'astResult': '(ERROR)'}
    if platform.system().lower() == 'windows':
        cmd = ["ast_tools\\cmd\\ast-rs.exe"]
    else:
        cmd = ["ast_tools/cmd/ast-rs"]
    p = subprocess.Popen(cmd,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    read_pipe = ReadPipe(p.stderr)
    read_pipe.start()

    json_rpc_endpoint = JsonRpcEndpoint(p.stdin, p.stdout)

    endpoint = MyEndpoint(json_rpc_endpoint)
    endpoint.start()
    result = endpoint.call_method("ParseAstInRange", {
        "language": language,
        "code": code,
        "cursorPosition": cursor_position
    })
    endpoint.stop()

    return result
