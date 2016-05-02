title: MapReduce
date: 2016-05-02
description: MapReduce tutorial with Java.
tags: programming, hadoop, bigdata, yarn

##MapReduce : Find Maximum Temperature

In this Map Reduce program we will calculate the Maximum Termperature for each Year from NCDC data.

Mapper

Implemented by extending org.apache.hadoop.mapreduce.Mapper class

public class MaxTemperatureMapper
    extends Mapper<LongWritable, Text, Text, IntWritable> {

        @Override
        public void map(LongWritable key, Text value,
                Context context)
                  throws IOException, InterruptedException {
        }
}
Complete Code Listing

public class MaxTemperatureMapper
  extends Mapper<LongWritable, Text, Text, IntWritable> {

  private static final int MISSING = 9999;

  @Override
  public void map(LongWritable key, Text value, Context context)
          throws IOException, InterruptedException {

        String line = value.toString();
        String year = line.substring(15, 19);
        int airTemperature;
        if (line.charAt(87) == '+') {
 // parseInt doesn't like leading plus signs
          airTemperature = Integer.parseInt(line.substring(88, 92));
        } else {
          airTemperature = Integer.parseInt(line.substring(87, 92));
        }
        String quality = line.substring(92, 93);
        if (airTemperature != MISSING && quality.matches("[01459]")) {
          context.write(new Text(year),
      new IntWritable(airTemperature));
        }
  }
}
Reducer

MaxTemperatureReducer

public class MaxTemperatureReducer
  extends Reducer<Text, IntWritable, Text, IntWritable> {

  @Override
  public void reduce(Text key, Iterable<IntWritable> values,
          Context context)
          throws IOException, InterruptedException {

        int maxValue = Integer.MIN_VALUE;
        for (IntWritable value : values) {
          maxValue = Math.max(maxValue, value.get());
        }
        context.write(key, new IntWritable(maxValue));
  }
}
Job Class MaxTemperature

public class MaxTemperature {

  public static void main(String[] args) throws Exception {
        Job job = new Job();
        job.setJarByClass(MaxTemperature.class);
        job.setJobName("Max temperature");

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        job.setMapperClass(MaxTemperatureMapper.class);
        job.setReducerClass(MaxTemperatureReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
Execute the MaxTemperature Job as shown below:

hadoop MaxTemperature /ncdc/all output
Where /ncdc/all is the input directory and output is a relative path in HDFS with absolute value /user/hduser/output.

MapReduce : Find Maximum Temperature With Combiner

In this Map Reduce program we will calculate the Maximum Termperature for each Year from NCDC data by using a Combiner in Addition to a Mapper and Reducer. Combiner is set on the Job object as show below. This will reduce the shuffling and sorting happening between the mapper and reducer.

 public class MaxTemperatureWithCombiner {

     public static void main(String[] args) throws Exception {
         ...
         Job job = new Job();
         job.setJarByClass(MaxTemperatureWithCombiner.class);
         job.setJobName("Max temperature");

         FileInputFormat.addInputPath(job, new Path(args[0]));
         FileOutputFormat.setOutputPath(job, new Path(args[1]));

         job.setMapperClass(MaxTemperatureMapper.class);
         /*[*/job.setCombinerClass(MaxTemperatureReducer.class)/*]*/;
         job.setReducerClass(MaxTemperatureReducer.class);

         job.setOutputKeyClass(Text.class);
         job.setOutputValueClass(IntWritable.class);

         System.exit(job.waitForCompletion(true) ? 0 : 1);
   }
 }
hadoop MaxTemperatureWithCombiner /ncdc/all output
Where /ncdc/all is the input directory and output is a relative path in HDFS with absolute value /user/hduser/output.

MapReduce : Max Temperature with Compression

In this Map Reduce program output is compressed into a Gzip file by setting the FileOutputFormat Compressor Class using the command FileOutputFormat.setOutputCompressorClass(job, GzipCodec.class)

     public class MaxTemperatureWithCompression {
       public static void main(String[] args) throws Exception {
             if (args.length != 2) {
               System.err.println("Usage: MaxTemperatureWithCompression <input path> " +
                 "<output path>");
               System.exit(-1);
             }

             Job job = new Job();
             job.setJarByClass(MaxTemperature.class);

             FileInputFormat.addInputPath(job, new Path(args[0]));
             FileOutputFormat.setOutputPath(job, new Path(args[1]));

             job.setOutputKeyClass(Text.class);
             job.setOutputValueClass(IntWritable.class);

             /*[*/FileOutputFormat.setCompressOutput(job, true);
             FileOutputFormat.setOutputCompressorClass(job, GzipCodec.class);/*]*/

             job.setMapperClass(MaxTemperatureMapper.class);
             job.setCombinerClass(MaxTemperatureReducer.class);
             job.setReducerClass(MaxTemperatureReducer.class);

             System.exit(job.waitForCompletion(true) ? 0 : 1);
       }
     }
hadoop MaxTemperatureWithCompression /ncdc/all output
Sorting Data using SequenceFiles

We are going to sort the weather dataset by temperature. Storing temperatures as Text objects doesn’t work for sorting purposes, because signed integers don’t sort lexicographically. Instead, we are going to store the data using sequence files whose IntWritable keys represent the temperature (and sort correctly) and whose Text values are the lines of data.

Sort Data Processor The MapReduce job shown below is a map-only job that also filters the input to remove records that don’t have a valid temperature reading. Each map creates a single block-compressed sequence file as output.

public class SortDataPreprocessor extends Configured implements Tool {

  static class CleanerMapper
        extends Mapper<LongWritable, Text, IntWritable, Text> {

        private NcdcRecordParser parser = new NcdcRecordParser();

        @Override
        protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

          parser.parse(value);
          if (parser.isValidTemperature()) {
            context.write(new IntWritable(parser.getAirTemperature()), value);
          }
        }
  }

  @Override
  public int run(String[] args) throws Exception {
        Job job = JobBuilder.parseInputAndOutput(this, getConf(), args);
        if (job == null) {
          return -1;
        }

        job.setMapperClass(CleanerMapper.class);
        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(Text.class);
        job.setNumReduceTasks(0);
        job.setOutputFormatClass(SequenceFileOutputFormat.class);
        SequenceFileOutputFormat.setCompressOutput(job, true);
        SequenceFileOutputFormat.setOutputCompressorClass(job, GzipCodec.class);
        SequenceFileOutputFormat.setOutputCompressionType(job,
            CompressionType.BLOCK);

        return job.waitForCompletion(true) ? 0 : 1;
  }
  public static void main(String[] args) throws Exception {
        int exitCode = ToolRunner.run(new SortDataPreprocessor(), args);
        System.exit(exitCode);
  }
It is invoked with the following command:

hadoop jar hadoop-examples.jar SortDataPreprocessor /ncdc/all /input/ncdc/all-seq
Sort SequenceFile input using HashPartitioner

Code Below is a variation for sorting sequence files with IntWritable keys generated above

public class SortByTemperatureUsingHashPartitioner extends Configured
  implements Tool {

  @Override
  public int run(String[] args) throws Exception {
        Job job = JobBuilder.parseInputAndOutput(this, getConf(), args);
        ..

        job.setInputFormatClass(SequenceFileInputFormat.class);
        job.setOutputKeyClass(IntWritable.class);
        job.setOutputFormatClass(SequenceFileOutputFormat.class);

        return job.waitForCompletion(true) ? 0 : 1;
  }

  public static void main(String[] args) throws Exception {
        int exitCode = ToolRunner.run(new SortByTemperatureUsingHashPartitioner(),
            args);
        System.exit(exitCode);
  }
}
Command to execute the Program above

hadoop SortByTemperatureUsingHashPartitioner /input/ncdc/all-seq output-hashsort
Assignment

Create a MinTemperature Job which run MinTemperatureMapper and Reducer on ncdc data

