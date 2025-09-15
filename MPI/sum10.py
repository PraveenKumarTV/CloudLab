from mpi4py import MPI
comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()
nums=list(range(10))
chunk_size=10//size
start=rank*chunk_size
end=start+chunk_size if rank!=size-1 else 10
thread_sum=sum(nums[start:end])
print("Process ",rank," computed sum:",thread_sum)
global_sum=comm.reduce(thread_sum,op=MPI.SUM,root=1)
if(rank==1):
    print("Total sum: ",global_sum)
