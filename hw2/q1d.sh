THRESHOLD=$1
N_ITEM=$2
N_MAPPER=5
N_REDUCER=5

if [ "$#" -ne 2 ]; then
	echo "usage: sh q1d.sh [threshold] [n_item]"
	exit 1
fi

rm -rf ~/ENGG4030/hw2/candidates.txt ~/ENGG4030/hw2/mr_output.txt

./bin/hdfs dfs -rmr -skipTrash /hw2_q1b_job1 /hw2_q1b_job2

./bin/hadoop jar ./share/hadoop/tools/lib/hadoop-streaming-2.7.5.jar \
-D mapred.map.tasks=$N_MAPPER \
-D mapred.reduce.tasks=$N_REDUCER \
-file ~/ENGG4030/hw2/q1d-job1-mapper.py \
-file ~/ENGG4030/hw2/q1b-job1-reducer.py \
-file ~/ENGG4030/hw2/utils.py \
-mapper "q1d-job1-mapper.py $THRESHOLD $N_ITEM" \
-reducer "q1b-job1-reducer.py $THRESHOLD $N_ITEM" \
-input /shakespeare-basket1.txt \
-input /shakespeare-basket2.txt \
-output /hw2_q1b_job1

./bin/hdfs dfs -copyToLocal /hw2_q1b_job1/part-00000 ~/ENGG4030/hw2/candidates.txt

./bin/hadoop jar ./share/hadoop/tools/lib/hadoop-streaming-2.7.5.jar \
-D mapred.map.tasks=$N_MAPPER \
-D mapred.reduce.tasks=$N_REDUCER \
-file ~/ENGG4030/hw2/q1d-job2-mapper.py \
-file ~/ENGG4030/hw2/q1b-job2-reducer.py \
-file ~/ENGG4030/hw2/utils.py \
-file ~/ENGG4030/hw2/candidates.txt \
-mapper "q1d-job2-mapper.py $THRESHOLD $N_ITEM" \
-reducer "q1b-job2-reducer.py $THRESHOLD $N_ITEM" \
-input /shakespeare-basket1.txt \
-input /shakespeare-basket2.txt \
-output /hw2_q1b_job2

./bin/hdfs dfs -copyToLocal /hw2_q1b_job2/part-00000 ~/ENGG4030/hw2/mr_output.txt

cat ~/ENGG4030/hw2/mr_output.txt | sort -nrk 2 > ~/ENGG4030/hw2/mr_output_sorted.txt