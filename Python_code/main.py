import sensor, time, image, pyb
from pyb import LED,  Pin, Timer
sensor.reset().

tim = pyb.Timer(4, freq=1000)
p0 = pyb.Pin(pyb.Pin.board.P0, pyb.Pin.OUT_PP)
p7 = tim.channel(1, pyb.Timer.PWM, pin=pyb.Pin("P7"))

sensor.set_contrast(3)
sensor.set_gainceiling(16)
sensor.set_framesize(sensor.VGA)
sensor.set_windowing((220, 190, 200, 100))
sensor.set_pixformat(sensor.GRAYSCALE)
eyes_cascade = image.HaarCascade("eye", stages=12)
print(eyes_cascade)
red_led   = LED(1)
green_led = LED(2)
clock = time.clock()
while (True):
    clock.tick()
    img = sensor.snapshot()
    eyes = img.find_features(eyes_cascade, threshold=0.5, scale_factor=1.5)
    for e in eyes:
        iris = img.find_eye(e)
        img.draw_rectangle(e[0], e[1],e[2]+30, e[3]+30)
        img.draw_cross(iris[0], iris[1])
        mid1 = (e[2]/2 + e[3]/2) - 25
        mid2 = (e[2]/2 + e[3]/2) + 25
        if e[0] < mid1:
            red_led.on()
            green_led.off()
            print("RED")
            img.draw_string(0,0, "right", (0,0,255))
            p0.value(0)
            p7.pulse_width_percent(30)
        if e[0] > mid2:
            red_led.off()
            green_led.on()
            print("GREEN")
            img.draw_string(0,0, "left", (0,0,255))
            p0.value(0)
            p7.pulse_width_percent(30)
        if e[0] > mid1:
            if e[0] < mid2:
                red_led.off()
                green_led.off()
                print("MIDPOINT")
                img.draw_string(0,0, "MIDPOINT")
                p7.pulse_width_percent(0)
                p0.value(0)
