#-*- coding:utf-8 -*-
# coding=utf-8
import sys
import frida

pid = sys.argv[1]
module = sys.argv[2]
offset = sys.argv[3]
device = frida.get_usb_device()
session = device.attach(pid)
print("pid :" + pid)
print("module :" + module)
print("offset :" + offset)
src = """
var base = Module.findBaseAddress("%s");
var pos = base.add(ptr(%d))
Interceptor.attach(pos, {
    onEnter: function (args) {
        console.log("backtrace: \\n" +
        Thread.backtrace(this.context , Backtracer.FUZZY).
        map(DebugSymbol.fromAddress).join("\\n") + "\\n");
    }
});
""" % (module, int(offset, 16))


def on_message(message, data):
    print(message)


print(src)
script = session.create_script(src)
script.on("message", on_message)

script.load()

sys.stdin.read()
