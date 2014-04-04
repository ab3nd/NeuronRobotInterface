for x in {2,5}
do
	./minmaxcluster.py ../../scripts/python_scripts/averages/mature_culture.avg 10 $x
done

for x in {20,50}
do
	./minmaxcluster.py ../../scripts/python_scripts/averages/mature_culture.avg 100 $x
done

for x in {20,50,100}
do
	./minmaxcluster.py ../../scripts/python_scripts/averages/mature_culture.avg 200 $x
done

for x in {50,100,250}
do
	./minmaxcluster.py ../../scripts/python_scripts/averages/mature_culture.avg 500 $x
done

for x in {100,250,500}
do
	./minmaxcluster.py ../../scripts/python_scripts/averages/mature_culture.avg 1000 $x
done

