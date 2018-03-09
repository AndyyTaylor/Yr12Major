# ML Major - Andy Taylor

## Standard-ish Algorithms
One issue I'm running into a bit is that most of these algorithms are standard, meaning my implementations are very similar to pre-existing implementations.
The first thing to note is I still have to make sure these all conform well enough to be 'plug and play' in the application


## Third Party Libraries
I was really hoping to write almost everything from scratch (using only numpy), but I'm going to have to make some exceptions.

1. I'll use pandas for loading datasets.
   This is a widely used tool, and being able to use it well will be invaluable for more complex ML work.
   Additionally, it allows me to spend time on more interesting analysis like feature engineering

2. I'll use scipy for complex mathematical formulas, so long as I properly understand them
   In addition to convenience, scipy is well optimized and writing this stuff in python would greatly slow down the application.

3. I'll have a Tensorflow or Theano implementation for complex deep learning algorithms.
   This is the same optimization problem as scipy * 1000
   As much as I can, I'll include my own implementation, but some of this stuff is a bit ridiculous
