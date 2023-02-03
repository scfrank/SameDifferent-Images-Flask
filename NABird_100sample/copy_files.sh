
NABIRDS_ROOT='/home/stella/datasets/NAbirds/nabirds/images/'
for file in $(cat ./sample_100_NAB.txt)
do
  echo $NABIRDS_ROOT$file
  cp $NABIRDS_ROOT$file .
done
