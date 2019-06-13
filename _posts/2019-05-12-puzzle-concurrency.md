---
layout: post
title: "Concurrency Problems"
date:   2019-05-12 20:00:00 +0500
description: Playing and testing with concurrency problems. # Add post description (optional)
img: fries.jpg # Add image post (optional)
fig-caption: # Add figcaption (optional)
tags: [Puzzles]
author: Trent Speckhart
---

Playing and testing concurrency problems.   

## Concurrency

This is a fun problem when working with distributed systems. Thinking about how the processing needs to flow through the system and other variables that can continue to break down the checks you put in place to protect the resource.

This example looks at a made up situation where we want to limit the number of potates which can be added to a file.   Simply thinking about testing, we can script the sequential adding, but we do not test when multiple requests hit the resource at a single time.  

## The meat

Our resource is going to be a file that contains the list of potatoes.  We need to read the file and check how many potatoes exist in the file to then decide if we can add more.
```
with open("testfile.dat", "r") as infile:
    lines=infile.readlines()
infile.close()
```

to help test this problem, we're going to make this request super slow.  This makes it easier to queue up a few requests to easily overcome and limits.
```
time.sleep(10)
```

We're going to do a super late read to let lots of things get into this pipeline.
```
totalpotatoes=len(lines)
retVal=""
```

Now we check if the total number of potatoes is greater than the limit (5) and if not we go ahead and write to append a new potato to the file.
```
if totalpotatoes > 5:
    retVal+="Exceed the Potato Limit, currently {}.".format(totalpotatoes)
else:
    retVal+="Read in {} Potatos.".format(totalpotatoes)
    with open("testfile.dat","a") as outfile:
        outfile.write("a potato\n")
    outfile.close()
```

Walking through this simple code, you can easily see how easy it would be for multiple requests coming in to all read 0 potatoes and every thread thinking it can write/append to the file.


## The Test

Cleanup from the previous test
```
rm testfile.dat
touch testfile.dat 
rm testfilefixed.dat 
touch testfilefixed.dat 

set -x
```

Lets run the failure test first; the last 2 serialized requests lets us see the problem. 
```
testcase="concurrenttest"

curl --url "http://localhost:5000/${testcase}" & 
curl --url "http://localhost:5000/${testcase}" & 
curl --url "http://localhost:5000/${testcase}" & 
curl --url "http://localhost:5000/${testcase}" & 
curl --url "http://localhost:5000/${testcase}" & 
curl --url "http://localhost:5000/${testcase}" & 
curl --url "http://localhost:5000/${testcase}" & 
curl --url "http://localhost:5000/${testcase}" & 
curl --url "http://localhost:5000/${testcase}" & 
curl --url "http://localhost:5000/${testcase}" 

sleep 10

curl --url "http://localhost:5000/${testcase}" 
```
testoutput: (cleaned for easy reading)
```
++ testcase=concurrenttest
Read in 0 Potatos.
Read in 0 Potatos.
Read in 0 Potatos.
Read in 0 Potatos.
Read in 0 Potatos.
Read in 0 Potatos.
Read in 0 Potatos.
Read in 0 Potatos.
Read in 0 Potatos.
Read in 0 Potatos.
++ sleep 10
Exceed the Potato Limit, currently 10.
```

Now let's run the tests against the fixed code.
```
testcase="concurrenttestfixed"

curl --url "http://localhost:5000/${testcase}" & 
curl --url "http://localhost:5000/${testcase}" & 
curl --url "http://localhost:5000/${testcase}" & 
curl --url "http://localhost:5000/${testcase}" & 
curl --url "http://localhost:5000/${testcase}" & 
curl --url "http://localhost:5000/${testcase}" & 
curl --url "http://localhost:5000/${testcase}" & 
curl --url "http://localhost:5000/${testcase}" & 
curl --url "http://localhost:5000/${testcase}" & 
curl --url "http://localhost:5000/${testcase}" 

sleep 10

curl --url "http://localhost:5000/${testcase}" 
```
SUCCESS! 
output: (cleaned up for ease of reading)
```
++ testcase=concurrenttestfixed
Read in 0 Potatos.
Read in 1 Potatos.
Read in 2 Potatos.
Read in 3 Potatos.
Read in 4 Potatos.
Read in 5 Potatos.
++ sleep 10
Exceed the Potato Limit, currently 6.
Exceed the Potato Limit, currently 6.
Exceed the Potato Limit, currently 6.
Exceed the Potato Limit, currently 6.
Exceed the Potato Limit, currently 6.
```

## Expansion Ideas

1. Create a user element and limit the potatoes to 5 per user.
2. Run multiple instances of the application (on the same host) and solve the problem.
3. Run the app on different hosts and solve the problem.

## The Code

Clone the code here, send in some PRs, have some fun.

[https://github.com/cmeinco/appsecwtf-puzzles/tree/master/concurrency-01](https://github.com/cmeinco/appsecwtf-puzzles/tree/master/concurrency-01)


## References

* [Let’s Synchronize Threads in Python](https://medium.com/@arichduvet/synchronization-primitives-in-python-564f89fee732)
* [Working with a global singleton in Flask (WSGI), do I have to worry about race conditions?](https://stackoverflow.com/questions/10181706/working-with-a-global-singleton-in-flask-wsgi-do-i-have-to-worry-about-race-c)
* [Java Thread – Mutex and Semaphore example](https://www.mkyong.com/java/java-thread-mutex-and-semaphore-example/)


