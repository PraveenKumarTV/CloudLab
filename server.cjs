const express=require('express');
const cors=require('cors');
const {MongoClient}=require('mongodb');
const app=express();
app.use(cors());
const port=4000;
const url='mongodb+srv://praveenkumartv1:praveen123@praveendb.ac0h0.mongodb.net/';
const dbName="praveendb";
const collectionName="studentsBio";
app.use(express.json());
MongoClient.connect(url,{useUnifiedTopology:true})
.then(client=>{
    db=client.db(dbName);
    col=db.collection(collectionName);
    console.log("Connected to MongoDb");
}).catch(err=>{
    console.log('Error connection to mongodb',err);
});
app.post('/api/students',async (req,res)=>{
    try{
    const {name,age,email,course}=req.body;
    const result=await col.insertOne({name,age,email,course});
    res.status(201);
    }catch(err){
        console.log('Error inserting student');
        res.status(500);
    }
});
app.listen(port,()=>{
    console.log(`Server is running on port ${port}`);
})