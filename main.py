import evdev
import lirc
import logging
import time

IR_INPUT_DEVICE_NAME = 'gpio_ir_recv'
LIRC_TX_REMOTE = 'smsl-ad18'
INTERVAL_FILTER_MS = 0.3
MAX_VALUE = 50000

# supported lirc keys
KEY_MUTE = 'KEY_MUTE'
KEY_POWER = 'KEY_POWER'
KEY_VOLUMEDOWN = 'KEY_VOLUMEDOWN'
KEY_VOLUMEUP = 'KEY_VOLUMEUP'

LOGGER = logging.getLogger(__name__)
LOG_LEVEL = logging.DEBUG
LOG_FILE = '/home/marty/pimote/pimote.log'

def init_logger():
  logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p', level=LOG_LEVEL, filename=LOG_FILE, encoding='utf-8', filemode='w')

def get_ir_device():
  devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
  for device in devices:
    LOGGER.debug(device)
    if (device.name == IR_INPUT_DEVICE_NAME):
      LOGGER.info('using %s', device)
      return device

def forward_remote_key(client, key_code):
  time.sleep(0.01)
  LOGGER.info('%s forwarded', key_code)
  client.send_once(LIRC_TX_REMOTE, key_code)

# main
def main():
  # setup
  init_logger()

  LOGGER.info('starting pimote')
  LOGGER.info('input device %s', IR_INPUT_DEVICE_NAME)
  LOGGER.info('output device %s', LIRC_TX_REMOTE)

  lirc_client = lirc.Client()

  if (lirc_client is None):
    raise Exception('lirc client not found')

  LOGGER.info('lirc_client %s', lirc_client)

  device = get_ir_device()

  if (device is None):
    error_message = f'{IR_INPUT_DEVICE_NAME} not found'
    LOGGER.error(error_message)
    raise Exception(error_message)

  LOGGER.info('waiting for input from %s', device)

  prev_timestamp = 0

  # main loop
  for event in device.read_loop():
    value = event.value

    # filter out zero values
    if (value == 0):
      continue

    if (value > MAX_VALUE):
      continue

    # filter out events that occur too quickly
    timestamp = event.timestamp()
    delta = timestamp - prev_timestamp
    if (delta < INTERVAL_FILTER_MS):
      continue

    LOGGER.debug(value)

    # update previous timestamp
    prev_timestamp = timestamp

    # listen to hisense remote, and forward corresponding smsl-ad18 keys
    if (value == 48964):
      forward_remote_key(lirc_client, KEY_VOLUMEUP)
    if (value == 48963):
      forward_remote_key(lirc_client, KEY_VOLUMEDOWN)
    if (value == 48909):
      # send_remote_key(lirc_client, KEY_POWER)
      LOGGER.debug('%s not forwarded', KEY_POWER)

if (__name__ == "__main__"):
  main()
