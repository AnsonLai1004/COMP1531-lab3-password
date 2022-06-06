# Lab03 - Password

[TOC]

## Due Date

Week 4 Monday 5:00 pm AEST

## Background

### Note

**The quality of your tests will be assessed in this lab and future labs from this point onwards**.

### Rationale

Users are not very clever. They tend to choose the ~~laziest~~ most convenient option available despite being fully aware of the drawbacks that it entails. 

Take passwords, for example - how often do people:

1. use a common phrase such as `password`,
1. re-use the same password across different accounts, or
1. use/combine simple words (e.g. `hearsay`) to make a weak password,

thus sacrificing security for the sake of not having to remember a strong yet difficult string of authentication. 

In this lab, your goal is to rate the strength of a password using a set of requirements and produce a test suite that can dynamically verify, to a satisfactory extent, that a particular solution will meet these requirements.

### Getting Started
- Copy the SSH clone link from Gitlab and clone this repository on either VLAB or your local machine. 
- In your terminal, change your directory (using the `cd` command) into the newly cloned lab. To check if you have done this correctly, type `ls` in this new directory to see if you can see the relevant files (including [password.js](password.js)).


### Jest Installation

*[Jest](https://jestjs.io/) is a delightful JavaScript Testing Framework with a focus on simplicity*. To get started,

1. Install Jest as a development dependency by specifying the option `--save-dev`. We do this because testing packages are unnecessary in production code.
    ```shell
    $ npm install --save-dev jest # shortcut: npm i -D jest
    ```

1. For compatibility with our new import/export syntax, we will also install [@babel/preset-env](https://www.npmjs.com/package/@babel/preset-env).
    ```shell
    $ npm install --save-dev @babel/preset-env # shortcut: npm i -D @babel/preset-env
    ```

1. Open [package.json](package.json) and confirm that jest and @babel/preset-env are shown in `"devDependencies"`, e.g
    ```json
    // Note: Your version number may differ
    "devDependencies": {
        "@babel/preset-env": "^7.17.10",
        "jest": "^28.1.0"
    }
    ```

1. Also, under `"scripts"`, you should see a section similar to:
    ```json
    "scripts": {
        "test": "echo \"Error: no test specified\" && exit 1"
    }
    ```
    Modify the value of the key `test` to `jest`:
    ```json
    "scripts": {
        "test": "jest"
    }
    ```

1. You can run your added scripts with the command `npm run [script]`. However, since `test` is a special keyword in `npm`, you can use any of the three commands below:
    ```shell
    $ npm run test
    $ npm test
    $ npm t
    ```

1. To check that you have completed the steps correctly, compare your [package.json](package.json) with our sample package.json in the [Additional Information](#additional-information) section.

1. Type `git status` in your terminal. You should see that [package.json](package.json) and [package-lock.json](package-lock.json) have been modified or is untracked. Use git to add, commit and push these changes.

### Interface: Functions

<table>
  <tr>
    <th>Name & Description</th>
    <th>Parameters</th>
    <th>Return Type</th>
    <th>Errors</th>
  </tr>
  <tr>
    <td>
        <code>checkPassword</code><br /><br />
        Checks the strength of the given password and returns a string
        to represent the result.
        <br/><br/>
        The returned string is based on the requirements below:
        <br/><br/>
        <ol>
            <li>
                Strong Password
                <ul>
                    <li>at least 12 characters</li>
                    <li>at least  1 number</li>
                    <li>at least  1 uppercase letter</li>
                    <li>at least  1 lowercase letter</li>
                </ul>
            </li>
            <li>
                Moderate Password
                <ul>
                    <li>at least  8 characters</li>
                    <li>at least  1 number</li>
                </ul>
            </li>
            <li>
                Horrible Password
                <ul>
                    <li>
                        passwords that are exactly any of the <a href="https://en.wikipedia.org/wiki/List_of_the_most_common_passwords" target="_blank"><b>top 5</b> (not 20) most common passwords</a> in the 2021 Nordpass Ranking.
                    </li>
                </ul>
            </li>
            <li>
                Poor Password
                <ul>
                    <li>
                        all remaining passwords that are not horrible, moderate or strong.
                    </li>
                <ul>
            </li>
        </ol>
    </td>
    <td>
        (password)
    </td>
    <td>
        <code>string</code>
    </td>
    <td>
        N/A
    </td>
  </tr>
</table>

### Interface: Data Types
| Variable Name | Type |
| --- | --- |
| `password` | `string` |


## Task

### Writing Tests

Before implementing `checkPassword`,

1. Open the file [password.test.js](password.test.js).
1. Write at least 10 tests for `checkPassword`.
    - you should avoid repeated/redundant tests.
    - ensure that each test targets exactly one specific case.
    - aim to cover as many different cases for the function as you can. **You will be assessed on this**.
    - try to follow the specification as closely as possible when designing your tests.
1. Run your tests with
    ```shell
    $ npm t
    ```
1. Ensure that there are unexpected errors. You should expect the current stub code in `checkPassword` to fail most tests.
1. Use git to add, commit and push [password.test.js](password.test.js).


#### Tips with Jest
- View the API and documentation at https://jestjs.io/docs/api
- You may want to explore `test.each` - this is a way to write multiple tests succinctly.

### Implementation

Once you have written your test suite,

1. Open [password.js](password.js) and implement `checkPassword` according to its documentation
1. Run your test
1. Fix any bug in your implementation
1. Git add, commit and push your code


### Share your experience!

Share your thoughts [HERE](https://cgi.cse.unsw.edu.au/~cs1531/redirect_activity/?activity=lab03_password) on any of the following:
1. How did you find this activity? What were the challenges?
1. What is something you learned from this activity?
1. What are a few of your favourite passwords? (just kidding, please don't answer this honestly)
1. What are some other ways we can make passwords stronger?

## Submission

- Use `git` to `add`, `commit`, and `push` your changes on your master branch.
- Check that your code has been uploaded to your Gitlab repository on this website (you may need to refresh the page).

**If you have pushed your latest changes to master on Gitlab no further action is required! At the due date and time, we automatically collect your work from what's on your master branch on Gitlab.**

## Notes
- You should only test the requirements specified in the [Interface: Functions](interface-functions).
- You should **not** be testing any undefined behaviour (e.g do not pass in a `number` instead of a `string` for a password).
- You are not allowed to use any other external libraries/modules in this exercise.

## Additional Information

### Sample package.json

<details>

<summary>Click to view our sample package.json</summary><br/>

**Note**: 
1. The main keys to pay attention to are `"scripts"`, `"dependencies"` and `"devDependencies"`.
1. It is fine if the versions of your packages are newer.

```json
{
  "name": "lab03_password",
  "version": "1.0.0",
  "description": "[TOC]",
  "type": "module",
  "main": "password.js",
  "scripts": {
    "test": "jest"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "@babel/preset-env": "^7.17.10",
    "jest": "^28.1.0"
  }
}
```

</details>

### Miscellaneous

<details>

<summary>Other information that is not core to the course</summary><br/>

- For starting new projects, 
    - a [package.json](package.json) file can be generated with `npm init`, where you will be prompted with a series of questions.
    - Alternatively, `npm init --yes` (shortcut `npm init -y`) will immediately generate a [package.json](package.json) with default options.
    - However, we will always provide you with a stub [package.json](package.json) in the labs, so you won't ever need to do this.
- [@babel/preset-env](https://www.npmjs.com/package/@babel/preset-env) will only be needed in lab03 
    - this is for using javascript Jest with ES Modules (notice the key `"type"` in [package.json](package.json) has the value `"module"`).
    - this package is utilised in the file [.babelrc](.babelrc).
    - labs in future weeks will not require this dependency.

</details>
