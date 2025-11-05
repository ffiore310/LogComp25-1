function inc(n:number):number {
  return n + 1;
}

let y:number;
y = inc("a");  // ERRO: argumento string passado onde se espera number

log(y);
