sub esp, 4
sub esp, 4
mov eax, 10
mov [ebp-4], eax
mov eax, 5
push eax
mov eax, [ebp-4]
pop ecx
sub eax, ecx
mov [ebp-8], eax

let x:number;
let y:number;
x = 10;
y = x - 5;