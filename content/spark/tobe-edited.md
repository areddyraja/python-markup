Apache Spark usage 


Scala Iterators
    val it = Iterator("a", "number", "of", "words")
    while(it.hasNext) println(it.next)
    
    
    or 
    
     val it = Iterator("a", "number", "of", "words")
     for(elem <- it ) println(elem)
     
     //For instance, iterators provide a map method, which returns a new iterator:
     val it2 = it.map(_.length)
     it2 foreach println
     
     it2.next gives you exception becasue the it2 went to the end of the list.
     
     //There is only one standard operation which allows to re-use the same iterator: The call


     val (it1, it2) = it.duplicate
     
    
foreachPartition

	Executes an parameterless function for each partition. 
	Access to the data items contained in the partition is provided via the iterator argument.
	
	def foreachPartition(f: Iterator[T] => Unit)

    Gives the scala iterator for traversing the partition
    
    val b = sc.parallelize(List(1, 2, 3, 4, 5, 6, 7, 8, 9), 3)
    
    //you can always use for loop instead 
    b.foreachPartition(x => for (eleme <- x) println(eleme))
    //you can also use the while loop for iterating over the scala iterator
    b.foreachPartition(x => while(x.hasNext) println(x.next()))
    //you can also use the foreach and println
    b.foreachPartition(x => x foreach println)
	b.foreachPartition(x => println(x.reduce(_ + _)))
	

	
	
	

a = sc.parallelize(List("dog", "salmon", "salmon", "rat", "elephant "), 3)
b = a.keyBy(_.length)


val a = sc.parallelize(1 to 9, 3)

def myfunc[T](iter: Iterator[T]) : Iterator[(T,T)] = {  
	var res = List[(T,T)]()   
	var pre = iter.next
	while(iter.hasNext)  
	{  
	   val cur = iter.next  
	   res .:: (pre, cur)  
	   pre = cur 
	}   
	res.iterator  
}


