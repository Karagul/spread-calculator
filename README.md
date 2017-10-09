# spread-calculator
## Problem Define
This is a python approach to calculate the bond spread between corporate bonds and government bonds. There are two different ways of calculating the spread:
1. Based on the most similar government bond based on the term of the bond
2. Based on the linear interpolation of government bond

## Assumptions
First assumption we made is: the input is not sorted. Although the sample input is in a perfect ascending order, the description of the task didn't make the same assumption, to be cautious, our approach won't assume the data is pre-sorted.\
Second assumption is: not deal with cases when corporate bond does't fall under two government bonds. This is being mentioned in the task description already.

## Methodology
The simplist approach is as follows:
1. separate the csv file into corporate bond list and government bond list
2. do linear search for each corporate bond to find the nearest government bonds and do the calculation.

Instead of doing linear search for each corporate bond, which is the complexity of n sqaure, what we can do it pre-sort the list and use the order at most.
Here is what we did in the code:
- don't separate the csv file, instead, sort the whole list by term
- do one round of loop from the top of sorted list, record the nearest pre government bonds
- do one round of loop from the tail of sorted list, record the nearest post government bonds
- retrieve the benchmark bond or linear interpolation based on the adjacent nearest government bonds found from both direction.
Assume we use merge sort algorithm which can achieve the complexity of nlog(n), the total complexity will be nlog(n) + n << n square when n is big.
In other words, the method will be sort bonds -> create adjacent map -> calculate spread.

## Test
To test if the approach is correct or not, we used python built-in unittest module to test the previous method.\
Since 'sort bonds' uses the built-in sorting algorithm, we built three tests to help test:
1. create adjacent map
2. calcualte benchmark spread
3. calcualte linear interpolation spread

## How to run
To calcualte the spread, please run:
```
python spread_calculator.py --input_file='input_path.csv' --output_file='result_path.csv' --find_benchmark_bonds=True --calculate_spread_to_curve=True
```
*find_benchmark_bonds* refers to challendge 1, if set to true, it will return the result in output file;\
*calcualte_spread_to_curve* refers to challendge 2, if set to true, it will return the result in output file.

To test the module, please run:
```
python -m unittest discover -s tests -p "test_*.py"

```

## Work load
The practise python apporach took around 2 hours, if counting the time for adding documents, tests and the readme file. The simplarity of the probelm shouldn't take that long. However, instead of using the most familiar language, we would like to use that chance to practise the coding skill using python.

## Future work / Improvement

One improvement we can do is: since python doesn't have pointer like c/c++/golang, and we created a struct/object to carry all the information related to a bond even after move to adjacent map buildng or calcualting the spread, it will eat more memory.

What can be done is create anothe map which map a int type of id to the bond. Later on, instead of carrying the whole object, we can use the id, and check the information by id when needed.

Since the complexity of hash map is O(1), it should free the memory without introducing complexity to the computation. However, since the data we are playing with is small, and the author don't expect we will have "big data" level of bonds information for now, we leave that part as the future work.


