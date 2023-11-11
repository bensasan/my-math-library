function sum(a, b) {
  if (Array.isArray(a)) {
    return a.reduce((acc, n) => acc + n, 0)
  } else if (typeof a === 'number' && typeof b === 'number') {
    return a + b
  }
}


module.exports={sum};