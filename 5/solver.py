from pwn import *
from Crypto.Util.Padding import unpad, pad

HOST = 'localhost'
PORT = 1337

p = remote(HOST, PORT)

p.sendlineafter(b">> ", b"2")
p.recvuntil(b"Encrypted Message (hex): ")
ef = unhex(p.recvline().strip())
log.info(f"flag yang di encrypt: {ef.hex()}, len: {len(ef)}")

p.sendlineafter(b">> ", b"1")
inputs = b"0"
p.sendlineafter(b"Message: ", inputs)
p.recvuntil(b"Encrypted Message (hex): ")
em = unhex(p.recvline().strip())
log.info(f"input yang di encrypt: {em.hex()} len: {len(em)}")

padded_inputs = pad(inputs, 16)

keystream = xor(padded_inputs, em)

xor_flag = xor(ef, keystream)

unpadded_flag = unpad(xor_flag, 16)

log.success(f"flag: {unpadded_flag.decode()}")

p.interactive()
