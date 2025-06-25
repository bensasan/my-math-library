const math = require('./math')

const [, , op, aStr, bStr] = process.argv
const a = parseFloat(aStr)
const b = parseFloat(bStr)

if (isNaN(a) || isNaN(b)) {
  console.error('Please provide two numbers')
  process.exit(1)
}

let result
switch (op) {
  case 'add':
    result = math.add(a, b)
    break
  case 'subtract':
    result = math.subtract(a, b)
    break
  case 'multiply':
    result = math.multiply(a, b)
    break
  case 'divide':
    try {
      result = math.divide(a, b)
    } catch (err) {
      console.error(err.message)
      process.exit(1)
    }
    break
  default:
    console.error('Unknown operation')
    process.exit(1)
}

console.log(result)
