sub esp, 4
push scan_int
push format_in
call scanf
add esp 8
mov eax, dword [scan_int]
mov [ebp-4], eax

let x:number;
x = readline();