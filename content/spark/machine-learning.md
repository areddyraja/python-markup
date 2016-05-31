title: Machine Learning Apache Spark
date: 2016-05-02
description: A tutorial on Apache Spark
tags: spark, programming, hadoop, bigdata, yarn

###Scala: Machine Learning

MLlib is Spark’s library of machine learning functions. Designed to run in parallel on clusters, MLlib contains a variety of learning algorithms and is accessible from all of Spark’s programming languages.

MLlib’s design and philosophy are simple: it lets you invoke various algorithms on distributed datasets, representing all data as RDDs. MLlib introduces a few data types (e.g., labeled points and vectors), but at the end of the day, it is simply a set of functions to call on RDDs.

####Logistical Regression with SGD

This program uses two MLlib algorithms: HashingTF, which builds term frequency feature vectors from text data, and Logistic RegressionWithSGD, which implements the logistic regression procedure using stochastic gradient descent (SGD)

	:::java
	import org.apache.spark.SparkContext
	import org.apache.spark.SparkContext._
	import org.apache.spark.SparkConf
	import org.apache.spark.mllib.regression.LabeledPoint
	import org.apache.spark.mllib.feature.HashingTF
	import org.apache.spark.mllib.classification.LogisticRegressionWithSGD

	object SpamFilter {
		def main(args: Array[String]) {
		val conf = new SparkConf().setAppName("SpamFilter")
		val sc = new SparkContext(conf)
		val home = "/home/ubuntu/work/spark/spark-samples/"
		val spam = sc.textFile(home + "ml-samples/data/spam_v1_text.txt")
		val normal = sc.textFile(home + "ml-samples/data/non-spam_v1_text.txt")

		// Create a HashingTF instance to map email text to
		// vectors of 10,000 features.
		val tf = new HashingTF(numFeatures = 10000)
		// Each email is split into words,
		//and each word is mapped to one feature.
		val spamFeatures = spam.map(email => tf.transform(email.split(" ")))
		val normalFeatures = normal.map(email => tf.transform(email.split(" ")))

		// Create LabeledPoint datasets for positive (spam)
		// and negative (normal) examples.
		val positiveExamples = spamFeatures.map(
	    features => LabeledPoint(1, features))
		val negativeExamples = normalFeatures.map(
	    features => LabeledPoint(0, features))
		val trainingData = positiveExamples.union(negativeExamples)
		// Cache since Logistic Regression is an iterative algorithm.
		trainingData.cache()

		// Run Logistic Regression using the SGD algorithm.
		val model = new LogisticRegressionWithSGD().run(trainingData)

		// Test on a positive example (spam) and a negative one (normal).
		val sOne = "iPhone Leather Sleeve CASSIOPEIA http://t.co/EMtxZNU2ro | " +
				"#iphone #iphone5 #iPhone5Sleeve #iPhoneSleeve " +
				"#iPhone5sSleeve #iPhone5s #Swarovski"
		val sTwo = "this is non spam text "
        val sThree = "@airtelghana  thank you soo much #iphone5s​"
        val posTest = tf.transform(sOne.split(" "))
        val negTest = tf.transform(sTwo.split(" "))
        val thirdTest = tf.transform(sThree.split(" "))
        println("Prediction for Spam '" + sOne  + "' : "+ model.predict(posTest))
        println("Prediction for spam '" + sTwo + "' : " + model.predict(negTest))
        println("Prediction for spam '" + sThree + "' :  " + model.predict(thirdTest))
	  }
	}
Execute the Code

	:::shell
	~/work/spark/spark-1.3.0-bin-hadoop2.4/bin/spark-submit --class \
		  "ml.SpamFilter" --master local[4] target/scala-2.10/ml-project_2.10-1.0.jar

####TF-IDF Sample
	:::java
	object TfIdfSample{
	  def main(args: Array[String]) {
		val file = "/home/ubuntu/work/spark/spark-samples/ml-samples/data/README.md"
		val conf = new SparkConf().setAppName("TfIdfSample")
		val sc = new SparkContext(conf)
		val documents: RDD[Seq[String]] = sc.textFile(file).map(_.split(" ").toSeq)
		print("Documents Size:" + documents.count)
		val hashingTF = new HashingTF()
		val tf = hashingTF.transform(documents)
		for(tf_ <- tf) {
		  println(s"$tf_")
		}
		tf.cache()
		val idf = new IDF().fit(tf)
		val tfidf = idf.transform(tf)
		println("tfidf size : " + tfidf.count)
		for(tfidf_ <- tfidf) {
		  println(s"$tfidf_")
		}
	  }
	}

Execute the Code

	:::shell
	~/work/spark/spark-1.3.0-bin-hadoop2.4/bin/spark-submit --class \
		  "ml.TfIdfSample" --master local[4] target/scala-2.10/ml-project_2.10-1.0.jar

####Word2Vector Sample

Word2Vec computes distributed vector representation of words. The main advantage of the distributed representations is that similar words are close in the vector space, which makes generalization to novel patterns easier and model estimation more robust.

	:::scala
	object Word2Vector{
	  def main(args: Array[String]) {
		val file = "/home/ubuntu/work/spark/spark-samples/ml-samples/data/text8_10000"
		val conf = new SparkConf().setAppName("Word2Vector")
		val sc = new SparkContext(conf)
		val input = sc.textFile(file).map(line => line.split(" ").toSeq)
		val word2vec = new Word2Vec()
		val model = word2vec.fit(input)
		val synonyms = model.findSynonyms("anarchist", 40)
		for((synonym, cosineSimilarity) <- synonyms) {
		  println(s"$synonym $cosineSimilarity")
		}
	  }
	}

####Hashing TF Sample

	:::scala
	object HashingTFSample{
	  def main(args: Array[String]) {
		val conf = new SparkConf().setAppName("SpamFilter")
		val sc = new SparkContext(conf)
		val sentence = "This is a simple text"
		val words = sentence.split(" ")
		val tf = new HashingTF(numFeatures = 10000)
		val sparseVector = words.map(w => tf.transform(w))
		for(sv <- sparseVector) {
		  println(s"$sv")
		}
	  }
	}

####Consine Similarity

Input Data

	:::text
	0 2.857738033247042 0 2.061393766919624 2.619965104088255 4.745052855503306 2.004684436494304 0 2.122974378789621 2.228387042742021 2.228387042742023 0 0 0 0 0 0
	0 2.857738033247042 0 0 0 0 2.004684436494304 2.000347299268466 0 2.228387042742021 2.228387042742023 0 2.055002875864414 0 0 0 0
	1 0 2.52078447201548 2.061393766919624 0 0 2.004684436494304 2.000347299268466 0 0 0 0 2.055002875864414 0 0 0 0
	0 2.857738033247042 0 2.061393766919624 0 0 0 0 2.122974378789621 2.228387042742021 2.228387042742023 0 2.055002875864414 0 0 0 0
	0 2.857738033247042 0 0 2.619965104088255 0 2.004684436494304 2.000347299268466 0 2.228387042742021 2.228387042742023 0 0 0 0 0 0
	1 0 0 0 2.619965104088255 0 2.004684436494304 2.000347299268466 0 2.228387042742021 2.228387042742023 0 0 0 0 0 0
	1 2.857738033247042 2.52078447201548 2.061393766919624 2.619965104088255 0 2.004684436494304 0 0 2.228387042742021 2.228387042742023 0 0 0 0 0 0
	1 2.857738033247042 2.52078447201548 2.061393766919624 2.619965104088255 0 2.004684436494304 2.000347299268466 0 0 0 0 0 0 0 0 0
	1 2.857738033247042 0 2.061393766919624 2.619965104088255 0 0 2.000347299268466 0 0 0 0 2.055002875864414 0 0 0 0
	...

The program listing to find the cosine similarity is shown below:

	:::scala
	object CosineSimilarity{
	  def main(args: Array[String]) {
	val file = "/home/ubuntu/work/spark/spark-samples/ml-samples/data/sample_svm_data.txt"
	val conf = new SparkConf().setAppName("CosineSimilarity")
	val threshold = 0.1
	val sc = new SparkContext(conf)

	// Load and parse the data file.
	val rows = sc.textFile(file).map { line =>
	  val values = line.split(' ').map(_.toDouble)
	  Vectors.dense(values)
	}.cache()
	val mat = new RowMatrix(rows)

	// Compute similar columns perfectly, with brute force.
	val exact = mat.columnSimilarities()

	// Compute similar columns with estimation using DIMSUM
	val approx = mat.columnSimilarities(threshold)

	val exactEntries = exact.entries.map { case MatrixEntry(i, j, u) => ((i, j), u) }
	val approxEntries = approx.entries.map { case MatrixEntry(i, j, v) => ((i, j), v) }
	val MAE = exactEntries.leftOuterJoin(approxEntries).values.map {
	  case (u, Some(v)) =>
	    math.abs(u - v)
	  case (u, None) =>
	    math.abs(u)
	}.mean()

	println(s"Average absolute error in estimate is: $MAE")

	sc.stop()
	  }
	}

####Convert Word to Vectors

	:::scala
	object ConvertWordsToVectors{
	  def main(args: Array[String]) {
		val file = "/home/ubuntu/work/spark/spark-samples/ml-samples/data/text8_10000"
		val conf = new SparkConf().setAppName("Word2Vector")
		val sc = new SparkContext(conf)
		val input = sc.textFile(file).map(line => line.split(" ").toSeq)
		val word2vec = new Word2Vec()
		val model = word2vec.fit(input)
		val vectors = model.getVectors
		vectors foreach ( (t2) => println (t2._1 + "-->" + t2._2.mkString(" ")))
	  }
	}


