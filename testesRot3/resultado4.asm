sub esp, 4
mov eax, 0
mov [ebp-4], eax
loop_13:
mov eax, 5
push eax
mov eax, [ebp-4]
pop ecx
cmp eax, ecx
mov ecx, 1
mov eax, 0
cmove eax, ecx
cmp eax, 0
je exit_13
mov eax, 1
push eax
mov eax, [ebp-4]
pop ecx
add eax, ecx
mov [ebp-4], eax
jmp loop_13
exit_13:

let x:number = 0;
while (x < 5){
    x = x + 1;
}