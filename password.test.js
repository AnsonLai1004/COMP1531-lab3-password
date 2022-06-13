/**
 * @see password
 * @module password.test
 */

import { checkPassword } from './password';

describe('Horrible password', () => {
  test.each`
    input     | expectedResult
    ${'123456'}  | ${'Horrible password'}
    ${'123456789'}   | ${'Horrible password'}
    ${'12345'}  | ${'Horrible password'}
    ${'qwerty'}   | ${'Horrible password'}
    ${'password'} | ${'Horrible password'}
    // add new test cases here
  `('password $input is $expectedResult', ({ input, expectedResult }) => {
    expect(checkPassword(input)).toBe(expectedResult)
  })
})

describe('Length', () => {
  test.each`
    input     | expectedResult
    ${'Comp1531AAAA'}  | ${'Strong password'}
    ${'Comp1531'}   | ${'Moderate password'}
    ${'Comp'}  | ${'Poor password'}
    // add new test cases here
  `('password $input is $expectedResult', ({ input, expectedResult }) => {
    expect(checkPassword(input)).toBe(expectedResult)
  })
})
describe('has number', () => {
  test.each`
    input     | expectedResul
    ${'CompOneFiveThreeOne'}   | ${'Poor password'}
    ${'CompOneFive31'} | ${'Strong password'}
    ${'CompOneF3'} | ${'Moderate password'}
    // add new test cases here
  `('password $input is $expectedResult', ({ input, expectedResult }) => {
    expect(checkPassword(input)).toBe(expectedResult)
  })
})
describe('Uppercase and lowercase', () => {
  test.each`
    input     | expectedResul
    ${'CompOneFIve3111'}   | ${'Strong password'}
    ${'componefive3111'} | ${'Moderate password'}
    ${'COMPFIVE3111'} | ${'Moderate password'}
    // add new test cases here
  `('password $input is $expectedResult', ({ input, expectedResult }) => {
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
