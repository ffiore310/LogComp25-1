function fact(n:number):number {
  if (n < 2) {
    return 1;
  } else {
    return n * fact(n - 1);
  }
}

function greet(name:string):void {
  log("Hello,");
  log(name);
}

function max(a:number, b:number):number {
  if (a > b) {
    return a;
  } else {
    return b;
  }
}

let x:number;
x = fact(5);
log(x);

greet("Ana");

let z:number;
z = max(3, 7);
log(z);

