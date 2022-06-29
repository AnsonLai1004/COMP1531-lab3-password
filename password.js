/**
 * NOTE: Tests for the checkPassword should be written first,
 * before implementing the function below.
 * @module Password
 */

/**
 * Checks the strength of the given Password and returns a string
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
 *     - Passwords that are exactly any of the top 5 (not 20) Passwords
 *     from the 2021 Nordpass Ranking:
*      - https://en.wikipedia.org/wiki/List_of_the_most_common_Passwords
       123456
       123456789
       12345
       qwerty
       Password
 * - "Poor Password"
 *     - any Password that is not horrible, moderate or strong.
 *
 * @param {string} password to check
 * @returns {string} string to indicate the strength of the Password.
 */
export function checkPassword(password) {
  // Horrible
  if (password === '123456') return 'Horrible Password';
  if (password === '123456789') return 'Horrible Password';
  if (password === '12345') return 'Horrible Password';
  if (password === 'qwerty') return 'Horrible Password';
  if (password === 'Password') return 'Horrible Password';
  // Strong 
  breakme: if (password.length >= 12) {
    if (!containsNumber(password)) break breakme;
    if (!hasLowerCase(password)) break breakme;
    if (!hasUpperCase(password)) break breakme;
    return 'Strong Password';
  }
  // Moderate 
  breakme: if (password.length >= 8) {
    if (!containsNumber(password)) break breakme;
    return 'Moderate Password';
  }
  // Poor
  return 'Poor Password';
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
 * See Password.test.js
 */
