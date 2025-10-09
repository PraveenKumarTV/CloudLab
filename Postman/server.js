const express= require('express');
const bodyParser=require('body-parser');
const cors=require('cors');
const app=express();
app.use(bodyParser.json());
app.use(cors());
const port=3000;
let users=[];
app.get('/users',(req,res)=>{
    res.json(users);
});
app.post('/users',(req,res)=>{
    const {username,password}=req.body;
    if(!username || !password){
        return res.status(400).json({error:'Username and password are required'});
    }
    users.push({username,password});
    return res.status(201).json({message:'User created successfully'});
});
app.put('/users/:username',(req,res)=>{
    const {username}=req.params;
    const {password}=req.body;
    const user=users.find(u=>u.username==username);
    if(!user){
        res.status(400).json({error:'User not found'});
    }
    user.password=password;
    return res.status(201).json({message:'User updated successfully'});
});
app.delete('/users/:username',(req,res)=>{
    const {username}=req.params;
    const userInd=users.findIndex(u=>u.username==username);
    if(userInd===-1){
        return res.status(400).json({error:'User not found'});
    }
    users.splice(userInd,1);
    return res.status(201).json({message:'User deleted successfully'});
})
app.post('/weather',async(req,res)=>{
    const {city}=req.body;
    if(!city){
        return res.status(400).json({error:'City is invalid'});
    }
    const apiKey='665a26335661e6b4e444edf5903ec02e';
    const weatherData=`https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&appid=${apiKey}&units=metric`
    const response=await fetch(weatherData);
    if(!response.ok){
        return res.status(400).json({error:'Could not fetch weather data'});
    }
    const data=await response.json();
    return res.json({
        city:data.name,
        temperature:data.main.temp,
        weather:data.weather[0].description
    });


})

app.listen(port,()=>{
    console.log(`Server is running on port ${port}`);
});