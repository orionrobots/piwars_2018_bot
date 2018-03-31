Today I got the kids involved making - and we had some fun getting the motor cables the right way.
However, the stall outs, or lock ups troubled me. 
The piconzero on this (and tankbot) kept stopping - and it could even stop with the motors running.
This was disturbing.

[youtube driving before]

I was researching stuff on motor stall currents, and brushing up my physics - what had I missed? The robot could fail only seonds in, or a while in.

After checking on twitter, and then reading the piconzero docs - it turns out that older pi raspbian images had i2c stability issues.
So I started a dist-upgrade on it. This seemed like a great plan.

Bad news  then - I knocked out the power cable (external wall power) while doing the update!
The image I had was not going to work again. I'd luckily backed up my own code before doing so - so nothing lost but time.
And the @approx_eng came to the rescue with an image he had with BlueZ and sixaxis control on board, along with openCV. Which will save my compiling again.
My old image had python3 - so after using his image, there was some adapting to do.
First - smbus needed to be smbus2 - but this was because I had overlooked I was in a virtual env - once I'd adapted that, the motor test worked.
@biglesp had python3 adaptations of the piconzero code to use now.

I got it to drive again! It was no longer hanging, but I was getting squealing motor stalls.

My next thought was to try taming it from full spin to just braking a tread at a time.
So I make a "tankTest.py" module adapted from "motorTest.py" - using the numeric keypad like tank drive controls:

| Motor   | Left | Right |
| ------- | ---- | ----- |
| Forward |   7  |   9   |
| Stop    |   4  |   6   |
| Reverse |   1  |   3   |

This was then driving brilliantly - few stalls, no piconzero cutouts. Stability seems good.

[youtube driving now]


Next stages:
* Fitting camera
* Fitting distance sensors
* Getting my skittlebot code adapted for both the driving style and new opencv.
* Making the distance sensor code.
* Tidying up - cables a mess - my plan is to use PC drive power adaptors.
* Making a cover - not sure how much time, but this is Helena's most wanted task.
   
