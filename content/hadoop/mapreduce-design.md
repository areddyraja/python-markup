title: Big Data with Hadoop
date: 2016-05-02
description: MapReduce design patterns explained.
tags: mpareduce, hive, haddop, design patterns, boomfilter, programming, hadoop, bigdata, yarn


#Summarization - Average

In this lab you will use the StackOverflow User Comments to find the following

No of comments for each hour of the day
Average Lenght of each comment
Input Data

Downloaded from `https://archive.org/download/stackexchange/datascience.stackexchange.com.7z`_. We will use the user comments file Comments.xml Sample of the file is listed below.

<?xml version="1.0" encoding="utf-8"?>
<comments>
        <row Id="5" PostId="5" Score="9"
                Text="this is a super theoretical AI question. An interesting discussion! but out of place..."
                CreationDate="2014-05-14T00:23:15.437" UserId="34" />
        <row Id="6" PostId="7" Score="4" Text="List questions are usually not suited for Stack Exchange
                websites since there isn't an &quot;objective&quot; answer or a way to measure the usefulness
        of an answer. Having said that, one of my recommendations would be MacKay's &quot;Information
        Theory, Inference, and Learning Algorithms.&quot;"
        CreationDate="2014-05-14T00:38:19.510" UserId="51" />
</comments>
Mapper Code

Mapper tales in Input Comment line which is an Xml element and returns the outHour and outTuple. This is a custom type created and contains the following elements

  public class CountAverageTuple implements Writable {
    private int count;
    private float average;
...
  }
It extends the Generic Mapper : Output is written to the context object.

context.write(outHour, outTuple);
public static class AverageMapper extends
        Mapper<Object, Text, IntWritable, CountAverageTuple> {

        private IntWritable outHour = new IntWritable();
        private CountAverageTuple outTuple = new CountAverageTuple();

        @SuppressWarnings("deprecation")

        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {
          Map<String,String> parsed = transformXmlToMap(value.toString());

          String strDate = parsed.get("CreationDate");
          String text = parsed.get("Text");

          if (isNullOrEmpty(strDate) || isNullOrEmpty(text)) {
            return;
          }

          Date creationDate;

          try {
            creationDate = DATE_FORMAT.parse(strDate);
          } catch (ParseException e) {
            e.printStackTrace();
            return;
          }

          outHour.set(creationDate.getHours());

          outTuple.set(1, text.length());

          context.write(outHour, outTuple);
        }
}
Reducer Code

In the reducer code we iterate over Iterable<CountAverageTuple> values to calculate the count and average for each hour.

public static class AverageReducer extends
        Reducer<IntWritable, CountAverageTuple, IntWritable, CountAverageTuple> {

       private CountAverageTuple result = new CountAverageTuple();

       public void reduce(IntWritable key, Iterable<CountAverageTuple> values, Context context)
               throws IOException, InterruptedException {

         int sum = 0;
         float count = 0;

         for (CountAverageTuple val : values) {
           sum += val.getCount() * val.getAverage();
           count += val.getCount();
         }

         result.setCount(sum);
         result.setAverage(sum / count);

         context.write(key, result);
       }
 }
Job

public static void main(String[] args) throws Exception {
int res = ToolRunner.run(new Configuration(), new AverageCommentLengthByHour(), args); System.exit(res);
}

@Override public int run(String[] args) throws Exception {

Configuration conf = new Configuration(); String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs(); if (otherArgs.length != 2) {

System.err.println(“Usage: AverageCommentLengthByHour <in> <out>”); ToolRunner.printGenericCommandUsage(System.err); System.exit(2);
}

Job job = new Job(conf, “StackOverflow Average Comment Length By Hour”); job.setJarByClass(AverageCommentLengthByHour.class); job.setMapperClass(AverageMapper.class); job.setCombinerClass(AverageReducer.class); job.setReducerClass(AverageReducer.class); job.setOutputKeyClass(IntWritable.class); job.setOutputValueClass(CountAverageTuple.class); FileInputFormat.addInputPath(job, new Path(otherArgs[0])); FileOutputFormat.setOutputPath(job, new Path(otherArgs[1])); boolean success = job.waitForCompletion(true);

return success ? 0 : 1;

}

Running the Code

$ hadoop jar ./target/mrdpatterns-1.0-SNAPSHOT.jar \
        com.deploymentzone.mrdpatterns.AverageCommentLengthByHour \
        /mrdp/datascience.stackexchange.com/Comments.xml /mrdp/output
Output

$ hadoop fs -cat /mrdp/output/part-r-00000
0       3068497 222.4677
1       1747070 217.29726
2       1995013 210.55547
3       1711035 234.93547
4       2106781 218.81813
5       2129769 196.78175
6       2367701 195.41936
7       2655747 182.19998
8       2414720 175.9487
9       3731131 195.12242
10      3073206 173.57843
11      3126461 188.48863
12      2977856 183.95453
13      5755116 216.30896
14      5825227 200.43446
15      6316020 196.8466
16      5891920 208.9111
17      5249475 188.97278
18      4537627 199.50874
19      3935660 190.01834
20      6020116 227.81033
21      4273081 209.88658
22      3363404 219.19995
23      3513618 207.0


#Summarization - Median Standard Deviation

In this lab you will use the StackOverflow User Comments to find the following

Median length of comments in each hour
Standard Deviation of Length for comments in each hour.
Input Data

Downloaded from link. We will use the user comments file Comments.xml Sample of the file is listed below.

<?xml version="1.0" encoding="utf-8"?>
<comments>
        <row Id="5" PostId="5" Score="9"
                Text="this is a super theoretical AI question. An interesting discussion! but out of place..."
                CreationDate="2014-05-14T00:23:15.437" UserId="34" />
        <row Id="6" PostId="7" Score="4" Text="List questions are usually not suited for Stack Exchange
                websites since there isn't an &quot;objective&quot; answer or a way to measure the usefulness
        of an answer. Having said that, one of my recommendations would be MacKay's &quot;Information
        Theory, Inference, and Learning Algorithms.&quot;"
        CreationDate="2014-05-14T00:38:19.510" UserId="51" />
</comments>
Mapper Code

Mapper MedianStdDevMapper takes in Input Comment line which is an Xml element and returns the outHour and out. Both are of type IntWritable.

It extends the Generic Mapper
Input Xml is parsed using the method transformXmlToMap(..) to a map parsed of type Map<String, String>.
From the Map CreationDate and Text are extracted
outHour and out objects are populated
Output is written to the context object.
context.write(outHour, outTuple);
Code snippets can be seen below.

 public static class MedianStdDevMapper
        extends Mapper<Object, Text, IntWritable, IntWritable> {

        private IntWritable outHour = new IntWritable();
        private IntWritable out = new IntWritable();

        @SuppressWarnings("deprecation")
        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {
          Map<String,String> parsed = transformXmlToMap(value.toString());

          String strDate = parsed.get("CreationDate");
          String text = parsed.get("Text");

          if (isNullOrEmpty(strDate) || isNullOrEmpty(text)) {
            return;
          }

          Date creationDate;

          try {
            creationDate = DATE_FORMAT.parse(strDate);
          } catch (ParseException e) {
            e.printStackTrace();
            return;
          }

          outHour.set(creationDate.getHours());
          out.set(text.length());
          context.write(outHour, out);

        }
}
Reducer Code

In the reducer code we iterate over Iterable<CountAverageTuple> values to calculate the count and average for each hour.

public static class MedianStdDevReducer extends
        Reducer<IntWritable, IntWritable, IntWritable,
        MedianStandardDeviationTuple> {

        private MedianStandardDeviationTuple result =
                new MedianStandardDeviationTuple();
        private List<Float> commentLengths = new ArrayList<Float>();

        public void reduce(IntWritable key, Iterable<IntWritable> values,
                        Context context) throws IOException, InterruptedException {
                commentLengths.clear();
                result.setStandardDeviation(0);

                for (IntWritable val : values) {
                        commentLengths.add((float)val.get());
                }

                result.deriveMedian(commentLengths);
                result.deriveStandardDeviation(commentLengths);
                context.write(key, result);
        }
}
Job Creation and Execution

public static void main(String[] args) throws Exception {
        int res = ToolRunner.run(new Configuration(),
                new MedianAndStandardDeviationCommentLengthByHour(), args);
        System.exit(res);
  }

  @Override
  public int run(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        if (otherArgs.length != 2) {
          System.err.println("Usage: MedianAndStandardDeviationCommentLengthByHour <in> <out>");
          ToolRunner.printGenericCommandUsage(System.err);
          System.exit(2);
        }

        Job job = new Job(conf, "StackOverflow Median and Standard Deviation Comment Length By Hour");
        job.setJarByClass(MedianAndStandardDeviationCommentLengthByHour.class);
        job.setMapperClass(MedianStdDevMapper.class);
        job.setReducerClass(MedianStdDevReducer.class);
        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));
        boolean success = job.waitForCompletion(true);

        return success ? 0 : 1;
}
Running the Code

$ hadoop jar ./target/mrdpatterns-1.0-SNAPSHOT.jar \
        com.deploymentzone.mrdpatterns.MedianAndStandardDeviationCommentLengthByHour \
        /mrdp/datascience.stackexchange.com/Comments.xml /mrdp/outputavgstdev
Output

$ hadoop fs -cat  /mrdp/outputavgstdev/part-r-00000
0       170.5   153.8939
1       184.0   144.5877
2       190.0   153.19885
3       183.0   149.38205
4       170.5   146.31319
5       149.0   161.99849
6       152.5   147.57478
7       134.5   143.51433
8       148.0   125.56117
9       151.5   140.95326
10      147.5   126.79869
11      163.0   138.04395
12      135.0   131.61192
13      169.0   154.32361
14      150.0   145.27602
15      160.0   137.36118
16      162.0   151.96437
17      152.0   129.39383
18      162.5   136.75435
19      142.0   146.75641
20      190.0   148.06378
21      171.0   142.05786
22      161.0   163.24771
23      175.0   144.7733

#Filtering - Top Ten Users by Reputation

In this lab you will find top ten users by Reputation.

Input Data

Downloaded from `https://archive.org/download/stackexchange/datascience.stackexchange.com.7z`_. We will use the user comments file Users.xml Sample of the file is listed below.

<row Id="-1" Reputation="1"
        CreationDate="2014-05-13T21:29:22.820" DisplayName="Community"
        LastAccessDate="2014-05-13T21:29:22.820"
        WebsiteUrl="http://meta.stackexchange.com/"
        Location="on the server farm" AboutMe="..;"
        Views="0" UpVotes="506"
        DownVotes="37" AccountId="-1" />
Mapper Code

Mapper takes in Input User line which is an Xml element and returns the reputation and new Pair<String, String>(userId, displayName). This is a custom type created and contains the following elements

public class Pair<T1, T2> {
  private final T1 first;
  private final T2 second;

  public Pair(T1 first, T2 second) {
        this.first = first;
        this.second = second;
  }

  public T1 getFirst() {
        return first;
  }

  public T2 getSecond() {
        return second;
  }
}
The mapper processes all input records and stores them in a TreeMap. A TreeMap is a subclass of Map thatsorts on key. The default ordering of Integers is ascending. Then, if there are more than ten records in ourTreeMap, the first element (lowest value) can be removed. After all the records have been processed, the top ten records in the TreeMap are output to the reducers in the cleanup method. This method gets called once after all key/value pairs have been through map, just like how setup is called once before any calls to map.

    public static class TopTenMapper extends Mapper<Object,
            Text, IntWritable, TextArrayWritable> {
private TreeMap<Integer, Pair<String, String>> repToRecordMap =
            new TreeMap<Integer, Pair<String, String>>();

@Override
public void map(Object key, Text value, Context context) throws IOException,
            InterruptedException {
  Map<String, String> parsed = transformXmlToMap(value.toString());

  String userId = parsed.get("Id");
  String reputation = parsed.get("Reputation");
  String displayName = parsed.get("DisplayName");

  if (isNullOrEmpty(userId) || isNullOrEmpty(reputation)
            || !isInteger(reputation) || isNullOrEmpty(displayName)) {
    return;
  }

  // of course in ties, last one in wins
  int rep = Integer.parseInt(reputation);
  repToRecordMap.put(rep, new Pair<String, String>(userId, displayName));

  if (repToRecordMap.size() > 10) {
    repToRecordMap.remove(repToRecordMap.firstKey());
  }
}
Reducer Code

Reducer determines its top ten records in a way that’s very similar to the mapper. Because we configured our job to have one reducer using job.setNumReduceTasks(1) and we used NullWritableas our key, there will be one input group for this reducer that contains all the potential top ten records. The reducer iterates through all these records and stores them in a TreeMap. If the TreeMap’s size is above ten, the first element (lowest value) is remove from the map. After all the values have been iterated over, the values contained in the TreeMap are flushed to the file system in descending order. This ordering is achieved by getting the descending map from the TreeMap prior to outputting the values. This can be done directly in thereduce method, because there will be only one input group, but doing it in the cleanup method would alsowork.

    public static class TopTenReducer extends Reducer<IntWritable,
            TextArrayWritable, IntWritable, TextArrayWritable> {
    private TreeMap<Integer, Pair<Writable, Writable>>
            repToRecordMap = new TreeMap<Integer, Pair<Writable, Writable>>();

            @Override
            public void reduce(IntWritable key, Iterable<TextArrayWritable> values,
                    Context context) throws IOException,
                InterruptedException {
              for (ArrayWritable value : values) {
                repToRecordMap.put(Integer.valueOf(key.get()), new Pair<Writable,
                            Writable>(value.get()[0], value.get()[1]));
                if (repToRecordMap.size() > 10) {
                  repToRecordMap.remove(repToRecordMap.firstKey());
                }
              }
}
Job

$ hadoop jar ./target/mrdpatterns-1.0-SNAPSHOT.jar \
com.deploymentzone.mrdpatterns.TopTenUsersByReputation \
/mrdp/datascience.stackexchange.com/Users.xml /mrdp/outputtoptenreputation
Output

    $ hadoop fs -cat /mrdp/outputtoptenreputation/part-r-00000
2262        2452    Aleksandr Blekh
    1489    548     indico
    1386    84      Rubens
    1356    434     Steve Kallestad
    1255    21      Sean Owen
    1101    1279    ffriend
    1026    26      Alex I
    996     381     Emre
    841     108     rapaio
    747     97      IharS

