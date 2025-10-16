section .data
  format_out: db "%d", 10, 0 ; format do printf
  format_in: db "%d", 0 ; format do scanf
  scan_int: dd 0 ; 32-bits integer

section .text
  extern printf ; usar _printf para Windows
  extern scanf ; usar _scanf para Windows
  ; extern _ExitProcess@4 ; usar para Windows
  global _start ; início do programa

_start:
  push ebp ; guarda o EBP
  mov ebp, esp ; zera a pilha

sub esp, 4
mov eax, 0
mov [ebp-4], eax
if_11:
mov eax, 0
push eax
mov eax, [ebp-4]
pop ecx
cmp eax, ecx
mov ecx, 1
mov eax, 0
cmove eax, ecx
cmp eax, 0
je exit_11
mov eax, 1
mov [ebp-4], eax
exit_11:
mov eax, [ebp-4]
push eax
push format_out
call printf
add esp, 8
mov eax, 3
push eax
push format_out
call printf
add esp, 8
        
mov esp, ebp ; reestabelece a pilha
pop ebp

; chamada da interrupcao de saida (Linux)
mov eax, 1
xor ebx, ebx
int 0x80
