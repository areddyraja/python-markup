title: Cassandra Commands
date: 2016-05-02
description: A tutorial on Docker
tags: docker, kubernets, spark, programming, hadoop, bigdata, yarn

Cassandra Commands

#### To see all the keyspaces and their network topoplogies
    SELECT * FROM system.schema_keyspaces;
    
#### Multi Datacenter approach
   cassandra-topology.properties   is to be updated with Data Center information
   
   
##### Periodically run the nodetool cleanup
	
	:::text
	nodetool -h host cleanup

   cleans up all the keys that does not belong to this node.
   
##### For the statistics of all the column families

	:::shell
   	bin/nodetool --host 10.64.21.186   cfstats
   
##### For getting the cf histograms for the collector

	:::text
	bin/nodetool  cfhistorgrams yupptv_analytics_collector ys_user_stats


##### Describe ring

	:::text
   	bin/nodetool describering yupptv_analytics_collector

##### To start a Table Compaction

	:::text
   	bin/nodetool compact yupptv_analytics_collector program_active_count

##### To cleanup the snapshots

	:::text
	bin/nodetool clearsnapshot yupptv_analytics_collector


##### References
	
	* http://jonathanhui.com/cassandra-data-maintenance-backup-and-system-recovery
          Has details about taking backup and restore details on the page
   
	* Levelled compaction is better for getting the performance of read
          (For write, it is good to have sizebased compaction)

        * http://www.datastax.com/dev/blog/when-to-use-leveled-compaction
   

