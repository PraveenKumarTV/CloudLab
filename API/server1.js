const express= require('express');
const bodyParser=require('body-parser');
const cors=require('cors');
const app=express();
const {MongoClient}=require('mongodb');
app.use(bodyParser.json());
app.use(cors());
const port=3000;
const uri="mongodb+srv://praveenkumartv1:praveen123@praveendb.ac0h0.mongodb.net/";
let db,usersCollection;
MongoClient.connect(uri,{useNewUrlParser:true,useUnifiedTopology:true})
.then(client=>{
	db=client.db("test");
	usersCollection=db.collection('users');
	console.log("Connected to Mongodb Atlas");
})
let users=[];
app.get('/users',async(req,res)=>{
   try{
   	const users=await usersCollection.find({}).toArray();
   	res.json(users);
   }catch(error){
   	res.status(500).json({error:'Failed to fetch'});
   }
});
app.post('/users',async(req,res)=>{
    const {username,password}=req.body;
    if(!username || !password){
        return res.status(400).json({error:'Username and password are required'});
    }
    try{
    await usersCollection.insertOne({username,password});
    return res.status(201).json({message:'User created successfully'});
    }catch(error){
    	res.status(500).json({error:'Failed to create user'});
    }
});
app.put('/users/:username',async(req,res)=>{
    const {username}=req.params;
    const {password}=req.body;
    try{
    	const res=await usersCollection.updateOne({username},{$set:{password}});
    	if(res.matchedCount==0){
    		return res.status(400).json({error:'user not found'});
    	}
    	return res.status(201).json({message:'User updated successfully'});
    }catch(error){
    	res.status(500).json({error:'Failed to update'});
    }
});
app.delete('/users/:username',async(req,res)=>{
    const {username}=req.params;
    try{
    	const res=await usersCollection.deleteOne({username});
    	if(res.deletedCount===0){
    		return res.status(400).json({error:'User not found'});
    	}
    	return res.status(200).json({message:'User deleted'});
    }catch(error){
    	res.status(500).json({error:'Failed to delete user'});
    }
});

app.listen(port,()=>{
    console.log(`Server is running on port ${port}`);
});
