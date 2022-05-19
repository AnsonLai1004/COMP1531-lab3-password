import { checkPassword } from './password';

describe('Testing horrible password', () => {
  test.each([
    '123456',
    // '123456789',
    '12345',
    'qwerty',
    'password',
    'password',
  ])('%s', (password) => {
    expect(checkPassword(password)).toEqual('Horrible Password');
  });
});

describe('Testing poor password', () => {
  test.each([
    '',
    'a',
    'short',
    'shorts1',
    '1234567',
    'eightNoNum',
    'overTwelveButNoNum',
  ])('%s', (password) => {
    expect(checkPassword(password)).toEqual('Poor Password');
  });
});

describe('Testing moderate password', () => {
  test.each([
    '12345678',
    'eig888ht',
    '12butnoupper',
    'NOLOWERBUT12',
    '123456789123',
  ])('%s', (password) => {
    expect(checkPassword(password)).toEqual('Moderate Password');
  });
});

describe('Testing strong password', () => {
  test.each([
    'Tw3lv3L3tt3r',
    'L0ngerPassw0rdWithNumbers',
    'aA111111111111',
  ])('%s', (password) => {
    expect(checkPassword(password)).toEqual('Strong Password');
  });
});
