#include<iostream>
#include<omp.h>
using namespace std;
int main(){
	int nums[10];
	int sum=0;
	for(int i=0;i<10;i++){
		nums[i]=i+1;
	}
#pragma omp parallel for reduction(+:sum)
	for(int i=0;i<10;i++){
		sum+=nums[i];
	}
	cout<<"Sum of array elements: "<<sum<<endl;
	return 0;

}
