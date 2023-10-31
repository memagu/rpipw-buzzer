import machine
import network
import urequests
import usocket
from time import sleep

from picozero import pico_led, Buzzer

SSID_1 = ""
PASSWORD_1 = ""
SSID_2 = ""
PASSWORD_2 = ""
HOSTNAME = ""
PORT = 1944
TIMEOUT_SECONDS = 10
POLL_INTERVAL_SECONDS = 30
LED_PULSE_DURATION = 0.5
BUZZER_PIN = 7
BUZZER_PATTERN = 0b00000010110110010110010100101101
BUZZER_PATTERN_SIZE = 32
BUZZER_PATTERN_DURATION_SECONDS = 2
BUZZER_PATTERN_REPETITIONS = 5


def play_pattern(buzzer: Buzzer, pattern: int, pattern_size: int, duration_seconds: int, repetitions: int) -> None:
    for _ in range(repetitions):
        for bit_pos in range(pattern_size):
            if (pattern >> bit_pos) & 1:
                buzzer.on()
            else:
                buzzer.off()

            sleep(duration_seconds / pattern_size)

    buzzer.off()


def connect_wifi(ssid: str, password: str, timeout_seconds: int) -> str:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    for second in range(timeout_seconds):
        if wlan.isconnected():
            print(f"Successfully connected to {ssid}")
            return wlan.ifconfig()[0]

        print(f"Connecting to {ssid} ...")
        pico_led.off()
        sleep(LED_PULSE_DURATION)
        pico_led.on()
        sleep(LED_PULSE_DURATION)

    raise Exception("Wifi connection took to long")


def get_action(hostname: str, port: int) -> str:
    host = usocket.getaddrinfo(hostname, 80)[0][-1][0]
    request_address = f"http://{host}:{port}/api/get_action"
    print(f'Sending get request to "{request_address}"')
    response = urequests.get(request_address)

    print(response.status_code)
    if response.status_code != 200:
        return ''

    print(response.text)
    return response.text


def main():
    try:
        connect_wifi(SSID_1, PASSWORD_1, TIMEOUT_SECONDS)
    except Exception:
        connect_wifi(SSID_2, PASSWORD_2, TIMEOUT_SECONDS)

    buzzer = Buzzer(BUZZER_PIN)

    while True:
        action = get_action(HOSTNAME, PORT)
        print(f'Received action: "{action}"')

        if action == "kill":
            raise Exception("Killed by server.")

        if action == "beep":
            play_pattern(buzzer, BUZZER_PATTERN, BUZZER_PATTERN_SIZE, BUZZER_PATTERN_DURATION_SECONDS,
                         BUZZER_PATTERN_REPETITIONS)
            # buzzer.beep(LED_PULSE_DURATION, LED_PULSE_DURATION, BUZZER_PULSE_AMOUNT)

        sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        machine.reset()

