import React, {useState} from "react";
const StudentForm=()=>{
    const[name,setName]=useState("");
    const[age,setAge]=useState("");
    const[email,setEmail]=useState("");
    const[course,setCourse]=useState("");
    const[message,setMessage]=useState("");
const handleSubmit=async(e)=>{
    e.preventDefault();
    try{
        const form=document.getElementById('studform');
        const res=await fetch('http://localhost:4000/api/students',{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify({name,age,email,course})
        });
        if(res.ok){
            setMessage('Student details saves successfully');
        }else{
            const err=await res.json();
            setMessage(`Error:${err.message}`);
        }
    }catch(error){
        setMessage('network error');
    }
}
return (
    <div>
    <h2>Student Bio-details</h2>
    <form onSubmit={handleSubmit} id='studform'>
        <div>
        <label>Name:</label>
        <input type="text" name='name' onChange={(e)=>setName(e.target.value)} required/>
        </div>
        <div>
            <label>Age:</label>
            <input type="number" name="age" id="" onChange={(e)=>setAge(e.target.value)} required/>
        </div>
        <div>
            <label htmlFor="">Email:</label>
            <input type="email" name="email" id="" onChange={(e)=>setEmail(e.target.value)} required/>
        </div>
        <div>
            <label htmlFor="">Course:</label>
            <input type="text" name="course" onChange={(e)=>setCourse(e.target.value)} id="" required/>
        </div>
        <button type='submit'>Submit</button>
    </form>
    {message && <p>{message}</p>}
    </div>
);
}
export default StudentForm;