# LogComp25-1

[![Compilation Status](https://compiler-tester.insper-comp.com.br/svg/ffiore310/LogComp25-1)](https://compiler-tester.insper-comp.com.br/svg/ffiore310/LogComp25-1)

Repositório privado para o desenvolvimento do projeto e dos roteiros relacionados a matéria de Lógica da Computação 

### Diagrama sintático do Projeto
<img width="467" height="361" alt="image" src="https://github.com/user-attachments/assets/b1807032-4559-436d-a5d7-c3fb1d5cd526" />

## Gramática EBNF

```ebnf
programa       = { declaracao } EOF ;

declaracao     = acao ";"
               | atribuicao ";"
               | if_stmt
               | while_stmt
               | comentario
               ;

acao           = "ir"
               | "abrir"
               | "fechar"
               | "abrir" "por" tempo
               | "adicionar" "andar" andar
               | "limpar" "andares"
               | "parar"
               | "campainha"
               | "anunciar" string
               | "esperar" tempo
               ;

atribuicao     = "set" "modo" "=" modo
               | "set" "andar_destino" "=" andar
               ;

if_stmt        = "se" condicao ":" bloco [ "senao" ":" bloco ] ;

while_stmt     = "enquanto" loop_cond ":" bloco ;

bloco          = "{" { declaracao } "}" ;

(* --- Condições --- *)
condicao       = sensor_cond
               | comparacao                (* ex.: andar_destino == andar_atual *)
               ;

sensor_cond    = "lotado"
               | "porta_bloqueada"
               | "emergencia"
               | "porta_aberta"
               | "fila_vazia"
               | "ha_destino"
               | "primeiro_andar"
               | "ultimo_andar"
               ;

comparacao     = lado_esq comparador lado_dir ;

lado_esq       = "andar_atual" | "andar_destino" | "modo" ;
lado_dir       = "andar_atual" | "andar_destino" | "modo" | andar | modo ;

comparador     = "==" | "!=" | "<" | "<=" | ">" | ">=" ;

(* --- Loops suportados --- *)
loop_cond      = "fila_nao_vazia"
               | ( "modo" "==" modo )     (* ex.: enquanto modo == livre *)
               ;

andar          = "T" | numero ;
tempo          = numero "s" ;

modo           = "normal" | "servico" | "livre" | numero ;

comentario     = "#" { caractere_que_nao_quebra_linha } ( "\n" | EOF ) ;

string         = "\"" { caractere_sem_aspas_ou_escape | escape } "\"" ;
escape         = "\\" ( "\"" | "\\" | "n" | "t" ) ;

numero         = [ "+" | "-" ]? DIGITO { DIGITO } ;
DIGITO         = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
```
