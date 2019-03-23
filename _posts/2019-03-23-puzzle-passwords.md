---
layout: post
title: "Puzzle for developers on password protection"
date:   2019-03-23 20:00:00 +0500
description: Password protection always seems like an easy thing to do; but lets take a test driven approach to see how you do. # Add post description (optional)
img: hdd-concrete-2.jpg # Add image post (optional)
fig-caption: # Add figcaption (optional)
tags: [Puzzles]
author: Trent Speckhart
---

Password protection always seems like an easy thing to do; but lets take a test driven approach to see how you do.

## Password Protection

We see all over the news about passwords being leaked in the clear or leveraging only encoding or even weak hashing algorithms.  Let's take a simplified approach at looking at the logic associated with password storage and protections.   I recently read a discussion() which challenged the "storage" of historical passwords.   This foundation allows you to test and play with ideas to protect even these historical passwords while meeting the need to protect from re-used and drive regular rotation and changes. 

### Setup

1. Clone https://github.com/cmeinco/appsecwtf-puzzles
1. `cd appsecwtf-puzzles/passwords-01`
1. Install requirements

### The Challenges

We start with a "working" version of the password management component.  Review the code and feel free to adjust to your style, leverage the test cases to validate the functionality against positive and negative scenarios.

1. Install and confirm 2 passed, 1 skipped, 3 xfailed.
1. Protect the password while stored in the database. (Enable the skipped test case)
1. Add a check for password complexity. 
1. Protect the logs, cleanup the logging messages to not output passwords in plain text.
1. Dont let the password be changed immediately, add a timer which can be changed for different environments.  Allowing a user to change their password immediately allows them to easily and quickly bypass the historical password requirement.  Many environments enforce a 1 day wait time between password changes.

Feel free to push a PR with new ideas or test cases to help others!  

### More Thought Provoking Articles

Never stop learning.

1. https://softwareengineering.stackexchange.com/questions/177342/how-to-implement-a-safe-password-history?utm_source=twitterfeed&utm_medium=twitter
2. https://www.troyhunt.com/should-websites-be-required-to-publicly/
3. https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Password_Storage_Cheat_Sheet.md
4. https://nakedsecurity.sophos.com/2013/11/20/serious-security-how-to-store-your-users-passwords-safely/


