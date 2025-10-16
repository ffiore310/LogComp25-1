mov eax, 7
push eax
mov eax, 5
push eax
mov eax, 4
pop ecx
imul ecx
push eax
mov eax, 3
pop ecx
add eax, ecx
pop ecx
sub eax, ecx
push eax
push format_out
call printf
add esp, 8
mov eax, 6
neg eax
push eax
push format_out
call printf
add esp, 8


log(3+4*5-7);
log(-6);