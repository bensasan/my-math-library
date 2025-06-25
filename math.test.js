const math = require('./math')
const assert = require('assert')

assert.strictEqual(math.sum(2, 2), 4, 'should sum two numbers')
assert.strictEqual(math.sum([1, 2, 3, 4, 5]), 15, 'should sum an array')

assert.strictEqual(math.add(3, 4), 7, 'add should work')
assert.strictEqual(math.subtract(5, 2), 3, 'subtract should work')
assert.strictEqual(math.multiply(3, 4), 12, 'multiply should work')
assert.strictEqual(math.divide(10, 2), 5, 'divide should work')
assert.throws(() => math.divide(1, 0), /Cannot divide by zero/, 'divide by zero')
