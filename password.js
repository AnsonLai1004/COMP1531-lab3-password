/**
 * NOTE: Tests for the checkPassword should be written first,
 * before implementing the function below.
 * @module password
 */

/**
 * Checks the strength of the given password and returns a string
 * to represent the result.
 *
 * The returned string is based on the requirements below:
 * - "Strong Password"
 *     - at least 12 characters
 *     - at least  1 number
 *     - at least  1 uppercase letter
 *     - at least  1 lowercase letter
 * - "Moderate Password"
 *     - at least  8 characters
 *     - at least  1 number
 * - "Horrible Password"
 *     - passwords that are exactly any of the top 5 (not 20) passwords
 *     from the 2021 Nordpass Ranking:
*      - https://en.wikipedia.org/wiki/List_of_the_most_common_passwords
       123456
       123456789
       12345
       qwerty
       password
 * - "Poor Password"
 *     - any password that is not horrible, moderate or strong.
 *
 * @param {string} password to check
 * @returns {string} string to indicate the strength of the password.
 */
export function checkPassword(password) {
  // Horrible
  if (password === '123456') return 'Horrible password';
  if (password === '123456789') return 'Horrible password';
  if (password === '12345') return 'Horrible password';
  if (password === 'qwerty') return 'Horrible password';
  if (password === 'password') return 'Horrible password';
  // Strong 
  breakme: if (password.length >= 12) {
    if (!containsNumber(password)) break breakme;
    if (!hasLowerCase(password)) break breakme;
    if (!hasUpperCase(password)) break breakme;
    return 'Strong password';
  }
  // Moderate 
  breakme: if (password.length >= 8) {
    if (!containsNumber(password)) break breakme;
    return 'Moderate password';
  }
  // Poor
  return 'Poor password';
}

function containsNumber(str) {
  return /\d/.test(str);
}
function hasLowerCase(str) {
  return (/[a-z]/.test(str));
}
function hasUpperCase(str) {
  return (/[A-Z]/.test(str));
}
/**
 * Testing will no longer be done in here.
 * See password.test.js
 */
