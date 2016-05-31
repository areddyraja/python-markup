title: Reduce
date: 2016-05-02
description: A tutorial on Apache Spark
tags: spark, programming, hadoop, bigdata, yarn

###Reduce
Reduces the given input. 

	:::scala
	def reduce(f: (T, T) => T): T

####Reduce numbers 1 to 100 by adding them up

	:::scala
	val x = sc.parallelize(1 to 100, 3)
	val y = x.reduce((accum,n) => (accum + n)) 
	y: Int = 55

Accum: is the accumulated value passed every time to the reduce function.
Accum is the previous value, and n is the current value. accum+n is the cumulative sum of the numbers. The reduce takes a function, which shoud be commutative *(a+b=b+a)* other wise, reduce will give different results every time reduce is run on the same data

Short Syntax

	:::scala
	val numbers = sc.parallelize(1 to 100, 3)
	numbers.reduce( _ + _ )
	res0: Int = 5050

Same thing for multiplication

	:::scala
	val y = x.reduce(_ * _) 
        y: Int = 3628800

