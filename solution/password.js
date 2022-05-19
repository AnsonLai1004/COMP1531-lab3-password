/**
 * The solution below makes heavy use of
 * regular expression.
 *
 * /\d/ for containing a digit
 * /[A-Z]/ for containing an upper case
 * /[a-z]/ for containing a lower case
 */
export function checkPassword(password) {
  if (['123456', '123456789', '12345', 'qwerty', 'password'].includes(password)) {
    return 'Horrible Password';
  }
  if (password.length >= 8 && /\d/.test(password)) {
    if (password.length >= 12 && /[A-Z]/.test(password) && /[a-z]/.test(password)) {
      return 'Strong Password';
    }
    return 'Moderate Password';
  }
  return 'Poor Password';
}
