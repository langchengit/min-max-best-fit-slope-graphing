# linear graph

draws error boxes, min, max and best-fit line

# how to use

input data and error range, create utility functions for yourself if you need

(eg. you can do inverse relationship like this: 

provide x and y values normally, create a function reciprocal(x) and call `reciprocal(x) for x in x` on line 13

when drawing error box, do 
``
left = reciprocal (x + error_x)
right = reciprocal (x - error_x)

``
)
