rm -rf ~/ENGG4030/hw2/candidates.txt ~/ENGG4030/hw2/mr_output.txt

./bin/hdfs dfs -rmr -skipTrash /hw2_q1b_job1 /hw2_q1b_job2

./bin/hadoop jar ./share/hadoop/tools/lib/hadoop-streaming-2.7.5.jar \
-file ~/ENGG4030/hw2/q1b-job1-mapper.py \
-file ~/ENGG4030/hw2/q1b-job1-reducer.py \
-file ~/ENGG4030/hw2/utils.py \
-mapper "q1b-job1-mapper.py 0.0025 1" \
-reducer "q1b-job1-reducer.py 0.0025 1" \
-input /shakespeare-basket1.txt \
-input /shakespeare-basket2.txt \
-output /hw2_q1b_job1

./bin/hdfs dfs -copyToLocal /hw2_q1b_job1/part-00000 ~/ENGG4030/hw2/candidates.txt

./bin/hadoop jar ./share/hadoop/tools/lib/hadoop-streaming-2.7.5.jar \
-file ~/ENGG4030/hw2/q1b-job2-mapper.py \
-file ~/ENGG4030/hw2/q1b-job2-reducer.py \
-file ~/ENGG4030/hw2/utils.py \
-file ~/ENGG4030/hw2/candidates.txt \
-mapper "q1b-job2-mapper.py 0.0025 3" \
-reducer "q1b-job2-reducer.py 0.0025 3" \
-input /shakespeare-basket1.txt \
-input /shakespeare-basket2.txt \
-output /hw2_q1b_job2

./bin/hdfs dfs -copyToLocal /hw2_q1b_job2/part-00000 ~/ENGG4030/hw2/mr_output.txt

cat ~/ENGG4030/hw2/mr_output.txt | sort -nrk 2 > ~/ENGG4030/hw2/mr_output_sorted.txt