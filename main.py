import rotaryio
import board
import digitalio
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import adafruit_debouncer

sda_pin = board.D0
scl_pin = board.D1
b_pin = board.D2

button_pin = digitalio.DigitalInOut(b_pin)
button_pin.direction = digitalio.Direction.INPUT
button_pin.pull = digitalio.Pull.UP

button = adafruit_debouncer.Button( button_pin, value_when_pressed=False )
encoder = rotaryio.IncrementalEncoder(sda_pin, scl_pin)
cc = ConsumerControl(usb_hid.devices)
last_position = encoder.position

while True:
    button.update()
    current_position = encoder.position
    position_change = current_position - last_position
    if position_change > 0:
        for _ in range(position_change):
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        print(current_position)
    elif position_change < 0:
        for _ in range(-position_change):
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        print(current_position)
    last_position = current_position

    if button.short_count == 1:
        cc.send(ConsumerControlCode.PLAY_PAUSE)
    elif button.short_count == 2:
        cc.send(ConsumerControlCode.MUTE)
