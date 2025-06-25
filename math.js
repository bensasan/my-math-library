function sum(a, b) {
  if (Array.isArray(a)) {
    return a.reduce((acc, n) => acc + n, 0)
  } else if (typeof a === 'number' && typeof b === 'number') {
    return a + b
  }
}

function add(a, b) {
  return a + b
}

function subtract(a, b) {
  return a - b
}

function multiply(a, b) {
  return a * b
}

function divide(a, b) {
  if (b === 0) {
    throw new Error('Cannot divide by zero')
  }
  return a / b
}

module.exports = { sum, add, subtract, multiply, divide }
