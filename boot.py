import storage

storage.remount("/", readonly=False)

m = storage.getmount("/")
m.label = "ROTARY_PI"

storage.remount("/", readonly=True)

storage.enable_usb_drive()