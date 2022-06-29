/**
 * @see password
 * @module password.test
 */

import { checkPassword } from './password.js';

describe('Horrible Password', () => {
  test.each`
    input     | expectedResult
    ${'123456'}  | ${'Horrible Password'}
    ${'123456789'}   | ${'Horrible Password'}
    ${'12345'}  | ${'Horrible Password'}
    ${'qwerty'}   | ${'Horrible Password'}
    ${'password'} | ${'Horrible Password'}
    // add new test cases here
  `('Password $input is $expectedResult', ({ input, expectedResult }) => {
    expect(checkPassword(input)).toBe(expectedResult)
  })
})

describe('Length', () => {
  test.each`
    input     | expectedResult
    ${'Comp1531AAAA'}  | ${'Strong Password'}
    ${'Comp1531'}   | ${'Moderate Password'}
    ${'Comp'}  | ${'Poor Password'}
    // add new test cases here
  `('Password $input is $expectedResult', ({ input, expectedResult }) => {
    expect(checkPassword(input)).toBe(expectedResult)
  })
})
describe('has number', () => {
  test.each`
    input     | expectedResult
    ${'CompOneFiveThreeOne'}   | ${'Poor Password'}
    ${'CompOneFive31'} | ${'Strong Password'}
    ${'CompOneF3'} | ${'Moderate Password'}
    // add new test cases here
  `('Password $input is $expectedResult', ({ input, expectedResult }) => {
    expect(checkPassword(input)).toBe(expectedResult)
  })
})
describe('Uppercase and lowercase', () => {
  test.each`
    input     | expectedResult
    ${'CompOneFIve3111'}   | ${'Strong Password'}
    ${'componefive3111'} | ${'Moderate Password'}
    ${'COMPFIVE3111'} | ${'Moderate Password'}
    // add new test cases here
  `('Password $input is $expectedResult', ({ input, expectedResult }) => {
    expect(checkPassword(input)).toBe(expectedResult)
  })
})

/*

// You can remove or replace this with your own tests.
// TIP: you may want to explore "test.each"
describe('Example block of tests', () => {
  test('Example test 1', () => {
    expect(checkPassword('something')).toEqual('Poor Password');
  });

  test('Example test 2', () => {
    expect(checkPassword('not a good test')).toEqual('Poor Password');
  });
});

*/
