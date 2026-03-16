import socket
import time
from machine import Pin

import config
from webpage import WEBPAGE


state = "NA"

led = Pin(config.LED_PIN, Pin.OUT)
dir_pin = Pin(config.DIR_PIN, Pin.OUT)
step_pin = Pin(config.STEP_PIN, Pin.OUT)


def parse_request_line(line):
    try:
        method, path, _ = line.split(" ", 2)
    except ValueError:
        return None, None
    return method, path


def parse_query(path):
    if "?" not in path:
        return path, {}
    base, query = path.split("?", 1)
    params = {}
    for pair in query.split("&"):
        if not pair:
            continue
        if "=" in pair:
            key, value = pair.split("=", 1)
        else:
            key, value = pair, ""
        params[key] = value
    return base, params


def clamp_steps(value):
    try:
        steps = int(value)
    except (TypeError, ValueError):
        return 100
    if steps < config.STEPS_MIN or steps > config.STEPS_MAX:
        return 100
    return steps


def move_engine(steps):
    for _ in range(steps):
        step_pin.value(1)
        time.sleep_ms(config.STEP_DELAY_MS)
        step_pin.value(0)
        time.sleep_ms(config.STEP_DELAY_MS)


def response(conn, status, content_type, body):
    conn.send("HTTP/1.1 {}\r\n".format(status))
    conn.send("Content-Type: {}\r\n".format(content_type))
    conn.send("Connection: close\r\n\r\n")
    conn.send(body)


def handle_root(conn):
    response(conn, "200 OK", "text/html", WEBPAGE)


def handle_valve(conn, desired_state, steps):
    global state
    if desired_state == "open":
        led.value(1)
        dir_pin.value(1)
        state = "ABIERTA"
    else:
        led.value(0)
        dir_pin.value(0)
        state = "CERRADA"
    move_engine(steps)
    response(conn, "200 OK", "text/plain", state)


def start_server():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    while True:
        conn, _ = s.accept()
        try:
            request_line = conn.readline().decode("utf-8")
            if not request_line:
                conn.close()
                continue
            method, path = parse_request_line(request_line)
            if method != "GET" or path is None:
                response(conn, "405 Method Not Allowed", "text/plain", "Method Not Allowed")
                conn.close()
                continue
            while True:
                header = conn.readline()
                if not header or header == b"\r\n":
                    break
            base_path, params = parse_query(path)
            if base_path == "/":
                handle_root(conn)
            elif base_path == "/valve_open":
                steps = clamp_steps(params.get("steps"))
                handle_valve(conn, "open", steps)
            elif base_path == "/valve_close":
                steps = clamp_steps(params.get("steps"))
                handle_valve(conn, "close", steps)
            else:
                response(conn, "404 Not Found", "text/plain", "Not Found")
        finally:
            conn.close()


def main():
    start_server()


main()
